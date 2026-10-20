import { API_BASE, USE_MOCK } from "./config.js";
import { mockRequest } from "./mock.js";

async function call(path, { method = "GET", body, query } = {}) {
  if (USE_MOCK) return mockRequest(path, body, query);

  let url = API_BASE + path;
  if (query) url += "?" + new URLSearchParams(query).toString();

  let res;
  try {
    res = await fetch(url, {
      method,
      headers: body ? { "Content-Type": "application/json" } : undefined,
      body: body ? JSON.stringify(body) : undefined,
    });
  } catch {
    throw new Error("Cannot reach the server. Check that the API is running.");
  }

  let data = null;
  try { data = await res.json(); } catch { /* non-JSON response */ }

  if (!res.ok) {
    const detail = data && (data.detail ?? data.error ?? data.message);
    const text = typeof detail === "string" ? detail : detail ? JSON.stringify(detail) : "";
    throw new Error(text || `The server returned an error (${res.status}).`);
  }
  return data;
}

export const validateIp = (ip) => call("/api/v1/validate", { method: "POST", body: { ip } });
export const calculateSubnet = (ip, cidr) =>
  call("/api/v1/subnet", { method: "POST", body: { ip, cidr: Number(cidr) } });
export const lookupDns = (domain, type) => call("/api/v1/dns", { query: { domain, type } });
