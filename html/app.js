function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

async function api(url, options = {}) {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const data = await response.json();
  if (!response.ok || !data.ok) {
    throw new Error(data.error || "Request failed.");
  }
  return data;
}

function setMessage(message, isError) {
  const el = document.getElementById("message");
  if (!el) return;
  el.textContent = message || "";
  el.className = message ? (isError ? "msg-error" : "msg-success") : "";
}

function pageName() {
  const path = window.location.pathname;
  if (!path || path === "/") return "index.html";
  return path.split("/").pop();
}

function highlightActiveNav() {
  const page = pageName();
  document.querySelectorAll("nav a").forEach((a) => {
    if (a.getAttribute("href") === page) a.classList.add("active");
  });
}

function statusBadge(status) {
  const cls = { Available: "badge-available", Reserved: "badge-reserved", Sold: "badge-sold" }[status] || "";
  return `<span class="badge ${cls}">${escapeHtml(status)}</span>`;
}

function renderRows(tbody, rows, emptyText, rowRenderer) {
  if (!tbody) return;
  if (!rows.length) {
    tbody.innerHTML = `<tr><td colspan="20" style="text-align:center;color:#94a3b8;padding:2rem 1rem;">${escapeHtml(emptyText)}</td></tr>`;
    return;
  }
  tbody.innerHTML = rows.map(rowRenderer).join("");
}

async function initDashboard() {
  const data = await api("/api/dashboard");
  document.getElementById("metricTotalInventory").textContent = data.metrics.total_inventory;
  document.getElementById("metricItemsAvailable").textContent = data.metrics.items_available;
  document.getElementById("metricItemsReserved").textContent = data.metrics.items_reserved;
  document.getElementById("metricItemsSold").textContent = data.metrics.items_sold;
  document.getElementById("metricSoldCost").textContent = "$" + Number(data.metrics.sold_inventory_cost).toFixed(2);

  const tbody = document.getElementById("recentSalesBody");
  renderRows(tbody, data.recentSold, "No sold items yet.", (row) => `
    <tr>
      <td>${escapeHtml(row.ItemID)}</td>
      <td>${escapeHtml(row.Brand)}</td>
      <td>${escapeHtml(row.Model)}</td>
      <td>${escapeHtml(row.CustomerID ?? "—")}</td>
    </tr>
  `);
}

async function loadSneakers() {
  const data = await api("/api/sneakers");
  const tbody = document.getElementById("sneakerBody");
  renderRows(tbody, data.sneakers, "No sneakers found.", (row) => `
    <tr>
      <td>${escapeHtml(row.ID)}</td>
      <td>${escapeHtml(row.Brand)}</td>
      <td>${escapeHtml(row.Model)}</td>
      <td>${escapeHtml(row.Colorway || "—")}</td>
      <td>${escapeHtml(row.ReleaseDate ?? "—")}</td>
      <td><button class="btn btn-danger btn-sm" type="button" data-sneaker-id="${escapeHtml(row.ID)}">Delete</button></td>
    </tr>
  `);

  tbody.querySelectorAll("button[data-sneaker-id]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      if (!confirm("Delete this sneaker model? This cannot be undone.")) return;
      try {
        await api(`/api/sneakers/${btn.getAttribute("data-sneaker-id")}`, { method: "DELETE" });
        setMessage("Sneaker deleted.", false);
        await loadSneakers();
      } catch (err) {
        setMessage(err.message, true);
      }
    });
  });
}

function initAddSneaker() {
  const form = document.getElementById("addSneakerForm");
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const payload = {
      sneakerId: form.sneakerId.value,
      brand: form.brand.value,
      model: form.model.value,
      colorway: form.colorway.value,
      releaseDate: form.releaseDate.value,
    };
    try {
      const result = await api("/api/sneakers", { method: "POST", body: JSON.stringify(payload) });
      setMessage(result.message || "Sneaker saved.", false);
      form.reset();
      await loadSneakers();
    } catch (err) {
      setMessage(err.message, true);
    }
  });
  loadSneakers();
}

