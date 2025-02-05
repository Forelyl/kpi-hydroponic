class HomeButton extends HTMLElement {
  constructor() {
    super();

    // Create shadow DOM
    const shadow = this.attachShadow({ mode: 'open' });

    // Elements
    this.container      = document.createElement('a');
    this.svg_container  = document.createElement('div');

    // Attributes
    this.svg_container.innerHTML = `
      <svg width="40px" height="40px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M19 9.77794V15M5 15V9.77728M21 11.9998L15.5668 5.96381C14.3311 4.59104 13.7133 3.90466 12.9856 3.65126C12.3466 3.4287 11.651 3.42875 11.0119 3.65141C10.2843 3.90491 9.66661 4.59139 8.43114 5.96433L3 11.9998M3 20.0048C3 20.0048 3.69422 18.8856 4.8 19.0096C6.06078 19.151 7.13275 21 8.4 21C9.66725 21 10.7327 19.0096 12 19.0096C13.2673 19.0096 14.3327 21 15.6 21C16.8672 21 17.9392 19.151 19.2 19.0096C20.3058 18.8856 21 20.0048 21 20.0048M10 11H14V15H10V11Z" stroke="#fff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </path>
      </svg>
    `;

    this.container.setAttribute('href', '/');

    // Classes
    this.container.classList.add('horizontal-block');
    this.svg_container.classList.add('horizontal-icon');

    // Style and content
    const styleLinker = document.createElement('link');
    styleLinker.rel = 'stylesheet';
    styleLinker.href = '/src/component/single/home-button/home-button.css';

    // Append
    shadow.appendChild(styleLinker);
    shadow.appendChild(this.container);
    this.container.appendChild(this.svg_container);

  }
}

// Define the custom element
customElements.define('home-button', HomeButton);


/*
<home-button></home-button>
*/