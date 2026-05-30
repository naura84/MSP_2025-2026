from services.nmap_scanner import discover_hosts, run_nmap_scan

print("=" * 50)
print("TEST 1: Network Discovery")
print("=" * 50)

# Scan your local network for connected machines
hosts = discover_hosts()
print(f"\nMachines found: {len(hosts)}")
for h in hosts:
    print(f"  - {h['ip']} ({h['hostname']})")

print("\n" + "=" * 50)
print("TEST 2: Port & Vulnerability Scan")
print("=" * 50)

# Scan your own machine (localhost)
result = run_nmap_scan("127.0.0.1")
print(f"\nHost: {result['host']}")
print(f"Risk level: {result.get('risk_level', 'N/A')}")
print(f"Risk score: {result.get('risk_score', 'N/A')}")
print(f"Services found: {len(result.get('services_found', []))}")
print(f"Vulnerabilities: {len(result.get('vulnerabilities', []))}")

# Show vulnerabilities if any
for v in result.get('vulnerabilities', []):
    print(f"\n  ⚠️  Port {v['port']} - {v['product']} {v['version']}")
    if v.get('vulnerability'):
        print(f"     CVE: {v['vulnerability']['cve']}")
        print(f"     Severity: {v['vulnerability']['severity']}")

print("\nDone!")