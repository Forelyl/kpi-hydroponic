class MainHeader extends HTMLElement {
    constructor() {
      super();

      // Create shadow DOM
      const shadow = this.attachShadow({ mode: 'open' });

      // Elements
      this.container      = document.createElement('div');
      this.icon_container = document.createElement('div');
      this.icon           = document.createElement('img');
      this.header_title   = document.createElement('h1');

      // Attributes
      this.icon.src               = '/public/New.svg';
      this.header_title.innerHTML = '<span>Emerald</span>Water';

      // Classes
      this.container.classList.add('container');
      this.icon_container.classList.add('icon-container');
      this.icon.classList.add('icon');
      this.header_title.classList.add('header-title');

      // Style and content
      const styleLinker = document.createElement('link');
      styleLinker.rel = 'stylesheet';
      styleLinker.href = '/src/component/single/main-header/main-header.css';

      // Append
      shadow.appendChild(styleLinker);
      shadow.appendChild(this.container);
      this.container.appendChild(this.icon_container);
      this.icon_container.appendChild(this.icon);
      this.container.appendChild(this.header_title);


    }
  }

  // Define the custom element
  customElements.define('main-header', MainHeader);


  /*
  <main-header></main-header>
  */