
from services.validator_service import validate_ip


# Test 1: Valid IPv4 address
def test_valid_ipv4():
    result = validate_ip("192.168.1.1")

    assert result["status"] == "success"
    assert result["data"]["ip"] == "192.168.1.1"
    assert result["data"]["version"] == "IPv4"


# Test 2: Valid IPv6 address
def test_valid_ipv6():
    result = validate_ip("2001:db8::1")

    assert result["status"] == "success"
    assert result["data"]["version"] == "IPv6"


# Test 3: Invalid IPv4 address
def test_invalid_ipv4():
    result = validate_ip("999.999.999.999")

    assert result["status"] == "error"


# Test 4: Invalid IPv6 address
def test_invalid_ipv6():
    result = validate_ip("2001:db8:::1")

    assert result["status"] == "error"


# Test 5: Empty IP address
def test_empty_ip():
    result = validate_ip("")

    assert result["status"] == "error"


# Test 6: Loopback IPv4 address
def test_loopback_ipv4():
    result = validate_ip("127.0.0.1")

    assert result["status"] == "success"
    assert result["data"]["is_loopback"] is True


# Test 7: Private IPv4 address
def test_private_ipv4():
    result = validate_ip("192.168.1.1")

    assert result["status"] == "success"
    assert result["data"]["is_private"] is True


# Test 8: Public IPv4 address
def test_public_ipv4():
    result = validate_ip("8.8.8.8")

    assert result["status"] == "success"
    assert result["data"]["is_global"] is True


# Test 9: IPv4 address with invalid octet
def test_invalid_octet():
    result = validate_ip("256.0.0.1")

    assert result["status"] == "error"


# Test 10: IP address containing spaces
def test_ip_with_spaces():
    result = validate_ip("192.168.1.1 ")

    assert result["status"] == "error"


# Test 11: Non-string IP address
def test_non_string_ip():
    result = validate_ip(None)

    assert result["status"] == "error"
