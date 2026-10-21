import ipaddress

def calculate_subnet(cidr_string):

    try:
        network = ipaddress.ip_network(cidr_string, strict=False)

        total_addresses = network.num_addresses

        if network.version == 4:
            if network.prefixlen == 32:
                usable_hosts = 1
            elif network.prefixlen == 31:
                usable_hosts = 2
            else:
                usable_hosts = total_addresses - 2

            broadcast_address = str(network.broadcast_address)

        else:
            usable_hosts = total_addresses
            broadcast_address = None

        if network.version == 4 and network.prefixlen < 31:
            first_usable = network.network_address + 1
            last_usable = network.broadcast_address - 1
        else:
            first_usable = network.network_address
            last_usable = network[-1]

        return {
            "status": "success",
            "data": {
                "cidr": str(network),
                "network_address": str(network.network_address),
                "broadcast_address": broadcast_address,
                "subnet_mask": str(network.netmask),
                "total_hosts": total_addresses,
                "usable_hosts": usable_hosts,
                "first_usable_ip": str(first_usable),
                "last_usable_ip": str(last_usable),
            }
        }

    except (ValueError, TypeError) as e:
        return {
            "status": "error",
            "message": str(e)
        }
