import ipaddress
import dns.resolver
import dns.reversename
import dns.exception


def reverse_dns_lookup(ip_address):
    
    # Validate the IP address
    try:
        ipaddress.ip_address(ip_address)

    except ValueError:
        return {
            "success": False,
            "error": "Invalid IP address"
        }

    try:
        # Convert IP address into reverse DNS format
        reverse_name = dns.reversename.from_address(ip_address)

        # Query PTR records
        answers = dns.resolver.resolve(
            reverse_name,
            "PTR",
            lifetime=5
        )

        # Extract hostnames
        hostnames = []

        for answer in answers:
            hostnames.append(answer.to_text().rstrip("."))

        return {
            "success": True,
            "ip_address": ip_address,
            "hostnames": hostnames
        }

    except dns.resolver.NXDOMAIN:
        return {
            "success": False,
            "error": "No reverse DNS record found"
        }

    except dns.resolver.NoAnswer:
        return {
            "success": True,
            "ip_address": ip_address,
            "hostnames": []
        }

    except dns.resolver.NoNameservers:
        return {
            "success": False,
            "error": "No DNS nameservers available"
        }

    except dns.exception.Timeout:
        return {
            "success": False,
            "error": "Reverse DNS lookup timed out"
        }

    except dns.exception.DNSException:
        return {
            "success": False,
            "error": "Reverse DNS lookup failed"
        }