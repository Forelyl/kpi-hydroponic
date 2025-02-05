class Line extends HTMLElement {
  constructor() {
    super();
    const shadow = this.attachShadow({ mode: 'open' });

    // elements
    this.line_container = document.createElement('div');
    this.triangle = document.createElement('img');
    this.vertical_line = document.createElement('div');
    this.circle = document.createElement('div');

    this.inputs_container = document.createElement('div');

    this.input_group1     = document.createElement('div');
    this.top_input_group1 = document.createElement('div');
    this.icon1            = document.createElement('img');
    this.label1           = document.createElement('label');
    this.line1            = document.createElement('div');
    this.input1           = document.createElement('input');

    this.input_group2     = document.createElement('div');
    this.top_input_group2 = document.createElement('div');
    this.icon2            = document.createElement('img');
    this.label2           = document.createElement('label');
    this.line2            = document.createElement('div');
    this.input2           = document.createElement('input');

    this.input_group3     = document.createElement('div');
    this.top_input_group3 = document.createElement('div');
    this.icon3            = document.createElement('img');
    this.label3           = document.createElement('label');
    this.line3            = document.createElement('div');
    this.input3           = document.createElement('input');

    // Classes
    this.line_container.classList.add('line-container');
    this.triangle.classList.add('triangle');
    this.vertical_line.classList.add('vertical-line');
    this.circle.classList.add('circle');

    this.inputs_container.classList.add('inputs-container');

    this.input_group1.classList.add('input-group');
    this.input_group2.classList.add('input-group');
    this.input_group3.classList.add('input-group');

    this.top_input_group1.classList.add('top-input-group');
    this.top_input_group2.classList.add('top-input-group');
    this.top_input_group3.classList.add('top-input-group');

    this.icon1.classList.add('input-icon');
    this.icon2.classList.add('input-icon');
    this.icon3.classList.add('input-icon');

    this.label1.classList.add('input-label');
    this.label2.classList.add('input-label');
    this.label3.classList.add('input-label');

    this.line1.classList.add('input-line');
    this.line2.classList.add('input-line');
    this.line3.classList.add('input-line');

    this.input1.classList.add('input');
    this.input2.classList.add('input');
    this.input3.classList.add('input');

    this.input1.id = 'input1';
    this.input2.id = 'input2';
    this.input3.id = 'input3';

    // Atributes
    this.input1.placeholder = 'Enter float point number';
    this.input2.placeholder = 'Enter text';
    this.input3.placeholder = 'Enter email';

    this.id1 = this.getAttribute('id1') || '1'; // to specify input in get value
    this.id2 = this.getAttribute('id2') || '2';
    this.id3 = this.getAttribute('id3') || '3';

    this.label1.textContent = this.getAttribute('label1') || '';
    this.label2.textContent = this.getAttribute('label2') || '';
    this.label3.textContent = this.getAttribute('label3') || '';

    this.label1.setAttribute('for', 'input1');
    this.label2.setAttribute('for', 'input2');
    this.label3.setAttribute('for', 'input3');

    this.triangle.src = '/public/Triangle.svg';

    this.icon1.src = '/public/Field.svg';
    this.icon2.src = '/public/Field.svg';
    this.icon3.src = '/public/Field.svg';

    this.type1 = this.getAttribute('type1') || 'text';
    this.type2 = this.getAttribute('type2') || 'text';
    this.type3 = this.getAttribute('type3') || 'text';

    this.setupInputTypes();
    this.hideEmpty();

    // Style
    const styleLinker = document.createElement('link');
    styleLinker.rel = 'stylesheet';
    styleLinker.href = '/src/component/single/trio-input/trio-input.css';

    // Append
    shadow.appendChild(styleLinker);
    shadow.appendChild(this.line_container);
    this.line_container.appendChild(this.triangle);
    this.line_container.appendChild(this.vertical_line);
    this.line_container.appendChild(this.circle);

    shadow.appendChild(this.inputs_container);

    this.inputs_container.appendChild(this.input_group1);
    this.inputs_container.appendChild(this.input_group2);
    this.inputs_container.appendChild(this.input_group3);

    this.input_group1.appendChild(this.top_input_group1);
    this.input_group2.appendChild(this.top_input_group2);
    this.input_group3.appendChild(this.top_input_group3);

    this.top_input_group1.appendChild(this.icon1);
    this.top_input_group1.appendChild(this.input1);
    this.input_group1.appendChild(this.line1);
    this.input_group1.appendChild(this.label1);

    this.top_input_group2.appendChild(this.icon2);
    this.top_input_group2.appendChild(this.input2);
    this.input_group2.appendChild(this.line2);
    this.input_group2.appendChild(this.label2);

    this.top_input_group3.appendChild(this.icon3);
    this.top_input_group3.appendChild(this.input3);
    this.input_group3.appendChild(this.line3);
    this.input_group3.appendChild(this.label3);
  }

  hideEmpty() {
    if (this.label1.textContent === '') {
      this.input_group1.style.display = 'none';
      this.type1 = "undefined-type";
    }
    if (this.label2.textContent === '') {
      this.input_group2.style.display = 'none';
      this.type2 = "undefined-type";
    }
    if (this.label3.textContent === '') {
      this.input_group3.style.display = 'none';
      this.type3 = "undefined-type";
    }
  }

  setupInputTypes() {
    this.input1.type = this.type1;
    this.input2.type = this.type2;
    this.input3.type = this.type3;

    const dict_of_inputs = {
      "text": {
        "input_type": "text",
        "input_placeholder": "Enter text",
        "validator": Line.textValidator,
        "property_setter": (object) => {}
      },
      "float": {
        "input_type": "number",
        "input_placeholder": "Enter float point number",
        "validator": Line.floatValidator,
        "property_setter": Line.floatPropertySetter
      },
      "ufloat": {
        "input_type": "number",
        "input_placeholder": "Enter non negative float point number",
        "validator": Line.ufloatValidator,
        "property_setter": (object) => { Line.floatPropertySetter(object, 0); }
      },
      "celsius": {
        "input_type": "number",
        "input_placeholder": "Enter celsius (from 5°C to 25°C)",
        "validator": (object) => { return Line.floatValidator(object, 5, 25); },
        "property_setter": (object) => { Line.floatPropertySetter(object, 5, 25); }
      },
      "acidness": {
        "input_type": "number",
        "input_placeholder": "Enter acidity (from 0.0 to 14.0)",
        "validator": (object) => { return Line.floatValidator(object, 0, 14); },
        "property_setter": (object) => { Line.floatPropertySetter(object, 0, 14); }
      },
      "percentage": {
        "input_type": "number",
        "input_placeholder": "Enter percentage (from 0% to 100%)",
        "validator": (object) => { return Line.floatValidator(object, 0, 100); },
        "property_setter": (object) => { Line.floatPropertySetter(object, 0, 100); }
      },
      "undefined-type": {
        "input_type": "WEB-error",
        "input_placeholder": "WEB-error",
        "validator": (object) => { return true; },
        "property_setter": (object) => {}
      }
    };

    // check if types are in dictionary
    if (!this.type1 in dict_of_inputs) {
      this.type1 = "text";
      console.error("Type 1 is not in dictionary");
    }
    if (!this.type2 in dict_of_inputs) {
      this.type2 = "text";
      console.error("Type 2 is not in dictionary");
    }
    if (!this.type3 in dict_of_inputs) {
      this.type3 = "text";
      console.error("Type 3 is not in dictionary");
    }


    this.input1.type        = dict_of_inputs[this.type1].input_type;
    this.input1.placeholder = dict_of_inputs[this.type1].input_placeholder;
    this.input1.oninput     = (e) => { Line.ValidateFunction(    dict_of_inputs[this.type1].validator, this.input1); };
    this.input1.onblur      = (e) => { Line.blurValidateFunction(dict_of_inputs[this.type1].validator, this.input1); };
    dict_of_inputs[this.type1].property_setter(this.input1);

    this.input2.type        = dict_of_inputs[this.type2].input_type;
    this.input2.placeholder = dict_of_inputs[this.type2].input_placeholder;
    this.input2.oninput     = () => { Line.ValidateFunction(    dict_of_inputs[this.type2].validator, this.input2); };
    this.input2.onblur      = () => { Line.blurValidateFunction(dict_of_inputs[this.type2].validator, this.input2); };
    dict_of_inputs[this.type2].property_setter(this.input2);

    this.input3.type        = dict_of_inputs[this.type3].input_type;
    this.input3.placeholder = dict_of_inputs[this.type3].input_placeholder;
    this.input3.oninput     = () => { Line.ValidateFunction(    dict_of_inputs[this.type3].validator, this.input3); };
    this.input3.onblur      = () => { Line.blurValidateFunction(dict_of_inputs[this.type3].validator, this.input3); };
    dict_of_inputs[this.type3].property_setter(this.input3);

  }

  static blurValidateFunction(validator, object) {
    let is_validated = validator(object);
    if (!is_validated) {
      object.reportValidity();
      object.classList.add('invalid');
    }
  }

  static ValidateFunction(validator, object) {
    let is_validated = validator(object);
    if (is_validated) {
      object.classList.remove('invalid');
    }
    // if (!is_validated) this.reportValidity(); -- report on blur or accept (forced call)
  }

  // --- Properties setters ---
  static floatPropertySetter(object, min_value = -1000, max_value = 1000000) {
    object.min = min_value;
    object.max = max_value;

    object.step = "any";
  }


  // --- Validators ---

  static textValidator(object) {
    object.value = object.value.replace(/[^a-zA-Z0-9 ]/g, '').replace(/\s+/g, ' ');

    const maxLength = 120;
    if (object.value.length > maxLength) {
      object.value = object.value.substring(0, maxLength);
    }

    object.setCustomValidity('');
    return true;

    // if (object.value.length === 0) {
    //   object.setCustomValidity('Value cannot be empty');
    // } else {
    //   object.setCustomValidity('');
    //   return true;
    // }

  }

  static floatValidator(object, min_value = -1000, max_value = 1000000) {
    // if (object.value.length === 0) {
    //   object.setCustomValidity('Value cannot be empty');
    //   return false;
    // }


    if (isNaN(object.value)) {
      object.setCustomValidity('Value must be a number');
      return false;
    }

    let value = parseFloat(object.value);

    if (value < min_value) {
      object.setCustomValidity(`Value must be greater than ${min_value}`);
      return false;
    }

    if (value > max_value) {
      object.setCustomValidity(`Value must be less than ${max_value}`);
      return false;
    }

    object.setCustomValidity('');
    return true;
  }

  static ufloatValidator(object) {
    let is_validated = Line.floatValidator(object, 0, 1000000);
    if (!is_validated) return false;

    // post validation
    if (object.value === "0") {
      object.setCustomValidity('Value cannot be 0');
    } else {
      object.setCustomValidity('');
      return true;
    }
    return false;
  }



  // ---

  connectedCallback() {
    setTimeout(() => {
      const inputLine = this.shadowRoot.querySelectorAll('.input-line');
      for (let x of inputLine.values()) {
        x.classList.add('loaded');
      }
    }, 50);
  }

  // ---

  checkValid() {
    this.input1.oninput();
    if (!this.input1.reportValidity()) return false;

    this.input2.oninput();
    if (!this.input2.reportValidity()) return false;

    this.input3.oninput();
    if (!this.input3.reportValidity()) return false;

    // check is empty
    if (this.type1 != "undefined-type" && this.input1.value.length === 0) {
      this.input1.setCustomValidity('Value cannot be empty');
      this.input1.reportValidity()
      return false;
    }
    if (this.type2 != "undefined-type" && this.input2.value.length === 0) {
      this.input2.setCustomValidity('Value cannot be empty');
      this.input2.reportValidity()
      return false;
    }
    if (this.type3 != "undefined-type" && this.input3.value.length === 0) {
      this.input3.setCustomValidity('Value cannot be empty');
      this.input3.reportValidity()
      return false;
    }

    return true;
  }

  static getParseValue(input, type) {
    const float_types = ['float', 'ufloat', 'celsius', 'acidness', 'percentage'];
    if (float_types.includes(type)) {
      return parseFloat(input.value);
    }
    return input.value;
  }

  getValues() {
    if (!this.checkValid()) return null;
    let result = {};
    if (this.type1 != "undefined-type") result[this.id1] = Line.getParseValue(this.input1, this.type1);
    if (this.type2 != "undefined-type") result[this.id2] = Line.getParseValue(this.input2, this.type2);
    if (this.type3 != "undefined-type") result[this.id3] = Line.getParseValue(this.input3, this.type3);
    return result;
  }

}

// Register the Custom Element
customElements.define('trio-input', Line);