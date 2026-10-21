from app.services.dns_service import lookup_dns


print("Testing A Record:")
print(lookup_dns("google.com", "A"))

print("\nTesting MX Record:")
print(lookup_dns("gmail.com", "MX"))

print("\nTesting NS Record:")
print(lookup_dns("google.com", "NS"))

print("\nTesting Invalid Domain:")
print(lookup_dns("example.invalid", "A"))

print("\nTesting AAAA Record:")
print(lookup_dns("google.com", "AAAA"))

print("\nTesting TXT Record:")
print(lookup_dns("google.com", "TXT"))

print("\nTesting Unsupported Record:")
print(lookup_dns("google.com", "XYZ"))

print("\nTesting Empty Domain:")
print(lookup_dns("", "A"))



print("\nTesting Empty Domain:")
print(lookup_dns("", "A"))

print("\nTesting Whitespace Domain:")
print(lookup_dns("   ", "A"))

print("\nTesting Numeric Domain:")
print(lookup_dns(12345, "A"))