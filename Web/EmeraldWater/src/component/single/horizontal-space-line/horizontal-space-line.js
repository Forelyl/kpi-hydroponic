class Line extends HTMLElement {
    constructor() {
        super();
        this.shadow = this.attachShadow({ mode: 'open' });
        this.connectedCallback();

    }
    connectedCallback() {
        let len = parseInt(this.getAttribute('len')) | 0;
        len = Math.max(Math.min(len, 100), 0);

        this.shadow.innerHTML = `
        <style>
        :host {
            display: flex;
            height: 4vw;
            width: 100%;
            align-items: center;
            justify-content: center;
            margin: 3vh 0;
        }
        .rule {
            height: 0.4vw;
            background: #E9E9E9;
            width: ${len}%;
            height: 0.4vw;
        }
        .rule:before, .rule:after {
            content: '';
            height: 2vw;
            width: 2vw;
            border-radius: 2vw;
            float: left;
            background: #E9E9E9;
            margin-top: -0.8vw;
            margin-left: -1vw;
        }
        .rule:after {
            float: right;
            margin-right: -1vw;
        }
        </style>
        <div class="rule"></div>
        `;
    }
}

// Register the Custom Element
customElements.define('horizontal-space-line', Line);

/*
<line-with-ends
  len="50"
></line-with-ends>
*/