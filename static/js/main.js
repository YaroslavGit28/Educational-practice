document.addEventListener("click", (e) => {
  if (e.target.closest(".js-stop-card")) return;
  if (e.target.matches("[data-confirm]")) {
    if (!confirm(e.target.dataset.confirm)) {
      e.preventDefault();
    }
  }
  const card = e.target.closest(".product-click");
  if (card && card.dataset.href) {
    window.location.href = card.dataset.href;
  }
});

const liveSearchInput = document.querySelector("[data-live-search]");
const liveSearchForm = document.getElementById("live-search-form");

if (liveSearchInput && liveSearchForm) {
  let timer = null;
  liveSearchInput.addEventListener("input", () => {
    const query = liveSearchInput.value.trim();
    clearTimeout(timer);
    timer = setTimeout(() => {
      if (query.length === 0 || query.length >= 2) {
        liveSearchForm.submit();
      }
    }, 350);
  });
}

async function ajaxSubmit(form) {
  const method = (form.getAttribute("method") || "POST").toUpperCase();
  const url = form.getAttribute("action");
  const formData = new FormData(form);
  const res = await fetch(url, {
    method,
    body: formData,
    headers: { "X-Requested-With": "XMLHttpRequest" },
  });
  let payload = null;
  try {
    payload = await res.json();
  } catch {
    payload = { ok: false };
  }
  if (!res.ok || payload.ok === false) throw payload;
  return payload;
}

function setCartCount(count) {
  const el = document.getElementById("cart-count");
  if (el && typeof count !== "undefined") el.textContent = String(count);
}

document.addEventListener("submit", async (e) => {
  const form = e.target;
  const ajaxType = form.getAttribute("data-ajax");
  if (!ajaxType) return;
  e.preventDefault();

  try {
    const data = await ajaxSubmit(form);

    if (ajaxType === "cart-qty") {
      const row = document.querySelector(`[data-cart-item="${data.item_id}"]`);
      if (row) {
        const qtyEl = row.querySelector("[data-qty]");
        const totalEl = row.querySelector("[data-line-total]");
        if (qtyEl) qtyEl.textContent = String(data.qty);
        if (totalEl) totalEl.textContent = `${data.line_total} ₽`;
      }
      setCartCount(data.cart_count);
    }

    if (ajaxType === "cart-remove") {
      const row = document.querySelector(`[data-cart-item="${data.item_id}"]`);
      if (row) row.remove();
      setCartCount(data.cart_count);
    }

    if (ajaxType === "order-status") {
      const formWrap = form.closest(".bg-white");
      const badge = formWrap ? formWrap.querySelector(".badge") : null;
      if (badge) {
        badge.className = `badge status-${data.status}`;
        badge.textContent = data.status;
      }
      // hide current button after action to avoid double click
      form.remove();
    }

    if (ajaxType === "order-cancel") {
      const card = form.closest(".bg-white");
      const badge = card ? card.querySelector(".badge") : null;
      if (badge) {
        badge.className = "badge status-cancelled";
        badge.textContent = "cancelled";
      }
      form.remove();
    }
  } catch (err) {
    alert("Не удалось выполнить действие. Попробуйте ещё раз.");
  }
});
