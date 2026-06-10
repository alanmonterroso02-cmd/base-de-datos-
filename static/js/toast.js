class EcoToast {
  static container = null;

  static init() {
    if (this.container && document.getElementById("toast-template")) return;
    const existing = document.getElementById("toast-container");
    if (existing) {
      this.container = existing;
      if (!document.getElementById("toast-template")) {
        const template = document.createElement("template");
        template.innerHTML = `
          <div id="toast-template" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header">
              <i class="bi me-2" id="toast-icon"></i>
              <strong class="me-auto" id="toast-title"></strong>
              <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body" id="toast-body"></div>
          </div>`;
        existing.appendChild(template.content.firstElementChild);
      }
      return;
    }
    const div = document.createElement("div");
    div.className = "toast-container position-fixed bottom-0 end-0 p-3";
    div.id = "toast-container";
    div.style.zIndex = "9999";
    div.innerHTML = `
      <div id="toast-template" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
        <div class="toast-header">
          <i class="bi me-2" id="toast-icon"></i>
          <strong class="me-auto" id="toast-title"></strong>
          <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
        </div>
        <div class="toast-body" id="toast-body"></div>
      </div>`;
    document.body.appendChild(div);
    this.container = div;
  }

  static show(
    title,
    message,
    variant = "primary",
    icon = "bi-info-circle",
    delay = 4000,
  ) {
    this.init();
    const template = document.getElementById("toast-template");
    const clone = template.cloneNode(true);
    clone.id = "toast-" + Date.now();
    clone.querySelector("#toast-icon").className = `bi me-2 ${icon}`;
    clone.querySelector("#toast-title").textContent = title;
    clone.querySelector("#toast-body").textContent = message;
    clone.classList.add(`text-bg-${variant}`);
    document.getElementById("toast-container").appendChild(clone);
    const bsToast = new bootstrap.Toast(clone, { autohide: true, delay });
    bsToast.show();
    clone.addEventListener("hidden.bs.toast", () => clone.remove());
  }

  static success(message) {
    this.show("Éxito", message, "success", "bi-check-circle-fill");
  }

  static error(message) {
    this.show("Error", message, "danger", "bi-exclamation-triangle-fill");
  }

  static warning(message) {
    this.show("Advertencia", message, "warning", "bi-exclamation-circle-fill");
  }

  static info(message) {
    this.show("Información", message, "info", "bi-info-circle-fill");
  }
}
