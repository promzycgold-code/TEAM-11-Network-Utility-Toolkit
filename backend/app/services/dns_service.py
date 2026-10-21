import re
import dns.resolver


def is_valid_domain(domain):
    

    if not isinstance(domain, str):
        return False

    if not domain or len(domain) > 253:
        return False

    pattern = (
        r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)"
        r"(\.(?!-)[A-Za-z0-9-]{1,63}(?<!-))+$"
    )

    return bool(re.fullmatch(pattern, domain))


def lookup_dns(domain, record_type="A"):
   
    

    # Validate the domain name
    if not is_valid_domain(domain):
        return {
        "success": False,
        "error": "Invalid domain name"
    }

    supported_types = ["A", "AAAA", "MX", "TXT", "NS"]

    record_type = record_type.upper()

    if record_type not in supported_types:
        return {
            "success": False,
            "error": "Unsupported DNS record type"
        }

    
    
    try:
        answers = dns.resolver.resolve(
            domain,
            record_type,
            lifetime=5
        )

        records = []

        for answer in answers:
            records.append(answer.to_text())

        return {
            "success": True,
            "domain": domain,
            "record_type": record_type,
            "records": records
        }

    except dns.resolver.NXDOMAIN:
        return {
            "success": False,
            "error": "Domain does not exist"
        }

    except dns.resolver.NoAnswer:
        return {
            "success": True,
            "domain": domain,
            "record_type": record_type,
            "records": []
        }

    except dns.resolver.NoNameservers:
        return {
            "success": False,
            "error": "No DNS nameservers available"
        }

    except dns.exception.Timeout:
        return {
            "success": False,
            "error": "DNS lookup timed out"
        }

    except (dns.exception.DNSException, ValueError):
        return {
            "success": False,
            "error": "DNS lookup failed"
        }