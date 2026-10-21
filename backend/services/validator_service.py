import ipaddress

def validate_ip(ip_string):
    """
    Validate an IPv4 or IPv6 address.
    """

    try:
        ip = ipaddress.ip_address(ip_string)

        return {
            "status": "success",
            "data": {
                "ip": str(ip),
                "version": f"IPv{ip.version}",
                "is_private": ip.is_private,
                "is_global": ip.is_global,
                "is_loopback": ip.is_loopback,
                "is_multicast": ip.is_multicast,
                "is_link_local": ip.is_link_local,
                "is_reserved": ip.is_reserved,
            }
        }

    except ValueError as e:
        return {
            "status": "error",
            "message": f"Invalid IP address: {e}"
        }
#  --- Test Block ---
# if __name__ == "__main__":
#      print("\n--- TESTING IP VALIDATOR ---")
#      print(validate_ip("192.168.1.1"))
#      print(validate_ip("8.8.8.8"))
#      print(validate_ip("2001:db8::1"))
#      print(validate_ip("999.999.999.999")) # Should return error