import { test } from "node:test";
import assert from "node:assert/strict";
import {
  isValidIPv4, isValidIPv6, ipVersion, checkIp, checkSubnet, checkDomain, bitSplit,
} from "../validators.js";

test("accepts valid IPv4", () => {
  assert.equal(isValidIPv4("192.168.1.1"), true);
  assert.equal(isValidIPv4("0.0.0.0"), true);
  assert.equal(isValidIPv4("255.255.255.255"), true);
});

test("rejects bad IPv4 (failure path)", () => {
  for (const bad of ["256.0.0.1", "192.168.1", "1.2.3.4.5", "a.b.c.d", "01.2.3.4", "", "1.2.3."]) {
    assert.equal(isValidIPv4(bad), false, bad);
  }
});

test("accepts valid IPv6", () => {
  for (const ok of ["::1", "::", "2001:db8::1", "fe80::1", "1:2:3:4:5:6:7:8", "::ffff:192.168.1.1"]) {
    assert.equal(isValidIPv6(ok), true, ok);
  }
});

test("rejects bad IPv6", () => {
  for (const bad of ["1:2:3:4:5:6:7", "1::2::3", ":::", "12345::1", "g::1", "1:2:3:4:5:6:7:8:9"]) {
    assert.equal(isValidIPv6(bad), false, bad);
  }
});

test("trailing spaces are ignored by ipVersion", () => {
  assert.equal(ipVersion("  10.0.0.1  "), 4);
  assert.equal(ipVersion("::1"), 6);
  assert.equal(ipVersion("nope"), 0);
});

test("checkIp messages", () => {
  assert.equal(checkIp(""), "Enter an IP address.");
  assert.notEqual(checkIp("999.1.1.1"), "");
  assert.equal(checkIp("10.0.0.1"), "");
});

test("checkSubnet enforces prefix range", () => {
  assert.equal(checkSubnet("10.0.0.1", "24"), "");
  assert.notEqual(checkSubnet("10.0.0.1", "33"), "");
  assert.notEqual(checkSubnet("10.0.0.1", ""), "");
  assert.notEqual(checkSubnet("10.0.0.1", "abc"), "");
  assert.equal(checkSubnet("2001:db8::1", "64"), "");
  assert.notEqual(checkSubnet("2001:db8::1", "129"), "");
});

test("checkDomain", () => {
  assert.equal(checkDomain("google.com"), "");
  assert.equal(checkDomain("sub.example.co.uk"), "");
  assert.notEqual(checkDomain(""), "");
  assert.notEqual(checkDomain("localhost"), "");
  assert.notEqual(checkDomain("bad_domain.com"), "");
  assert.notEqual(checkDomain("-bad.com"), "");
});

test("bitSplit", () => {
  assert.deepEqual(bitSplit("192.168.1.10", 24), { network: 24, host: 8 });
  assert.equal(bitSplit("::1", 64), null);
  assert.equal(bitSplit("10.0.0.1", 40), null);
});
