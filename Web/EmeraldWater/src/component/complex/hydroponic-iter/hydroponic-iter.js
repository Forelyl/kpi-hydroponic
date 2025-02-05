class HydroponicIter extends HTMLElement {
    // so - solid
  constructor() {
    super();
    const shadow = this.attachShadow({ mode: 'open' });

    // Elements
    this.container        = document.createElement('a');

    this.header           = document.createElement('vertical-text');
    this.body             = document.createElement('div');
    this.end_line         = document.createElement('horizontal-space-line');

    this.main_solid_bar   = document.createElement('solid-progress-bar');
    this.statuses_wrapper = document.createElement('div');
    this.status_card1     = document.createElement('status-card');
    this.status_card2     = document.createElement('status-card');
    this.status_card3     = document.createElement('status-card');
    this.status_card4     = document.createElement('status-card');
    this.status_message   = document.createElement('status-box');

    // Attributes
    this.connectedCallback();

    // Classes
    this.container.classList.add('container');
    this.header.classList.add('header');
    this.body.classList.add('body');
    this.end_line.classList.add('end-line');

    this.main_solid_bar.classList.add('main-solid-bar');
    this.statuses_wrapper.classList.add('statuses-wrapper');
    this.status_card1.classList.add('status-card1');
    this.status_card2.classList.add('status-card2');
    this.status_card3.classList.add('status-card3');
    this.status_card3.classList.add('status-card4');
    this.status_message.classList.add('status-message');

    // Style
    const styleLinker = document.createElement('link');
    styleLinker.rel = 'stylesheet';
    styleLinker.href = '/src/component/complex/hydroponic-iter/hydroponic-iter.css';

    // JS imports
    this.loadJSModules();

    // Append
    shadow.appendChild(styleLinker);
    shadow.appendChild(this.container);
    // shadow.appendChild(this.end_line);
    this.container.appendChild(this.header);
    this.container.appendChild(this.body);

    this.body.appendChild(this.main_solid_bar);
    this.body.appendChild(this.statuses_wrapper);
    this.body.appendChild(this.status_message);

    this.statuses_wrapper.appendChild(this.status_card1);
    this.statuses_wrapper.appendChild(this.status_card2);
    this.statuses_wrapper.appendChild(this.status_card3);
    this.statuses_wrapper.appendChild(this.status_card4);


    // Event listeners
    this.text_color =  this.header.getAttribute('text-color') || '#E9E9E9'; // const value to be used on unhover

    this.container.addEventListener('mouseenter', () => {
      this.header.setAttribute('text-color', "#000");
    });

    this.container.addEventListener('mouseleave', () => {
      this.header.setAttribute('text-color', this.text_color);
    });

  }

  async loadJSModules() {
    try {
      await import('/src/component/single/progress-bar/progress-bar.js');
      await import('/src/component/single/status-card/status-card.js');
      await import('/src/component/single/solid-progress-bar/solid-progress-bar.js');
      await import('/src/component/single/status-box/status-box.js');
      await import('/src/component/single/vertical-text/vertical-text.js');
    } catch (error) {
      console.error('Error loading JS modules:', error);
    }
  }

  connectedCallback() {
    // get attributes
    const name                  = this.getAttribute('name') || '';

    const bgColorMain           = this.getAttribute('bg-color-main') || 'red';
    const bgColorSecondary_1    = this.getAttribute('bg-color-secondary1') || 'red';
    const bgColorSecondary_2    = this.getAttribute('bg-color-secondary2') || 'red';
    const bgColorSecondary_3    = this.getAttribute('bg-color-secondary3') || 'red';
    const bgColorSecondary_4    = this.getAttribute('bg-color-secondary4') || 'red';

    const main_value_volume     = this.getAttribute('main-value-volume') || 0;
    const main_value_percentage = parseFloat(this.getAttribute('main-value-percentage')) || 0;
    const main_sub_value        = this.getAttribute('main-sub-value') || 0;

    const sub_value1_volume     = this.getAttribute('sub-value1-volume') || 0;
    const sub_value1_percentage = parseFloat(this.getAttribute('sub-value1-percentage')) || 0;

    const sub_value2_volume     = this.getAttribute('sub-value2-volume') || 0;
    const sub_value2_percentage = parseFloat(this.getAttribute('sub-value2-percentage')) || 0;

    const sub_value3_volume     = this.getAttribute('sub-value3-volume') || 0;
    const sub_value3_percentage = parseFloat(this.getAttribute('sub-value3-percentage')) || 0;

    const sub_value4_volume     = this.getAttribute('sub-value4-volume') || 0;
    const sub_value4_percentage = parseFloat(this.getAttribute('sub-value4-percentage')) || 0;

    const status_code           = this.getAttribute('status-code') || '';
    const status_text           = this.getAttribute('status-text') || '';
    const status_color          = this.getAttribute('status-color') || 'black';

    // set attributes
    this.header.setAttribute('text', name);

    this.main_solid_bar.setAttribute('bg-color', bgColorMain);
    this.main_solid_bar.setAttribute('value', main_value_volume);
    this.main_solid_bar.setAttribute('percentage', main_value_percentage);
    this.main_solid_bar.setAttribute('upper-float-text', main_sub_value);

    this.status_card1.setAttribute('value', sub_value1_volume);
    this.status_card1.setAttribute('percentage', sub_value1_percentage);
    this.status_card1.setAttribute('bg-color', bgColorSecondary_1);
    this.status_card1.setAttribute('img', '/public/Minerals.svg');

    this.status_card2.setAttribute('value', sub_value2_volume);
    this.status_card2.setAttribute('percentage', sub_value2_percentage);
    this.status_card2.setAttribute('bg-color', bgColorSecondary_2);
    this.status_card2.setAttribute('img', '/public/Temperature.svg');

    this.status_card3.setAttribute('value', sub_value3_volume);
    this.status_card3.setAttribute('percentage', sub_value3_percentage);
    this.status_card3.setAttribute('bg-color', bgColorSecondary_3);
    this.status_card3.setAttribute('img', '/public/Acidness.svg');

    this.status_card4.setAttribute('value', sub_value4_volume);
    this.status_card4.setAttribute('percentage', sub_value4_percentage);
    this.status_card4.setAttribute('bg-color', bgColorSecondary_4);
    this.status_card4.setAttribute('img', '/public/Oxygen.svg');


    this.status_message.setAttribute('status', status_code);
    this.status_message.setAttribute('description', status_text);
    this.status_message.setAttribute('status-color', status_color);

    this.end_line.setAttribute('len', '40');

    // -----

    const link =  this.getAttribute('link');
    if (link !== null) {
      this.container.setAttribute('href', link);
    } else {
      this.container.setAttribute('href', '');
    }

  }

  static get observedAttributes() {
    return [
      "name",
      "bg-color-main", "bg-color-secondary1", "bg-color-secondary2", "bg-color-secondary3", "bg-color-secondary4",
      "main-value-volume", "main-value-percentage", "main-sub-value",
      "sub-value1-volume", "sub-value1-percentage",
      "sub-value2-volume", "sub-value2-percentage",
      "sub-value3-volume", "sub-value3-percentage",
      "sub-value4-volume", "sub-value4-percentage",
      "status-code", "status-text", "status-color"
    ]
  }

  attributeChangedCallback(name, oldValue, newValue) {
    switch(name) {
      case 'name':
        this.header.setAttribute('text', newValue);
        break;

      case 'bg-color-main':
        this.main_solid_bar.setAttribute('bg-color', newValue);
        break;
      case 'bg-color-secondary1':
        this.status_card1.setAttribute('bg-color', newValue);
        break;
      case 'bg-color-secondary2':
        this.status_card2.setAttribute('bg-color', newValue);
        break;
      case 'bg-color-secondary3':
        this.status_card3.setAttribute('bg-color', newValue);
        break;
      case 'bg-color-secondary4':
        this.status_card4.setAttribute('bg-color', newValue);
        break;

      case 'main-value-volume':
        this.main_solid_bar.setAttribute('value', newValue);
        break;
      case 'main-value-percentage':
        this.main_solid_bar.setAttribute('percentage', newValue);
        break;
      case 'main-sub-value':
        this.main_solid_bar.setAttribute('upper-float-text', newValue);
        break;

      case 'sub-value1-volume':
        this.status_card1.setAttribute('value', newValue);
        break;
      case 'sub-value1-percentage':
        this.status_card1.setAttribute('percentage', newValue);
        break;

      case 'sub-value2-volume':
        this.status_card2.setAttribute('value', newValue);
        break;
      case 'sub-value2-percentage':
        this.status_card2.setAttribute('percentage', newValue);
        break;

      case 'sub-value3-volume':
        this.status_card3.setAttribute('value', newValue);
        break;
      case 'sub-value3-percentage':
        this.status_card3.setAttribute('percentage', newValue);
        break;

      case 'sub-value4-volume':
        this.status_card4.setAttribute('value', newValue);
        break;
      case 'sub-value4-percentage':
        this.status_card4.setAttribute('percentage', newValue);
        break;


      case 'status-code':
        this.status_message.setAttribute('status', newValue);
        break;
      case 'status-text':
        this.status_message.setAttribute('description', newValue);
        break;
      case 'status-color':
        this.status_message.setAttribute('status-color', newValue);
        break;
    }
  }
}

  // Register custom element
  customElements.define('hydroponic-iter', HydroponicIter);