async function loadInventory(query = "") {
  const data = await api(`/api/inventory${query}`);
  const tbody = document.getElementById("inventoryBody");
  renderRows(tbody, data.inventory, "No inventory items found.", (row) => `
    <tr>
      <td>${escapeHtml(row.ItemID)}</td>
      <td><strong>${escapeHtml(row.Brand)}</strong> ${escapeHtml(row.Model)}</td>
      <td>${escapeHtml(row.Size)}</td>
      <td>${escapeHtml(row.ItemCondition)}</td>
      <td>$${escapeHtml(Number(row.PurchasePrice).toFixed(2))}</td>
      <td>${statusBadge(row.Status)}</td>
      <td>${escapeHtml(row.CustomerID ?? "—")}</td>
      <td><button class="btn btn-danger btn-sm" type="button" data-item-id="${escapeHtml(row.ItemID)}">Delete</button></td>
    </tr>
  `);

  tbody.querySelectorAll("button[data-item-id]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      if (!confirm("Delete this inventory item? This cannot be undone.")) return;
      try {
        await api(`/api/inventory/${btn.getAttribute("data-item-id")}`, { method: "DELETE" });
        setMessage("Inventory item deleted.", false);
        await loadInventory(query);
      } catch (err) {
        setMessage(err.message, true);
      }
    });
  });
}

function initAddInventory() {
  const form = document.getElementById("addInventoryForm");
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const payload = {
      itemId: form.itemId.value,
      sneakerId: form.sneakerId.value,
      size: form.size.value,
      condition: form.condition.value,
      purchasePrice: form.purchasePrice.value,
      supplierId: form.supplierId.value,
      status: form.status.value,
    };
    try {
      const result = await api("/api/inventory", { method: "POST", body: JSON.stringify(payload) });
      setMessage(result.message || "Inventory item saved.", false);
      form.reset();
      await loadInventory();
    } catch (err) {
      setMessage(err.message, true);
    }
  });
  loadInventory();
}

async function loadSuppliers(query = "") {
  const data = await api(`/api/suppliers${query}`);
  const tbody = document.getElementById("supplierBody");
  renderRows(tbody, data.suppliers, "No suppliers found.", (row) => `
    <tr>
      <td>${escapeHtml(row.ID)}</td>
      <td>${escapeHtml(row.Name)}</td>
      <td>${escapeHtml(row.Type)}</td>
      <td>${escapeHtml(row.ContactInfo)}</td>
      <td><button class="btn btn-danger btn-sm" type="button" data-supplier-id="${escapeHtml(row.ID)}">Delete</button></td>
    </tr>
  `);

  tbody.querySelectorAll("button[data-supplier-id]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      if (!confirm("Delete this supplier?")) return;
      try {
        await api(`/api/suppliers/${btn.getAttribute("data-supplier-id")}`, { method: "DELETE" });
        setMessage("Supplier deleted.", false);
        await loadSuppliers(query);
      } catch (err) {
        setMessage(err.message, true);
      }
    });
  });
}

function initSupplierManagement() {
  const saveForm = document.getElementById("supplierSaveForm");
  const searchForm = document.getElementById("supplierSearchForm");

  saveForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const payload = {
      supplierId: saveForm.supplierId.value,
      name: saveForm.name.value,
      type: saveForm.type.value,
      contactInfo: saveForm.contactInfo.value,
    };
    try {
      const result = await api("/api/suppliers", { method: "POST", body: JSON.stringify(payload) });
      setMessage(result.message || "Supplier saved.", false);
      saveForm.reset();
      await loadSuppliers();
    } catch (err) {
      setMessage(err.message, true);
    }
  });

  searchForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const params = new URLSearchParams({
      searchName: searchForm.searchName.value,
      searchType: searchForm.searchType.value,
    });
    await loadSuppliers(`?${params.toString()}`);
  });

  loadSuppliers();
}

async function loadCustomers(query = "") {
  const data = await api(`/api/customers${query}`);
  const tbody = document.getElementById("customerBody");
  renderRows(tbody, data.customers, "No customers found.", (row) => `
    <tr>
      <td>${escapeHtml(row.ID)}</td>
      <td>${escapeHtml(row.FirstName)} ${escapeHtml(row.LastName)}</td>
      <td>${escapeHtml(row.Email)}</td>
      <td>${escapeHtml(row.Phone ?? "—")}</td>
      <td><button class="btn btn-danger btn-sm" type="button" data-customer-id="${escapeHtml(row.ID)}">Delete</button></td>
    </tr>
  `);

  tbody.querySelectorAll("button[data-customer-id]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      if (!confirm("Delete this customer?")) return;
      try {
        await api(`/api/customers/${btn.getAttribute("data-customer-id")}`, { method: "DELETE" });
        setMessage("Customer deleted.", false);
        await loadCustomers(query);
      } catch (err) {
        setMessage(err.message, true);
      }
    });
  });
}

