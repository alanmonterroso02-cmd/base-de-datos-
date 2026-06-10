class AdminUI {
  static checkAuth() {
    const token = EcoAPI.getToken();
    if (!token) {
      window.location.href = "/login";
      return false;
    }
    return true;
  }

  static loadingRow(colspan, message = "Cargando...") {
    return `<tr><td colspan="${colspan}" class="text-center py-4">
      <div class="spinner-border spinner-border-sm me-2" role="status"></div>${message}
    </td></tr>`;
  }

  static emptyRow(colspan, message = "No hay datos disponibles.") {
    return `<tr><td colspan="${colspan}" class="text-center py-4 text-muted">${message}</td></tr>`;
  }

  static errorRow(colspan, message = "Error al cargar datos.") {
    return `<tr><td colspan="${colspan}" class="text-center py-4 text-danger">${message}</td></tr>`;
  }

  static async loadTable(url, tbodyId, renderFn, options = {}) {
    const tbody = document.getElementById(tbodyId);
    if (!tbody) return;
    const { emptyMessage, errorMessage, loadingMessage, colspan } = options;
    tbody.innerHTML = AdminUI.loadingRow(colspan || 3, loadingMessage);

    try {
      const data = await EcoAPI.get(url);
      if (!data || data.length === 0) {
        tbody.innerHTML = AdminUI.emptyRow(colspan || 3, emptyMessage);
        return;
      }
      tbody.innerHTML = renderFn(data);
    } catch (error) {
      console.error(error);
      tbody.innerHTML = AdminUI.errorRow(colspan || 3, errorMessage);
      EcoToast.error(error.message || "Error al cargar datos");
    }
  }

  static async submitForm(formId, apiUrl, method = "post", options = {}) {
    const form = document.getElementById(formId);
    if (!form) return;
    const btn = form.querySelector('button[type="submit"]');
    const { onSuccess, transformData, modalId } = options;

    btn.disabled = true;
    btn.textContent = "Guardando...";

    try {
      let body;
      if (transformData) {
        const fd = new FormData(form);
        body = transformData(fd);
      } else {
        body = new FormData(form);
      }

      await EcoAPI[method](apiUrl, body);
      EcoToast.success("Operación completada correctamente");

      if (modalId) {
        const modal = bootstrap.Modal.getInstance(document.getElementById(modalId));
        if (modal) modal.hide();
      }
      form.reset();
      if (onSuccess) onSuccess();
    } catch (error) {
      EcoToast.error(error.message || "Error en la operación");
    } finally {
      btn.disabled = false;
      btn.textContent = "Guardar";
    }
  }

  static async confirmAction(message, actionFn) {
    if (!confirm(message)) return;
    try {
      await actionFn();
      EcoToast.success("Operación completada");
    } catch (error) {
      EcoToast.error(error.message || "Error en la operación");
    }
  }
}
