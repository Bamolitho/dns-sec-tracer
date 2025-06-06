"""
    dnssec.py
    Objectif : Simuler une signature DNSSEC avec une clé secrète partagée
    Auteur : Amolitho BALDE
    Date : 31 mai 2025
"""

import hashlib

SECRET_KEY = "amolitho_secret"

def sign_response(domain, ip):
    """Crée une signature SHA256 basée sur domaine, IP et la clé secrète."""
    message = f"{domain}:{ip}:{SECRET_KEY}"
    return hashlib.sha256(message.encode()).hexdigest()

def verify_response(domain, ip, signature):
    """Vérifie que la signature correspond bien à celle attendue."""
    expected_signature = sign_response(domain, ip)
    return expected_signature == signature
