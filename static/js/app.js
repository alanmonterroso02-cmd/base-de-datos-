class EcoAPI {
  static BASE_URL = "http://localhost:8000";

  static getToken() {
    return document.cookie
      .split("; ")
      .find((r) => r.startsWith("token="))
      ?.split("=")[1];
  }

  static authHeaders() {
    const token = this.getToken();
    return token ? { Authorization: "Bearer " + token } : {};
  }

  static async get(url) {
    const res = await fetch(this.BASE_URL + url, {
      headers: this.authHeaders(),
    });
    if (res.status === 401) {
      window.location.href = "/login";
      return null;
    }
    if (!res.ok) {
      const data = await res.json().catch(() => ({}));
      throw new Error(data.detail || `Error ${res.status}`);
    }
    return res.json();
  }

  static async post(url, body, contentType) {
    const headers = { ...this.authHeaders() };
    if (contentType) {
      headers["Content-Type"] = contentType;
    } else if (
      body &&
      typeof body === "object" &&
      !(body instanceof FormData)
    ) {
      headers["Content-Type"] = "application/json";
      body = JSON.stringify(body);
    }
    const res = await fetch(this.BASE_URL + url, {
      method: "POST",
      headers,
      body,
    });
    if (res.status === 401) {
      window.location.href = "/login";
      return null;
    }
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.detail || `Error ${res.status}`);
    return data;
  }

  static async put(url, body) {
    const headers = {
      ...this.authHeaders(),
      "Content-Type": "application/json",
    };
    const res = await fetch(this.BASE_URL + url, {
      method: "PUT",
      headers,
      body: body ? JSON.stringify(body) : undefined,
    });
    if (res.status === 401) {
      window.location.href = "/login";
      return null;
    }
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.detail || `Error ${res.status}`);
    return data;
  }

  static async del(url) {
    const res = await fetch(this.BASE_URL + url, {
      method: "DELETE",
      headers: this.authHeaders(),
    });
    if (res.status === 401) {
      window.location.href = "/login";
      return null;
    }
    if (!res.ok) {
      const data = await res.json().catch(() => ({}));
      throw new Error(data.detail || `Error ${res.status}`);
    }
    return res.json().catch(() => null);
  }
}

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
