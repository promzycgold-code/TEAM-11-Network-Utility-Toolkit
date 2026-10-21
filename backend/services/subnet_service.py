import ipaddress

def calculate_subnet(cidr_string):
    """
    Takes a string like '192.168.1.0/24' and returns network details.
    """
    try:
        network = ipaddress.ip_network(cidr_string, strict=False)
        
        hosts = list(network.hosts())
        
        return {
            "status": "success",
            "data": {
                "cidr": str(network),
                "network_address": str(network.network_address),
                "broadcast_address": None,
                "subnet_mask": str(network.netmask),
                "total_hosts": network.num_addresses,
                "usable_hosts": len(hosts),
                "first_usable_ip": str(hosts[0]) if len(hosts) > 0 else "N/A",
                "last_usable_ip": str(hosts[-1]) if len(hosts) > 0 else "N/A",
            }
        }
    except ValueError as e:
        return {
            "status": "error",
            "message": str(e)
        }
# --- Test Block ---
if __name__ == "__main__":
    print("--- TESTING CIDR ---")
    print(calculate_subnet("192.168.1.0/24"))
    print(calculate_subnet("10.0.0.0/8"))
    print(calculate_subnet("invalid/24")) # Should return error

#     print("\n--- TESTING IP VALIDATOR ---")
#     print(validate_ip("192.168.1.1"))
#     print(validate_ip("8.8.8.8"))
#     print(validate_ip("2001:db8::1"))
#     print(validate_ip("999.999.999.999")) # Should return error