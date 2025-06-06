"""
    dns_auth.py
    Objectif : Serveur DNS autoritaire simulé avec signature DNSSEC
    Auteur : Amolitho BALDE
    Date : 31 mai 2025
"""

import socket
import json
import os
import sys

DNSSEC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../dnssec"))
sys.path.insert(0, DNSSEC_DIR)
import dnssec

from logs_utils import write_log, clear_current_resolution_log, finalize_resolution

# Initialisation du socket UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("localhost", 5303))

print("[Authoritative DNS] En écoute sur le port 5303...")

while True:
    data, addr = s.recvfrom(1024)
    domain = data.decode().strip()

    clear_current_resolution_log("auth")
    write_log("auth", f"Reçu de {addr[0]}:{addr[1]} | Domaine: {domain}")

    response = {}

    try:
        # Si c'est un nom de domaine, tenter une résolution gethostbyname
        if not domain.endswith(".in-addr.arpa."):
            ip = socket.gethostbyname(domain.rstrip('.'))
            signature = dnssec.sign_response(domain, ip)
            write_log("auth", f"A | {domain} → IP: {ip}, Signature: {signature}")
            response["ip"] = ip
            response["signature"] = signature

        # Sinon, c'est une requête PTR
        else:
            ip_parts = domain.replace(".in-addr.arpa.", "").split('.')
            ip_address = '.'.join(reversed(ip_parts))
            hostname, _, _ = socket.gethostbyaddr(ip_address)
            signature = dnssec.sign_response(domain, hostname)
            write_log("auth", f"PTR | {domain} → {hostname}, Signature: {signature}")
            response["ip"] = hostname
            response["signature"] = signature

    except Exception as e:
        write_log("auth", f"Erreur : {e}")
        response["ip"] = "0.0.0.0"
        response["signature"] = "INVALID"

    s.sendto(json.dumps(response).encode(), addr)
    finalize_resolution("auth")


