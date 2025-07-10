# Etap 1: Builder (with Node.js and Python deps)
FROM python:3.11-slim AS builder

# Instalacja Node.js (dodanie repozytorium NodeSource i instalacja Node 18 LTS)
RUN apt-get update && apt-get install -y curl gnupg && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs build-essential && \
    rm -rf /var/lib/apt/lists/*

# Ustawienie katalogu roboczego
WORKDIR /app

# Kopiowanie plików zależności frontendowych i backendowych
COPY frontend/package.json frontend/package-lock.json ./frontend/
COPY app/requirements.txt ./

# Instalacja zależności Pythona (we wspólnym środowisku)
RUN pip install -r requirements.txt

# Instalacja zależności Node (frontend)
RUN cd frontend && npm ci

# Kopiowanie kodu źródłowego frontend i budowanie aplikacji frontendu
COPY frontend/. ./frontend/
# Budowanie projektu frontend (Vite) – wyjście trafi do app/static
RUN cd frontend && npx vite build

# Etap 2: Finalny obraz produkcyjny (tylko Python, bez Node)
FROM python:3.11-slim AS production

# Ustawienie katalogu roboczego
WORKDIR /app

# Kopiowanie zbudowanych zależności Pythona z buildera (opcjonalnie można też wykonać pip install ponownie)
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn
COPY --from=builder /usr/local/bin/gunicorn /usr/local/bin/gunicorn

# Kopiowanie kodu aplikacji i statycznych plików frontend (z buildera)
COPY --from=builder /app/app /app/app
COPY --from=builder /app/templates/dist /app/app/static

# Ustawienie domyślnego polecenia (Gunicorn z workerami Uvicorn dla produkcji)
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--workers", "4", "--bind", "0.0.0.0:8000", "app.main:app"]
