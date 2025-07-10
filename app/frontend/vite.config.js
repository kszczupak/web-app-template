import { defineConfig } from 'vite';
import path from 'path';

export default defineConfig({
  // Root katalogu projektu frontend (bieżący)
  root: __dirname,
  build: {
    outDir: path.resolve(__dirname, "../app/static"),
    emptyOutDir: true    // czyści katalog statyczny przed każdą kompilacją
  },
  server: {
    port: 5173,
    strictPort: true,
    // Proxy przekierowujące zapytania API podczas developmentu do backendu FastAPI
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true
      }
    }
  }
});
