// Pure functions: no DOM, no network. Easy to test.

export function isValidIPv4(value) {
  const parts = value.split(".");
  return (
    parts.length === 4 &&
    parts.every((p) => /^(0|[1-9]\d{0,2})$/.test(p) && Number(p) <= 255)
  );
}

export function isValidIPv6(value) {
  if (!/^[0-9a-fA-F:.]+$/.test(value)) return false;
  const halves = value.split("::");
  if (halves.length > 2) return false;
  const split = (s) => (s === "" ? [] : s.split(":"));
  const head = split(halves[0]);
  const tail = halves.length === 2 ? split(halves[1]) : [];
  const all = [...head, ...tail];
  let count = 0;
  for (let i = 0; i < all.length; i++) {
    const g = all[i];
    const atEnd = i === all.length - 1 && (halves.length === 1 || tail.length > 0);
    if (g.includes(".")) {
      if (!atEnd || !isValidIPv4(g)) return false;
      count += 2;
    } else if (/^[0-9a-fA-F]{1,4}$/.test(g)) {
      count += 1;
    } else {
      return false;
    }
  }
  return halves.length === 2 ? count <= 7 : count === 8;
}

// Returns 4, 6, or 0 (invalid). Trailing spaces are ignored.
export function ipVersion(value) {
  const v = String(value).trim();
  if (isValidIPv4(v)) return 4;
  if (isValidIPv6(v)) return 6;
  return 0;
}

// Returns an error message, or "" when the input is fine.
export function checkIp(value) {
  const v = String(value).trim();
  if (!v) return "Enter an IP address.";
  if (!ipVersion(v)) return "That is not a valid IPv4 or IPv6 address.";
  return "";
}

export function checkSubnet(ip, cidr) {
  const ipError = checkIp(ip);
  if (ipError) return ipError;
  const text = String(cidr).trim();
  if (!text) return "Enter a prefix length (CIDR).";
  if (!/^\d{1,3}$/.test(text)) return "CIDR must be a whole number.";
  const max = ipVersion(ip) === 4 ? 32 : 128;
  if (Number(text) > max) return `CIDR must be between 0 and ${max} for this address.`;
  return "";
}

export function checkDomain(value) {
  const v = String(value).trim();
  if (!v) return "Enter a domain name.";
  if (v.length > 253) return "Domain names are at most 253 characters.";
  const labels = v.replace(/\.$/, "").split(".");
  const ok =
    labels.length >= 2 &&
    labels.every((l) => /^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$/.test(l));
  return ok ? "" : "Enter a domain like example.com.";
}

// For the 32-bit visual: returns { network: n, host: 32-n } or null.
export function bitSplit(ip, cidr) {
  if (ipVersion(ip) !== 4) return null;
  const n = Number(cidr);
  if (!Number.isInteger(n) || n < 0 || n > 32) return null;
  return { network: n, host: 32 - n };
}
