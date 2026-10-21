

from services.subnet_service import calculate_subnet


# Test 1: Valid IPv4 subnet
def test_valid_ipv4_subnet():
    result = calculate_subnet("192.168.1.10/24")

    assert result["status"] == "success"
    assert result["data"]["cidr"] == "192.168.1.0/24"
    assert result["data"]["network_address"] == "192.168.1.0"
    assert result["data"]["broadcast_address"] == "192.168.1.255"
    assert result["data"]["subnet_mask"] == "255.255.255.0"
    assert result["data"]["total_hosts"] == 256
    assert result["data"]["usable_hosts"] == 254
    assert result["data"]["first_usable_ip"] == "192.168.1.1"
    assert result["data"]["last_usable_ip"] == "192.168.1.254"


# Test 2: IPv4 /31 subnet
def test_ipv4_31_subnet():
    result = calculate_subnet("192.168.1.0/31")

    assert result["status"] == "success"
    assert result["data"]["usable_hosts"] == 2
    assert result["data"]["first_usable_ip"] == "192.168.1.0"
    assert result["data"]["last_usable_ip"] == "192.168.1.1"


# Test 3: IPv4 /32 subnet
def test_ipv4_32_subnet():
    result = calculate_subnet("192.168.1.10/32")

    assert result["status"] == "success"
    assert result["data"]["usable_hosts"] == 1
    assert result["data"]["first_usable_ip"] == "192.168.1.10"
    assert result["data"]["last_usable_ip"] == "192.168.1.10"


# Test 4: Valid IPv6 subnet
def test_valid_ipv6_subnet():
    result = calculate_subnet("2001:db8::/64")

    assert result["status"] == "success"
    assert result["data"]["network_address"] == "2001:db8::"
    assert result["data"]["broadcast_address"] is None
    assert result["data"]["total_hosts"] == 2**64
    assert result["data"]["usable_hosts"] == 2**64
    assert result["data"]["first_usable_ip"] == "2001:db8::"
    assert result["data"]["last_usable_ip"] == "2001:db8::ffff:ffff:ffff:ffff"


# Test 5: Invalid subnet
def test_invalid_subnet():
    result = calculate_subnet("invalid/24")

    assert result["status"] == "error"


# Test 6: Invalid CIDR prefix
def test_invalid_prefix():
    result = calculate_subnet("192.168.1.0/40")

    assert result["status"] == "error"


# Test 7: Large IPv4 network
def test_large_ipv4_network():
    result = calculate_subnet("10.0.0.0/8")

    assert result["status"] == "success"
    assert result["data"]["total_hosts"] == 16777216
    assert result["data"]["usable_hosts"] == 16777214


# Test 8: Empty subnet input
def test_empty_subnet():
    result = calculate_subnet("")

    assert result["status"] == "error"


# Test 9: Non-string subnet input
def test_non_string_subnet():
    result = calculate_subnet(None)

    assert result["status"] == "error"
