import { LitElement, html, css } from 'lit';
import { customElement, property, state } from 'lit/decorators.js';

@customElement('my-component')
export class MyComponent extends LitElement {
  @property({type: String}) declare name: string;
  @state()            declare apiMessage: string;

  constructor() {
    super();
    this.name       = 'World';   // <- ustawienie bez konfliktu
    this.apiMessage = '';
  }

  static styles = css`
    .hello { color: #3366ff; font-weight: bold; }
    .message { font-style: italic; margin-top: 0.5em; }
  `;

  // Metoda lifecycle Lit wywoływana po pierwszym renderze komponentu
  firstUpdated() {
    // Po załadowaniu komponentu – pobranie danych z API
    this.fetchMessageFromApi();
  }

  async fetchMessageFromApi() {
    try {
      const response = await fetch('/api/hello');
      if (!response.ok) {
        console.error('API responded with status', response.status);
        return;
      }
      const data = await response.json();
      this.apiMessage = data.message || '';
    } catch (error) {
      console.error('Error fetching API message:', error);
    }
  }

  render() {
    return html`
      <p class="hello">Hello, ${this.name}!</p>
      ${this.apiMessage 
          ? html`<p class="message">Wiadomość z serwera: "${this.apiMessage}"</p>`
          : html`<p class="message">Ładowanie wiadomości...</p>`}
    `;
  }
}
