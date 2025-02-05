class ProgressBar extends HTMLElement {
  constructor() {
    super();
    const shadow = this.attachShadow({ mode: 'open' });

    // Attributes
    const value      = this.getAttribute('value') || '';
    const percentage = parseFloat(this.getAttribute('percentage')) || 0;
    const bgColor    = this.getAttribute('bg-color') || 'red';
    const img        = this.getAttribute('img') || '';

    /**
     container -> icon, filler, text
     */
    // Elements
    this.container = document.createElement('div');
    this.icon = document.createElement('img');
    this.filler = document.createElement('div');
    this.text = document.createElement('div');

    // Set data
    this.icon.src = img;
    this.icon.alt = 'Icon';
    this.icon.classList.add('card-icon');

    this.filler.style.backgroundColor = bgColor;
    this.filler.style.width = `${percentage}%`;

    this.text.textContent = value;

    // add classes
    this.container.classList.add('progress-container');
    this.icon.classList.add('progress-icon');
    this.filler.classList.add('progress-filler');
    this.text.classList.add('progress-text');

    // Make style
    const styleLinker = document.createElement('link');
    styleLinker.rel = 'stylesheet';
    styleLinker.href = '/src/component/single/progress-bar/progress-bar.css';

    // Structure
    shadow.appendChild(styleLinker);
    shadow.appendChild(this.container);
    this.container.appendChild(this.icon);
    this.container.appendChild(this.text);
    this.container.appendChild(this.filler);
  }

  static get observedAttributes() {
    return ['value', 'percentage', 'bg-color'];
  }

  attributeChangedCallback(name, oldValue, newValue) {
    switch (name) {
      case 'value':
        this.text.textContent = newValue;
        break;
      case 'percentage':
        this.filler.style.width = `${newValue}%`;
        break;
      case 'bg-color':
        this.filler.style.backgroundColor = newValue;
        break;
    }
  }
}

customElements.define('progress-bar', ProgressBar);

/*
<progress-bar
  value="82%"
  percentage="82"
  bg-color="#e57373"
  img="data/house-water-svgrepo-com.svg">
</progress-bar>
*/
