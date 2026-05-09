import sqlite3
import socket

def check_port(host, port):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.settimeout(1)

    result = sock.connect_ex((host, port))

    sock.close()

    return result == 0

def run_scan(host):

    ports_to_scan = [21, 22, 80, 443]
    open_ports = []

    for port in ports_to_scan:

        if check_port(host, port):
            open_ports.append(port)

    risque = "faible"

    if 21 in open_ports:
        risque = "élevé"

    elif 22 in open_ports:
        risque = "moyen"
    
    conn = sqlite3.connect("audit.db")

    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO scans (status, risque) VALUES (?, ?)",
                   ("scan termine", risque)
                   )
    conn.commit()
    conn.close()

    return {
        "host" : host,
        "ports_ouverts" : open_ports,
        "risque" : risque
    }