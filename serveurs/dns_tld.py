"""
    dns_tld.py
    Objectif : Serveur DNS TLD simulé avec signature DNSSEC
    Auteur : Amolitho BALDE
    Date : 31 mai 2025
"""
import socket
import json
import os
import sys
from logs_utils import write_log, clear_current_resolution_log, finalize_resolution

DNSSEC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../dnssec"))
sys.path.insert(0, DNSSEC_DIR)
import dnssec

HOST = "localhost"
PORT = 5302

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))

print("[TLD DNS] En écoute sur port 5302...")

while True:
    data, addr = s.recvfrom(1024)
    domain = data.decode().strip()

    clear_current_resolution_log("tld")

    if not domain.endswith("."):
        domain += "."

    try:
        tld = domain.split('.')[-2] + "."
    except IndexError:
        tld = ""

    ip, port = ("localhost", 5303)  # Tous vers serveur autoritaire
    signature = dnssec.sign_response(domain, ip)

    write_log("tld", f"Reçu de {addr[0]}:{addr[1]} | Domaine: {domain} → IP: {ip}, Port: {port}, Signature: {signature[:8]}...")
    finalize_resolution("tld")

    response = {
        "ip": ip,
        "port": port,
        "signature": signature
    }
    s.sendto(json.dumps(response).encode(), addr)


