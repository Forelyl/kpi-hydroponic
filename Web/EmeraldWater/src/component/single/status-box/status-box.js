class StatusBox extends HTMLElement {
    constructor() {
      super();

      // Attach shadow DOM
      const shadow = this.attachShadow({ mode: "open" });

      // Create container
      this.outer_container = document.createElement("div");
      this.outer_container.classList.add("outer-container");

      this.container = document.createElement("div");
      this.container.classList.add("status-container");

      // Update
      this.connectedCallback();

      // Add styles
      const styles = document.createElement("style");
      styles.textContent = `
        .outer-container {
          width: 100%;
          padding: 1vw;
          background-color: white;
          border: 3px dashed black;
          border-radius: 1vw;
        }

        .status-container {
          width: calc(100% - 6.5vw);
          border-radius: 1vw;
          border: 3px solid black;
          text-align: center;
          font-family: Inconsolata, sans-serif;
          font-size: 3vw;
          line-height: 3vw;
          font-weight: bold;
          padding: 2vw 3vw;
          display: inline-block;
        }

        .status {
          font-weight: bold;
        }

        .label {
          color: #09cfbfef;
        }

        .description {
          font-weight: normal;
        }
      `;

      // Append
      shadow.appendChild(styles);
      shadow.appendChild(this.outer_container);
      this.outer_container.appendChild(this.container);
    }

    connectedCallback() {
      // Get attributes
      const status = this.getAttribute("status") || "Unknown";
      let description = this.getAttribute("description");
      if (description === null) {
        description = "";
      } else {
        description = " - " + description
      }
      const statusColor = this.getAttribute("status-color") || "black";

      // Update
      // Make inner text
      this.container.innerHTML = `
        <span class="label">Status: </span>
        <span class="status" style="color: ${statusColor};">${status}</span>
        <span class="description">${description}</span>
      `;
    }

    static get observedAttributes() {
      return ["status", "description", "status-color"];
    }

    attributeChangedCallback(name, oldValue, newValue) {
      this.connectedCallback();
    }
  }

// Define the custom element
customElements.define("status-box", StatusBox);

/*
<status-box
  status="Danger"
  description="overinfused with minerals"
  status-color="red"
></status-box>
*/