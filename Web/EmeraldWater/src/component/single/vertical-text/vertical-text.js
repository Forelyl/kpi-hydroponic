class VerticalText extends HTMLElement {
  constructor() {
    super();

    // Create shadow DOM
    const shadow = this.attachShadow({ mode: 'open' });

    // Elements
    this.container      = document.createElement('div');
    this.text_line      = document.createElement('div');
    this.text           = document.createElement('div');
    this.icon           = document.createElement('img');
    this.line           = document.createElement('div');

    // Update
    this.connectedCallback();

    // Classes
    this.container.classList.add('vertical-block');
    this.text_line.classList.add('vertical-text-line');
    this.text.classList.add('vertical-text');
    this.icon.classList.add('vertical-icon');
    this.line.classList.add('vertical-line');

    // Style and content
    const styleLinker = document.createElement('link');
    styleLinker.rel = 'stylesheet';
    styleLinker.href = '/src/component/single/vertical-text/vertical-text.css';

    // Attributes
    this.icon.setAttribute('src', '/public/Leaves.svg');

    // Append
    shadow.appendChild(styleLinker);
    shadow.appendChild(this.container);
    this.container.appendChild(this.text_line);
    this.text_line.appendChild(this.text);
    this.text_line.appendChild(this.icon);
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

    this.text.textContent = text;
    this.text.style.color = textColor;
  }
}

// Define the custom element
customElements.define('vertical-text', VerticalText);


/*
<vertical-text
  text="Smart Hydroponic XarmM12"
  text-color="#D9D9D9"
></vertical-text>
*/