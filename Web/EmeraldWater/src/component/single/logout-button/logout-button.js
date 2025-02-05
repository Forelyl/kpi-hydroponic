class LogoutButton extends HTMLElement {
  constructor() {
    super();

    // Create shadow DOM
    const shadow = this.attachShadow({ mode: 'open' });

    // Elements
    this.container      = document.createElement('a');
    this.svg_container  = document.createElement('div');

    // Attributes
    this.svg_container.innerHTML = `
      <svg width="800px" height="800px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" stroke="#E9E9E9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 12L13 12"/>
        <path d="M18 15L20.913 12.087V12.087C20.961 12.039 20.961 11.961 20.913 11.913V11.913L18 9"/>
        <path d="M16 5V4.5V4.5C16 3.67157 15.3284 3 14.5 3H5C3.89543 3 3 3.89543 3 5V19C3 20.1046 3.89543 21 5 21H14.5C15.3284 21 16 20.3284 16 19.5V19.5V19"/>
      </svg>
    `;

    this.container.setAttribute('href', '/src/pages/logout/logout.html');

    // Classes
    this.container.classList.add('container');
    this.svg_container.classList.add('icon-container');

    // Style and content
    const styleLinker = document.createElement('link');
    styleLinker.rel = 'stylesheet';
    styleLinker.href = '/src/component/single/logout-button/logout-button.css';

    // Append
    shadow.appendChild(styleLinker);
    shadow.appendChild(this.container);
    this.container.appendChild(this.svg_container);

  }
}

// Define the custom element
customElements.define('logout-button', LogoutButton);


/*
<logout-button></logout-button>
*/