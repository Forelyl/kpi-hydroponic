class SolidProgressBar extends HTMLElement {

  constructor() {
    super();
    const shadow = this.attachShadow({ mode: 'open' });

    // Elements
    this.container      = document.createElement('div');
    this.floating_text  = document.createElement('div');

    this.icon_curtain   = document.createElement('div');
    this.icon_container = document.createElement('div');
    this.icon_filler    = document.createElement('div');
    this.icon           = document.createElement('img');

    this.text           = document.createElement('span');
    this.bar_wrapper    = document.createElement('div');
    this.bar            = document.createElement('div');
    this.filler         = document.createElement('div');

    // Classes
    this.container.classList.add('solid-container');
    this.floating_text.classList.add('solid-floating-text');
    this.icon_container.classList.add('solid-icon-container');
    this.icon_filler.classList.add('solid-icon-filler');
    this.icon_curtain.classList.add('solid-icon-curtain');
    this.icon.classList.add('solid-icon');
    this.bar.classList.add('solid-bar');
    this.bar_wrapper.classList.add('solid-bar-wrapper');
    this.filler.classList.add('solid-filler');
    this.text.classList.add('solid-text');

    // Atribute
    this.connectedCallback();
    this.icon.src = '/public/solid-bar-header.svg';
    this.icon.alt = 'Icon';

    // Style
    const styleLinker = document.createElement('link');
    styleLinker.rel = 'stylesheet';
    styleLinker.href = '/src/component/single/solid-progress-bar/solid-progress-bar.css';

    // Append
    shadow.appendChild(styleLinker);
    shadow.appendChild(this.container);

    this.container.appendChild(this.icon_container);
    this.container.appendChild(this.bar);

    this.icon_container.appendChild(this.icon);
    this.icon_container.appendChild(this.icon_filler);
    this.icon_container.appendChild(this.icon_curtain);

    this.bar.appendChild(this.floating_text);
    this.bar.appendChild(this.bar_wrapper);
    this.bar_wrapper.appendChild(this.text);
    this.bar_wrapper.appendChild(this.filler);
  }

  connectedCallback() {
    // const
    const so_filler_h = 80.0; // %
    const so_filler_to_input_width = so_filler_h / 100.0; // coeficient

    // Update
    const value            = this.getAttribute('value') || '';
    const percentage       = parseFloat(this.getAttribute('percentage')) || 0;
    const bgColor          = this.getAttribute('bg-color') || '#ccc';
    const upper_float_text = this.getAttribute('upper-float-text') || '';

    // evaluate tube filler properties
    let icon_filler_height = percentage * so_filler_to_input_width;
    let filler_height;
    if (icon_filler_height < 20) {
      filler_height = 0;
    } else if (icon_filler_height > 60) {
      filler_height = 100;
    } else {
      filler_height = (icon_filler_height - 20) * 2.5; // 2.5 = 100 / 40
    }

    // Attributes
    this.filler.style.height = `${filler_height}%`;
    this.filler.style.backgroundColor = bgColor;

    this.icon_curtain.style.top = `-${icon_filler_height + 10}%`;
    this.icon_filler.style.backgroundColor = bgColor;

    this.floating_text.textContent = upper_float_text;
    this.floating_text.style.color = bgColor;

    this.text.textContent = value;
  }

  static get observedAttributes() {
    return ['value', 'percentage', 'bg-color', 'upper-float-text'];
  }

  attributeChangedCallback(name, oldValue, newValue) {
    switch (name) {
      case 'value':
        this.text.textContent = newValue;
        break;
      case 'percentage':
        this.connectedCallback();
        break;
      case 'bg-color':
        this.filler.style.backgroundColor = newValue;
        this.floating_text.style.color = newValue;
        this.icon_filler.style.backgroundColor = newValue;
        break;
      case 'upper-float-text':
        this.floating_text.textContent = newValue;
        break;
    }
  }
}



// Register custom element
customElements.define('solid-progress-bar', SolidProgressBar);

/*
<solid-progress-bar
  value="82%"
  percentage="50"
  bg-color="#ff2299"
  upper-float-text="1200ml"
></solid-progress-bar>
*/