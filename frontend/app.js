import { validateIp, calculateSubnet, lookupDns } from "./api.js";
import { USE_MOCK } from "./config.js";
import { checkIp, checkSubnet, checkDomain, bitSplit } from "./validators.js";

const $ = (id) => document.getElementById(id);

// ---------- tabs ----------
const tabs = document.querySelectorAll("[role=tab]");
tabs.forEach((tab) => {
  tab.addEventListener("click", () => selectTab(tab));
  tab.addEventListener("keydown", (e) => {
    const list = [...tabs];
    const i = list.indexOf(tab);
    if (e.key === "ArrowRight") selectTab(list[(i + 1) % list.length], true);
    if (e.key === "ArrowLeft") selectTab(list[(i - 1 + list.length) % list.length], true);
  });
});
function selectTab(tab, focus) {
  tabs.forEach((t) => {
    const on = t === tab;
    t.setAttribute("aria-selected", on);
    t.tabIndex = on ? 0 : -1;
    $(t.getAttribute("aria-controls")).hidden = !on;
  });
  if (focus) tab.focus();
}

// ---------- result rendering ----------
function pretty(key) {
  const s = key.replace(/_/g, " ");
  return s.charAt(0).toUpperCase() + s.slice(1);
}

function renderValue(value) {
  if (Array.isArray(value)) {
    if (value.every((v) => v === null || typeof v !== "object")) {
      const ul = document.createElement("ul");
      value.forEach((v) => {
        const li = document.createElement("li");
        li.textContent = String(v);
        ul.append(li);
      });
      return ul;
    }
    const wrap = document.createElement("div");
    value.forEach((v) => wrap.append(renderValue(v)));
    return wrap;
  }
  if (value && typeof value === "object") return renderTable(value);
  const span = document.createElement("span");
  span.textContent = value === null ? "-" : String(value);
  return span;
}

function renderTable(obj) {
  const table = document.createElement("table");
  const body = document.createElement("tbody");
  Object.entries(obj).forEach(([k, v]) => {
    const tr = document.createElement("tr");
    const th = document.createElement("th");
    th.scope = "row";
    th.textContent = pretty(k);
    const td = document.createElement("td");
    td.append(renderValue(v));
    tr.append(th, td);
    body.append(tr);
  });
  table.append(body);
  return table;
}

function show(target, node) {
  target.replaceChildren(node);
}
function showError(target, message) {
  const p = document.createElement("p");
  p.className = "error";
  p.setAttribute("role", "alert");
  p.textContent = message;
  show(target, p);
}
function showLoading(target) {
  const p = document.createElement("p");
  p.className = "muted";
  p.textContent = "Working...";
  show(target, p);
}

// ---------- 32-bit strip (subnet tab) ----------
function renderBits(ip, cidr) {
  const split = bitSplit(ip, cidr);
  if (!split) return null;
  const fig = document.createElement("figure");
  fig.className = "bits";
  const bar = document.createElement("div");
  bar.className = "bits-bar";
  bar.setAttribute("role", "img");
  bar.setAttribute("aria-label", `${split.network} network bits, ${split.host} host bits`);
  for (let i = 0; i < 32; i++) {
    const cell = document.createElement("span");
    cell.className = i < split.network ? "bit net" : "bit host";
    bar.append(cell);
  }
  const cap = document.createElement("figcaption");
  cap.textContent = `${split.network} network bits | ${split.host} host bits`;
  fig.append(bar, cap);
  return fig;
}

// ---------- form wiring ----------
function wire(formId, resultId, run) {
  const form = $(formId);
  const result = $(resultId);
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const button = form.querySelector("button[type=submit]");
    button.disabled = true;
    try {
      await run(new FormData(form), result, form);
    } catch (err) {
      showError(result, err.message);
    } finally {
      button.disabled = false;
    }
  });
}

wire("form-validate", "result-validate", async (data, result) => {
  const ip = data.get("ip").trim();
  const problem = checkIp(ip);
  if (problem) return showError(result, problem);
  showLoading(result);
  show(result, renderTable(await validateIp(ip)));
});

wire("form-subnet", "result-subnet", async (data, result) => {
  const ip = data.get("ip").trim();
  const cidr = data.get("cidr").trim();
  const problem = checkSubnet(ip, cidr);
  if (problem) return showError(result, problem);
  showLoading(result);
  const response = await calculateSubnet(ip, cidr);
  const wrap = document.createElement("div");
  const bits = renderBits(ip, cidr);
  if (bits) wrap.append(bits);
  wrap.append(renderTable(response));
  show(result, wrap);
});

wire("form-dns", "result-dns", async (data, result) => {
  const domain = data.get("domain").trim();
  const type = data.get("type");
  const problem = type === "PTR" ? checkIp(domain) : checkDomain(domain);
  if (problem) return showError(result, problem);
  showLoading(result);
  show(result, renderTable(await lookupDns(domain, type)));
});

// Reverse lookup takes an IP, so adjust the label when PTR is chosen.
$("dns-type").addEventListener("change", (e) => {
  const reverse = e.target.value === "PTR";
  $("dns-label").textContent = reverse ? "IP address" : "Domain name";
  $("dns-input").placeholder = reverse ? "8.8.8.8" : "example.com";
});

if (USE_MOCK) $("mock-banner").hidden = false;
