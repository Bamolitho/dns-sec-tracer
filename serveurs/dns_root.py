"""
    dns_root.py
    Objectif : Serveur DNS Root simulé avec signature DNSSEC
    Auteur : Amolitho BALDE
    Date : 31 mai 2025
"""
import socket
import json
import os
import sys

from logs_utils import write_log, clear_current_resolution_log

DNSSEC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../dnssec"))
sys.path.insert(0, DNSSEC_DIR)
import dnssec

# Zone initiale avec quelques TLD connus
zone = {
    "com.": ("localhost", 5302),
    "org.": ("localhost", 5302),
    "io.": ("localhost", 5302)
}

DEFAULT_IP = "localhost"
DEFAULT_PORT = 5302

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("localhost", 5301))

print("[Root DNS] En écoute sur port 5301...")

while True:
    data, addr = s.recvfrom(1024)
    domain = data.decode().strip().lower()  # nettoyage + minuscules

    # Extraire le TLD (tout après le dernier '.')
    if '.' in domain:
        tld = domain.split('.')[-1] + '.'
    else:
        tld = ""

    # Ajouter le TLD dynamique si non connu
    if tld and tld not in zone:
        zone[tld] = (DEFAULT_IP, DEFAULT_PORT)

    ip, port = zone.get(tld, ("0.0.0.0", 0))

    clear_current_resolution_log("root")
    write_log("root", f"Reçu de {addr[0]}:{addr[1]} | Domaine: {domain} → TLD: {tld}")

    signature = dnssec.sign_response(domain, ip)

    response = {
        "ip": ip,
        "port": port,
        "signature": signature
    }

    s.sendto(json.dumps(response).encode(), addr)
    write_log("root", f"Réponse envoyée à {addr[0]}:{addr[1]} → IP: {ip}, Port: {port}, Signature: {signature[:8]}...")
