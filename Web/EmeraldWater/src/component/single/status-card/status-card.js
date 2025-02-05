class StatusCard extends HTMLElement {
  constructor() {
    super();

    /**
     container -> box | text
     box -> filler | icon
     */

     // Attach a shadow DOM
    const shadow = this.attachShadow({ mode: 'open' });

    // Define the template as a `<div>`
    this.container = document.createElement('div');
    this.box       = document.createElement('div');
    this.filler    = document.createElement('div');
    this.icon      = document.createElement('img');
    this.text      = document.createElement('div');

    // add classes
    this.container.classList.add('icon-block-container');
    this.box.classList.add('visual-container');
    this.filler.classList.add('filler');
    this.icon.classList.add('icon');
    this.text.classList.add('text');

    // Update
    this.connectedCallback();

    // Make style
    const styleLinker = document.createElement('link');
    styleLinker.rel = 'stylesheet';
    styleLinker.href = '/src/component/single/status-card/status-card.css';

    // Append elements
    shadow.appendChild(styleLinker);
    shadow.appendChild(this.container);
    this.container.appendChild(this.box);
    this.container.appendChild(this.text);
    this.box.appendChild(this.filler);
    this. box.appendChild(this.icon);
  }

  connectedCallback() {
      // Get data
      let value = this.getAttribute('value') || '';
      let percentage = parseFloat(this.getAttribute('percentage')) || 0;
      let bgColor = this.getAttribute('bg-color') || 'red';
      let img = this.getAttribute('img') || '';

      // Set data
      this.filler.style.height = `${percentage}%`;
      this.filler.style.backgroundColor = bgColor;

      this.icon.src = img;
      this.icon.alt = 'Icon';

      this.text.innerText = value;
  }

  static get observedAttributes() {
    return ['value', 'percentage', 'bg-color'];
  }

  attributeChangedCallback(name, oldValue, newValue) {
    this.connectedCallback();
  }

}

// Define the custom element
customElements.define('status-card', StatusCard);

/*
<status-card
  percentage="50"
  value="83%"
  img="data/house-water-svgrepo-com.svg"
  bg-color="#e57373"
></status-card>
*/