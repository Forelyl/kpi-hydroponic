class HorizontalText extends HTMLElement {
  constructor() {
    super();

    // Create shadow DOM
    const shadow = this.attachShadow({ mode: 'open' });

    // Elements
    this.container      = document.createElement('div');
    this.text           = document.createElement('div');
    this.icon           = document.createElement('img');
    this.line           = document.createElement('div');

    // Attributes
    this.connectedCallback();
    this.icon.src = '/public/Leaves.svg';

    // Classes
    this.container.classList.add('horizontal-block');
    this.text.classList.add('horizontal-text');
    this.icon.classList.add('horizontal-icon');
    this.line.classList.add('horizontal-line');

    // Style and content
    const styleLinker = document.createElement('link');
    styleLinker.rel = 'stylesheet';
    styleLinker.href = '/src/component/single/horizontal-text/horizontal-text.css';

    // Append
    shadow.appendChild(styleLinker);
    shadow.appendChild(this.container);
    this.container.appendChild(this.text);
    this.container.appendChild(this.icon);
    this.container.appendChild(this.line);
  }

  connectedCallback() {
    this.text.innerText = this.getAttribute('text') || '';
    this.text.style.color = this.getAttribute('text-color') || '#E9E9E9';
  }

  static get observedAttributes() {
    return ['text', 'text-color'];
  }


  attributeChangedCallback(name, oldValue, newValue) {
    if (oldValue !== newValue) {
      this.updateContent();
    }
  }

    // Update content and styles dynamically
  updateContent() {
    const text = this.getAttribute('text') || '';
    const textColor = this.getAttribute('text-color') || '#000';

    const shadow = this.shadowRoot;
    this.text.textContent = text;
    this.text.style.color = textColor;

  }
}

// Define the custom element
customElements.define('horizontal-text', HorizontalText);


/*
<horizontal-text
  text="Smart Hydroponic XarmM12"
  text-color="#D9D9D9"
></horizontal-text>
*/