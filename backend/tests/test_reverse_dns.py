from unittest.mock import patch, MagicMock

import dns.resolver

from app.services.reverse_dns_service import reverse_dns_lookup


# Test 1: Valid IPv4 address
def test_valid_ipv4():

    fake_answer = MagicMock()
    fake_answer.to_text.return_value = "dns.google."

    with patch(
        "app.services.reverse_dns_service.dns.resolver.resolve"
    ) as mock_resolve:

        mock_resolve.return_value = [fake_answer]

        result = reverse_dns_lookup("8.8.8.8")

    assert result["success"] is True
    assert result["ip_address"] == "8.8.8.8"
    assert result["hostnames"] == ["dns.google"]


# Test 2: Valid IPv6 address
def test_valid_ipv6():

    fake_answer = MagicMock()
    fake_answer.to_text.return_value = "dns.google."

    with patch(
        "app.services.reverse_dns_service.dns.resolver.resolve"
    ) as mock_resolve:

        mock_resolve.return_value = [fake_answer]

        result = reverse_dns_lookup("2001:4860:4860::8888")

    assert result["success"] is True
    assert result["ip_address"] == "2001:4860:4860::8888"
    assert result["hostnames"] == ["dns.google"]


# Test 3: Invalid IP address
def test_invalid_ip():

    result = reverse_dns_lookup("999.999.999.999")

    assert result["success"] is False
    assert result["error"] == "Invalid IP address"


# Test 4: Empty IP address
def test_empty_ip():

    result = reverse_dns_lookup("")

    assert result["success"] is False
    assert result["error"] == "Invalid IP address"


# Test 5: Missing PTR record
def test_missing_ptr_record():

    with patch(
        "app.services.reverse_dns_service.dns.resolver.resolve"
    ) as mock_resolve:

        mock_resolve.side_effect = dns.resolver.NXDOMAIN

        result = reverse_dns_lookup("8.8.8.8")

    assert result["success"] is False
    assert result["error"] == "No reverse DNS record found"


# Test 6: No DNS answer
def test_no_dns_answer():

    with patch(
        "app.services.reverse_dns_service.dns.resolver.resolve"
    ) as mock_resolve:

        mock_resolve.side_effect = dns.resolver.NoAnswer

        result = reverse_dns_lookup("8.8.8.8")

    assert result["success"] is True
    assert result["hostnames"] == []


# Test 7: DNS timeout
def test_dns_timeout():

    with patch(
        "app.services.reverse_dns_service.dns.resolver.resolve"
    ) as mock_resolve:

        mock_resolve.side_effect = dns.resolver.LifetimeTimeout

        result = reverse_dns_lookup("8.8.8.8")

    assert result["success"] is False
    assert result["error"] == "Reverse DNS lookup timed out"