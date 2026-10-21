from unittest.mock import patch

import dns.resolver

from app.services.dns_service import lookup_dns


def test_valid_a_record():

    from unittest.mock import MagicMock

    # Create simulated DNS answers
    answer1 = MagicMock()
    answer1.to_text.return_value = "8.8.8.8"

    answer2 = MagicMock()
    answer2.to_text.return_value = "8.8.4.4"

    fake_answers = [answer1, answer2]

    # Mock the DNS resolver
    with patch("app.services.dns_service.dns.resolver.resolve") as mock_resolve:

        mock_resolve.return_value = fake_answers

        result = lookup_dns("google.com", "A")

    # Verify the result
    assert result["success"] is True

    assert result["domain"] == "google.com"

    assert result["record_type"] == "A"

    assert result["records"] == ["8.8.8.8", "8.8.4.4"]

def test_empty_domain():
    result = lookup_dns("", "A")

    assert result["success"] is False
    assert result["error"] == "Invalid domain name"


def test_whitespace_domain():
    result = lookup_dns("   ", "A")

    assert result["success"] is False
    assert result["error"] == "Invalid domain name"


def test_numeric_domain():
    result = lookup_dns(12345, "A")

    assert result["success"] is False
    assert result["error"] == "Invalid domain name"


def test_unsupported_record_type():
    result = lookup_dns("google.com", "XYZ")

    assert result["success"] is False
    assert result["error"] == "Unsupported DNS record type"


def test_nonexistent_domain():
    with patch("app.services.dns_service.dns.resolver.resolve") as mock_resolve:
        mock_resolve.side_effect = dns.resolver.NXDOMAIN

        result = lookup_dns("example.invalid", "A")

    assert result["success"] is False
    assert result["error"] == "Domain does not exist"


def test_no_dns_answer():
    with patch("app.services.dns_service.dns.resolver.resolve") as mock_resolve:
        mock_resolve.side_effect = dns.resolver.NoAnswer

        result = lookup_dns("example.com", "MX")

    assert result["success"] is True
    assert result["records"] == []


    # Test 8: Domain containing double dots
def test_double_dot_domain():
    result = lookup_dns("google..com", "A")

    assert result["success"] is False
    assert result["error"] == "Invalid domain name"


# Test 9: Domain starting with a hyphen
def test_domain_starting_with_hyphen():
    result = lookup_dns("-google.com", "A")

    assert result["success"] is False
    assert result["error"] == "Invalid domain name"


# Test 10: Domain ending with a hyphen
def test_domain_ending_with_hyphen():
    result = lookup_dns("google-.com", "A")

    assert result["success"] is False
    assert result["error"] == "Invalid domain name"


# Test 11: Domain containing spaces
def test_domain_containing_spaces():
    result = lookup_dns("google com", "A")

    assert result["success"] is False
    assert result["error"] == "Invalid domain name"