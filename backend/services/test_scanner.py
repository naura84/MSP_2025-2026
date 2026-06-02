from services.nmap_scanner import discover_hosts, run_nmap_scan
import sqlite3


def main():
    print("=" * 50)
    print("TEST 1: Network Discovery")
    print("=" * 50)

    hosts = discover_hosts()
    print(f"\nMachines found: {len(hosts)}")
    for h in hosts:
        print(f"  - {h['ip']} ({h['hostname']})")

    print("\n" + "=" * 50)
    print("TEST 2: Port & Vulnerability Scan")
    print("=" * 50)

    result = run_nmap_scan("192.168.1.1", [80, 443, 22, 21, 23])
    print(f"\nHost: {result['host']}")
    print(f"Risk level: {result.get('risk_level', 'N/A')}")
    print(f"Risk score: {result.get('risk_score', 'N/A')}")
    print(f"Services found: {len(result.get('services_found', []))}")

    for s in result.get('services_found', []):
        print(f"  Port {s['port']}: {s['product']} {s['version']} - Vulnerable: {s['vulnerable']}")
        if s.get('vulnerability'):
            print(f"    CVE: {s['vulnerability']['cve']}")
            print(f"    Severity: {s['vulnerability']['severity']}")

    print(f"\nVulnerabilities found: {len(result.get('vulnerabilities', []))}")

    print("\n" + "=" * 50)
    print("TEST 3: Database Check")
    print("=" * 50)

    conn = sqlite3.connect("audit.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scans ORDER BY id DESC LIMIT 5")
    rows = cursor.fetchall()

    print(f"\nLast 5 scans in database:")
    for row in rows:
        print(f"  Host: {row[1]}, Ports: {row[2]}, Risk: {row[3]}, Score: {row[4]}")

    conn.close()
    print("\nDone!")


if __name__ == "__main__":
    main()