function initCustomerManagement() {
  const saveForm = document.getElementById("customerSaveForm");
  const searchForm = document.getElementById("customerSearchForm");

  saveForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const payload = {
      customerId: saveForm.customerId.value,
      firstName: saveForm.firstName.value,
      lastName: saveForm.lastName.value,
      email: saveForm.email.value,
      phone: saveForm.phone.value,
    };
    try {
      const result = await api("/api/customers", { method: "POST", body: JSON.stringify(payload) });
      setMessage(result.message || "Customer saved.", false);
      saveForm.reset();
      await loadCustomers();
    } catch (err) {
      setMessage(err.message, true);
    }
  });

  searchForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const params = new URLSearchParams({
      searchName: searchForm.searchName.value,
      searchEmail: searchForm.searchEmail.value,
    });
    await loadCustomers(`?${params.toString()}`);
  });

  loadCustomers();
}

async function loadSoldPreview() {
  const data = await api("/api/record_sale");
  const tbody = document.getElementById("soldPreviewBody");
  renderRows(tbody, data.soldPreview, "No sold items yet.", (row) => `
    <tr>
      <td>${escapeHtml(row.ItemID)}</td>
      <td><strong>${escapeHtml(row.Brand)}</strong> ${escapeHtml(row.Model)}</td>
      <td>${escapeHtml(row.CustomerID ?? "—")}</td>
    </tr>
  `);
}

function initRecordSale() {
  const form = document.getElementById("recordSaleForm");
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const payload = {
      itemId: form.itemId.value,
      customerId: form.customerId.value,
    };
    try {
      await api("/api/record_sale", { method: "POST", body: JSON.stringify(payload) });
      setMessage("Sale recorded — item marked as Sold.", false);
      form.reset();
      await loadSoldPreview();
    } catch (err) {
      setMessage(err.message, true);
    }
  });
  loadSoldPreview();
}

function initInventorySearch() {
  const form = document.getElementById("inventorySearchForm");
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const params = new URLSearchParams({
      brand: form.brand.value,
      size: form.size.value,
      status: form.status.value,
    });
    try {
      await loadInventory(`?${params.toString()}`);
      setMessage("", false);
    } catch (err) {
      setMessage(err.message, true);
    }
  });
  loadInventory();
}

async function initReports() {
  const data = await api("/api/reports");

  renderRows(document.getElementById("statusBreakdownBody"), data.statusBreakdown, "No data.", (row) => `
    <tr>
      <td>${statusBadge(row.Status)}</td>
      <td>${escapeHtml(row.Count)}</td>
    </tr>
  `);

  renderRows(document.getElementById("supplierStockBody"), data.supplierStock, "No data.", (row) => `
    <tr>
      <td>${escapeHtml(row.SupplierID)}</td>
      <td>${escapeHtml(row.Name)}</td>
      <td>${escapeHtml(row.TotalItems)}</td>
      <td>${escapeHtml(row.AvailableItems)}</td>
      <td>${escapeHtml(row.SoldItems)}</td>
    </tr>
  `);

  renderRows(document.getElementById("soldByModelBody"), data.soldByModel, "No data.", (row) => `
    <tr>
      <td>${escapeHtml(row.SneakerID)}</td>
      <td>${escapeHtml(row.Brand)}</td>
      <td>${escapeHtml(row.Model)}</td>
      <td>${escapeHtml(row.SoldCount)}</td>
      <td>$${escapeHtml(Number(row.TotalCost).toFixed(2))}</td>
    </tr>
  `);
}

document.addEventListener("DOMContentLoaded", async () => {
  highlightActiveNav();
  try {
    const page = pageName();
    if (page === "index.html") await initDashboard();
    if (page === "add_sneaker.html") initAddSneaker();
    if (page === "add_inventory.html") initAddInventory();
    if (page === "supplier_management.html") initSupplierManagement();
    if (page === "customer_management.html") initCustomerManagement();
    if (page === "record_sale.html") initRecordSale();
    if (page === "inventory_search.html") initInventorySearch();
    if (page === "reports.html") await initReports();
  } catch (err) {
    setMessage(err.message || "Unexpected error.", true);
  }
});
