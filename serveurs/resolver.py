"""
    resolver.py
    Objectif : Résolution DNS récursive avec vérification DNSSEC simulée à chaque niveau
    Auteur : Amolitho BALDE
    Date : 31 mai 2025
"""

import json
import time
import sys
import os
import socket

from logs_utils import write_log, clear_current_resolution_log, finalize_resolution

DNSSEC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../dnssec"))
sys.path.insert(0, DNSSEC_DIR)
from dnssec import verify_response  # Import de la vérification DNSSEC

CACHE = {}  # Format : domain -> (ip, signature, expiration)
TTL = 30  # Durée de vie du cache en secondes

def log_resolution_step(role, message):
    write_log(role, message)

def forward_request(server, port, query):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(query.encode(), (server, port))
        data, _ = s.recvfrom(1024)
        return json.loads(data.decode())

def verify_dnssec_step(domain, ip, signature, niveau):
    if not verify_response(domain, ip, signature):
        log_resolution_step("resolver", f"Signature DNSSEC invalide au niveau {niveau} pour {domain}")
        finalize_resolution("resolver")
        return False
    log_resolution_step("resolver", f"DNSSEC valide au niveau {niveau} pour {domain}")
    return True

def resolve_domain(domain):
    now = time.time()
    role = "resolver"

    clear_current_resolution_log(role)
    log_resolution_step(role, f"Début résolution pour {domain}")

    if domain in CACHE:
        ip, signature, expire_time = CACHE[domain]
        if now < expire_time:
            log_resolution_step(role, f"Cache HIT pour {domain} → IP : {ip}")
            finalize_resolution(role)
            return {"ip": ip, "signature": signature}
        else:
            log_resolution_step(role, f"Cache EXPIRE pour {domain}")
            del CACHE[domain]

    log_resolution_step(role, f"Résolution réseau pour {domain}")

    # Résolution inverse
    if domain.endswith(".in-addr.arpa."):
        auth_response = forward_request("localhost", 5303, domain)
        ip = auth_response.get("ip")
        signature = auth_response.get("signature")

        if ip == "0.0.0.0":
            log_resolution_step(role, f"Domaine inversé non trouvé pour {domain}")
            finalize_resolution(role)
            return {"ip": "0.0.0.0", "signature": "INVALID"}

        if not verify_dnssec_step(domain, ip, signature, "inverse"):
            return {"ip": "0.0.0.0", "signature": "INVALID"}

        CACHE[domain] = (ip, signature, now + TTL)
        finalize_resolution(role)
        return {"ip": ip, "signature": signature}

    # Étape 1 : ROOT
    root_response = forward_request("localhost", 5301, domain)
    ip = root_response.get("ip")
    signature = root_response.get("signature")

    if ip == "0.0.0.0" or root_response.get("port", 0) == 0:
        log_resolution_step(role, f"Erreur : Root ne connaît pas ce domaine {domain}")
        finalize_resolution(role)
        return {"ip": "0.0.0.0", "signature": "INVALID"}

    if not verify_dnssec_step(domain, ip, signature, "root"):
        return {"ip": "0.0.0.0", "signature": "INVALID"}

    # Étape 2 : TLD
    tld_response = forward_request(ip, root_response["port"], domain)
    ip = tld_response.get("ip")
    signature = tld_response.get("signature")

    if ip == "0.0.0.0" or tld_response.get("port", 0) == 0:
        log_resolution_step(role, f"Erreur : TLD ne connaît pas ce domaine {domain}")
        finalize_resolution(role)
        return {"ip": "0.0.0.0", "signature": "INVALID"}

    if not verify_dnssec_step(domain, ip, signature, "tld"):
        return {"ip": "0.0.0.0", "signature": "INVALID"}

    # Étape 3 : Authoritative
    auth_response = forward_request(ip, tld_response["port"], domain)

    while "cname" in auth_response:
        cname = auth_response["cname"]
        log_resolution_step(role, f"CNAME détecté : {domain} → {cname}")
        domain = cname

        root_response = forward_request("localhost", 5301, domain)
        if not verify_dnssec_step(domain, root_response.get("ip"), root_response.get("signature"), "root"):
            return {"ip": "0.0.0.0", "signature": "INVALID"}

        tld_response = forward_request(root_response["ip"], root_response["port"], domain)
        if not verify_dnssec_step(domain, tld_response.get("ip"), tld_response.get("signature"), "tld"):
            return {"ip": "0.0.0.0", "signature": "INVALID"}

        auth_response = forward_request(tld_response["ip"], tld_response["port"], domain)

    ip = auth_response.get("ip")
    signature = auth_response.get("signature")

    if ip == "0.0.0.0":
        log_resolution_step(role, f"Domaine non trouvé pour {domain}")
        finalize_resolution(role)
        return {"ip": "0.0.0.0", "signature": "INVALID"}

    if not verify_dnssec_step(domain, ip, signature, "auth"):
        return {"ip": "0.0.0.0", "signature": "INVALID"}

    CACHE[domain] = (ip, signature, now + TTL)
    log_resolution_step(role, f"Résolution réussie pour {domain} → IP: {ip}")
    finalize_resolution(role)
    return {"ip": ip, "signature": signature}

def main():
    resolver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    resolver.bind(('localhost', 5300))
    print("[Resolver] En écoute sur port 5300...")

    while True:
        data, addr = resolver.recvfrom(1024)
        domain = data.decode().strip()

        if not domain.endswith("."):
            domain += "."

        response = resolve_domain(domain)

        if response["ip"] == "0.0.0.0":
            resolver.sendto(b"Erreur: domaine non trouve", addr)
            continue

        if response["signature"] == "INVALID":
            resolver.sendto(b"Erreur: signature DNSSEC invalide", addr)
            continue

        resolver.sendto(json.dumps(response).encode(), addr)

if __name__ == "__main__":
    main()
