class Loader extends HTMLElement {
  constructor() {
    super();

    // Create shadow DOM
    const shadow = this.attachShadow({ mode: 'open' });

    // Elements
    this.container = document.createElement('div');

    // Attributes
    this.container.innerHTML = `
      <div class="psoload">
        <div class="hexagon">&#x2B22;</div>
        <div class="center"></div>
        <div class="inner"></div>
      </div>
    `;

    // Classes
    this.container.classList.add('screen');

    // Style and content
    const styleLinker = document.createElement('link');
    styleLinker.rel = 'stylesheet';
    styleLinker.href = '/src/component/single/loader-screen/loader-screen.css';

    // Append
    shadow.appendChild(styleLinker);
    shadow.appendChild(this.container);
  }

  remove () {
    this.container.classList.add('fall-out');
    setTimeout(() => {
      this.container.style.display = 'none';
    }, 1000);
  }
}

// Define the custom element
customElements.define('loader-screen', Loader);

/*
<loader-screen></loader-screen>
*/