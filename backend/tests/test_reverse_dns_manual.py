from app.services.reverse_dns_service import reverse_dns_lookup


print("Testing Google DNS:")
print(reverse_dns_lookup("8.8.8.8"))

print("\nTesting Cloudflare DNS:")
print(reverse_dns_lookup("1.1.1.1"))

print("\nTesting Invalid IP:")
print(reverse_dns_lookup("999.999.999.999"))

print("\nTesting IPv6:")
print(reverse_dns_lookup("2001:4860:4860::8888"))