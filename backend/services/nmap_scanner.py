import nmap
import sqlite3
from datetime import datetime


# Known vulnerable versions
VULNERABLE_VERSIONS = {
    "openssh": {
        "max_safe": "8.9",
        "cve": "CVE-2023-38408",
        "severity": "high",
        "description": "Remote code execution in OpenSSH before 8.9"
    },
    "apache": {
        "max_safe": "2.4.54",
        "cve": "CVE-2022-37436",
        "severity": "high",
        "description": "Apache HTTP Server before 2.4.54 vulnerable to request splitting"
    },
    "proftpd": {
        "max_safe": "1.3.7c",
        "cve": "CVE-2021-46850",
        "severity": "critical",
        "description": "ProFTPD before 1.3.7c arbitrary file read"
    },
    "vsftpd": {
        "max_safe": "3.0.3",
        "cve": "CVE-2015-1419",
        "severity": "medium",
        "description": "vsFTPd before 3.0.3 denial of service"
    },
    "mysql": {
        "max_safe": "8.0.33",
        "cve": "CVE-2023-22944",
        "severity": "medium",
        "description": "MySQL before 8.0.33 privilege escalation"
    },
    "postgresql": {
        "max_safe": "15.3",
        "cve": "CVE-2023-2455",
        "severity": "medium",
        "description": "PostgreSQL before 15.3 SQL injection"
    }
}


def run_nmap_scan(host, ports_to_scan=None):
    """
    Run Nmap scan with version detection on given ports.
    Returns services found, vulnerabilities, and risk score.
    """
    
    if ports_to_scan is None:
        ports_to_scan = [21, 22, 23, 25, 80, 443, 3306, 3389, 5432, 8080]
    
    port_string = ",".join(map(str, ports_to_scan))
    
    nm = nmap.PortScanner()
    
    print(f"[NMAP] Scanning {host} on ports {port_string}")
    
    try:
        nm.scan(hosts=host, ports=port_string, arguments="-sV -T4")
        
        host_data = nm["scan"].get(host, {})
        
        if not host_data:
            return {
                "host": host,
                "error": "Host unreachable",
                "scan_date": datetime.utcnow().isoformat(),
                "services_found": [],
                "vulnerabilities": []
            }
        
        services_found = []
        vulnerabilities_found = []
        
        tcp_results = host_data.get("tcp", {})
        
        for port in tcp_results:
            port_info = tcp_results[port]
            
            service_entry = {
                "port": port,
                "service": port_info.get("name", "unknown"),
                "product": port_info.get("product", "Unknown"),
                "version": port_info.get("version", "Unknown"),
                "state": port_info.get("state", "unknown")
            }
            
            vuln = check_version_vulnerability(
                service_entry["service"],
                service_entry["product"],
                service_entry["version"]
            )
            
            if vuln:
                service_entry["vulnerable"] = True
                service_entry["vulnerability"] = vuln
                vulnerabilities_found.append(service_entry)
            else:
                service_entry["vulnerable"] = False
            
            services_found.append(service_entry)
        
        risk_score, risk_level = calculate_risk_score(services_found, vulnerabilities_found)
        
        # Save to database
        try:
            conn = sqlite3.connect("audit.db")
            cursor = conn.cursor()
            
            ports_ouverts = [s["port"] for s in services_found]
            port_string_db = ",".join(map(str, ports_ouverts))
            
            cursor.execute(
                """
                INSERT INTO scans (host, ports, risque, score, date_scan)
                VALUES (?, ?, ?, ?, ?)
                """,
                (host, port_string_db, risk_level, risk_score, datetime.utcnow().isoformat())
            )
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[NMAP] Database save failed: {e}")
        
        return {
            "host": host,
            "scan_date": datetime.utcnow().isoformat(),
            "ports_scanned": ports_to_scan,
            "services_found": services_found,
            "vulnerabilities": vulnerabilities_found,
            "risk_score": risk_score,
            "risk_level": risk_level
        }
    
    except nmap.PortScannerError as e:
        return {
            "host": host,
            "error": f"Nmap error: {str(e)}. Is Nmap installed?",
            "scan_date": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "host": host,
            "error": f"Scan failed: {str(e)}",
            "scan_date": datetime.utcnow().isoformat()
        }


def check_version_vulnerability(service_name, product, version):
    """Compare detected version against known vulnerable versions."""
    
    if not product or not version:
        return None
    
    product_lower = product.lower()
    
    for vuln_service, vuln_info in VULNERABLE_VERSIONS.items():
        if vuln_service in product_lower or vuln_service in service_name.lower():
            if is_version_vulnerable(version, vuln_info["max_safe"]):
                return {
                    "service": service_name,
                    "product": product,
                    "detected_version": version,
                    "safe_version": vuln_info["max_safe"],
                    "cve": vuln_info["cve"],
                    "severity": vuln_info["severity"],
                    "description": vuln_info["description"]
                }
    
    return None


def is_version_vulnerable(detected_version, max_safe_version):
    """Compare two version strings. Returns True if detected is older."""
    
    def parse_version(v):
        parts = []
        for segment in v.strip().lstrip("vV").split("."):
            num = ""
            for char in segment:
                if char.isdigit():
                    num += char
                else:
                    break
            parts.append(int(num) if num else 0)
        return parts
    
    detected_parts = parse_version(detected_version)
    safe_parts = parse_version(max_safe_version)
    
    while len(detected_parts) < len(safe_parts):
        detected_parts.append(0)
    while len(safe_parts) < len(detected_parts):
        safe_parts.append(0)
    
    for d, s in zip(detected_parts, safe_parts):
        if d < s:
            return True
        elif d > s:
            return False
    
    return False


def calculate_risk_score(services_found, vulnerabilities_found):
    """
    Calculate risk score from 0 to 100.
    Start at 100, subtract based on open services and vulnerabilities.
    """
    
    score = 100
    
    for service in services_found:
        if not service.get("vulnerable", False):
            score -= 5
    
    severity_weights = {
        "critical": 25,
        "high": 15,
        "medium": 10,
        "low": 5
    }
    
    for vuln in vulnerabilities_found:
        severity = vuln.get("vulnerability", {}).get("severity", "low")
        score -= severity_weights.get(severity, 5)
    
    score = max(0, min(100, score))
    
    if score >= 80:
        level = "faible"
    elif score >= 50:
        level = "moyen"
    else:
        level = "élevé"
    
    return score, level