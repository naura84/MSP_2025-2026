import sqlite3
import socket
import re
from datetime import datetime
from fastapi import HTTPException


def check_port(host, port):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.settimeout(1)

    try :

        result = sock.connect_ex((host, port))
     
        sock.close()
     
        return result == 0
    
    except socket.gaierror:

        return False
    

# Validation de l'hôte (IP ou domaine)
def is_valid_host(host):
    domain_pattern = r"^([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$"

    ip_pattern = r"^(\d{1,3}\.){3}\d{1,3}$"

    return (
        re.match(domain_pattern, host)
        or re.match(ip_pattern, host)
    )




def run_scan(host):

    if not is_valid_host(host):
        raise HTTPException(
            status_code=400,
            detail="Format Host invalide"
        )
    
    
    try:
        socket.gethostbyname(host)
    
    except socket.gaierror:

        raise HTTPException(
            status_code=404,
            detail="Host introuvable"
        )

    date_scan = datetime.utcnow().isoformat()

    score = 100

    # dictionnaire des ports et du risque associé à chaque port
    risk_rules = {
        21: 40,
        22: 20,
        80: 10,
        443: 5
    }

    ports_to_scan = [21, 22, 80, 443]
    open_ports = []

    for port in ports_to_scan:
        if check_port(host, port):
            open_ports.append(port)
            score -= risk_rules.get(port, 0)

    risque = "faible"
    port_string = ",".join(map(str, open_ports))

    # Déterminer le niveau de risque en fonction du score
    if score >= 80:
        risque = "faible"
    elif score >= 50:
        risque = "moyen"
    else:
        risque = "élevé"
    
    # connexion à la base de données
    conn = sqlite3.connect("audit.db")

    cursor = conn.cursor()
    
    cursor.execute(
        """
        INSERT INTO scans (
        host,
        ports,
        risque,
        score,
        date_scan
        )
        VALUES (?,?,?,?,?)
        """, 
        (
            host,
            port_string,
            risque,
            score,
            date_scan
        )
    )

    conn.commit()
    conn.close()

    return {
        "host": host,
        "open_ports": open_ports,
        "risque": risque,
        "score": score,
        "date_scan": date_scan
    }