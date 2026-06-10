class EcoAPI {
  static BASE_URL = window.location.origin;

  static getCookie(name) {
    return document.cookie
      .split("; ")
      .find((r) => r.startsWith(name + "="))
      ?.split("=")[1];
  }

  static getToken() {
    return this.getCookie("token");
  }

  static _redirectLogin() {
    const rol = this.getCookie("rol");
    if (rol === "Admin" || rol === "Colaborador") {
      window.location.href = "/login/colaborador";
    } else {
      window.location.href = "/login";
    }
  }

  static logout() {
    document.cookie = "token=; path=/; max-age=0; SameSite=Lax";
    document.cookie = "rol=; path=/; max-age=0; SameSite=Lax";
    this._redirectLogin();
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
      this._redirectLogin();
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
      this._redirectLogin();
      return null;
    }
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.detail || `Error ${res.status}`);
    return data;
  }

  static async _request(method, url, body) {
    const headers = { ...this.authHeaders() };
    if (body && typeof body === "object" && !(body instanceof FormData)) {
      headers["Content-Type"] = "application/json";
      body = JSON.stringify(body);
    }
    const res = await fetch(this.BASE_URL + url, { method, headers, body });
    if (res.status === 401) { this._redirectLogin(); return null; }
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.detail || `Error ${res.status}`);
    return data;
  }

  static async put(url, body) {
    return this._request("PUT", url, body);
  }

  static async patch(url, body) {
    return this._request("PATCH", url, body);
  }

  static async del(url) {
    const res = await fetch(this.BASE_URL + url, {
      method: "DELETE",
      headers: this.authHeaders(),
    });
    if (res.status === 401) {
      this._redirectLogin();
      return null;
    }
    if (!res.ok) {
      const data = await res.json().catch(() => ({}));
      throw new Error(data.detail || `Error ${res.status}`);
    }
    return res.json().catch(() => null);
  }
}
