// Fake responses so you can build the UI before the API exists.
// Update the shapes here if the team agrees different field names.
const wait = (ms) => new Promise((r) => setTimeout(r, ms));

export async function mockRequest(path, body, query) {
  await wait(400);
  if (path === "/api/v1/validate") {
    return { ip: body.ip, valid: true, version: body.ip.includes(":") ? 6 : 4 };
  }
  if (path === "/api/v1/subnet") {
    return {
      ip: body.ip,
      cidr: body.cidr,
      network_address: "192.168.1.0",
      broadcast_address: "192.168.1.255",
      subnet_mask: "255.255.255.0",
      usable_hosts: 254,
      first_host: "192.168.1.1",
      last_host: "192.168.1.254",
    };
  }
  if (path === "/api/v1/dns") {
    if (query.domain === "nope.invalid") {
      const err = new Error("Domain not found.");
      err.status = 400;
      throw err;
    }
    return { domain: query.domain, type: query.type, records: ["142.250.74.46", "142.250.74.78"] };
  }
  throw new Error("Unknown mock route");
}
