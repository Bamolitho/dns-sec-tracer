"""
client.py
Objectif : Interagir avec le resolver DNS local avec DNSSEC et gestion des logs
Auteur : Amolitho BALDE
Date : 31 mai 2025
"""

import socket
import json
import re
import sys
import os

# Import des utilitaires de logs
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # BASE_DIR : dossier où se trouve ce script Python

BASE_LOG_DIR = os.path.normpath(os.path.join(BASE_DIR, ".", "serveurs")) 
sys.path.insert(0, BASE_LOG_DIR)
from logs_utils import write_log, clear_current_resolution_log, finalize_resolution

# Obtenir le chemin du dossier dnssec
DNSSEC_DIR = os.path.normpath(os.path.join(BASE_DIR, ".", "dnssec")) 
sys.path.insert(0, DNSSEC_DIR)
from dnssec import verify_response  # 🔐 Vérification DNSSEC locale

SERVER_IP = 'localhost'
SERVER_PORT = 5300  # Port du resolver DNS
server_address = (SERVER_IP, SERVER_PORT)

def ip_to_ptr(ip):
    parts = ip.split('.')
    if len(parts) != 4 or not all(p.isdigit() and 0 <= int(p) <= 255 for p in parts):
        return None
    parts.reverse()
    return '.'.join(parts) + ".in-addr.arpa."

def resolve(domain):
    clear_current_resolution_log("client")
    write_log("client", f"Début résolution pour domaine : {domain}")

    # Détecter si c’est une IP (IPv4 basique)
    ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if re.match(ip_pattern, domain):
        ptr_domain = ip_to_ptr(domain)
        if ptr_domain:
            domain = ptr_domain
            write_log("client", f"IP détectée, conversion en PTR : {domain}")
        else:
            error_msg = "❌ IP invalide."
            write_log("client", error_msg)
            return error_msg + "\n"

    if not domain.endswith("."):
        domain += "."
        write_log("client", f"FQDN forcé, domaine modifié : {domain}")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
            client.settimeout(5)
            write_log("client", f"Envoi de la requête UDP à {SERVER_IP}:{SERVER_PORT} pour {domain}")
            client.sendto(domain.encode(), server_address)
            data, _ = client.recvfrom(4096)

        decoded = data.decode()
        write_log("client", f"Réponse brute reçue : {decoded}")

        if decoded.startswith("Erreur:"):
            write_log("client", f"Erreur reçue : {decoded}")
            return f"❌ {decoded}\n"

        response = json.loads(decoded)
        ip = response.get("ip")
        signature = response.get("signature")

        if not ip or not signature:
            msg = f"❌ Réponse incomplète reçue : {response}\n"
            write_log("client", msg)
            return msg

        if verify_response(domain, ip, signature):
            msg = (
                f"✅ IP : {ip}\n"
                f"🔐 Signature DNSSEC : {signature}\n"
                "📬 Résolution réussie avec validation DNSSEC locale ✔️\n"
            )
            write_log("client", f"Validation DNSSEC réussie. IP: {ip}, Signature: {signature}")
        else:
            msg = (
                "❌ Signature DNSSEC invalide !\n"
                f"⛔ IP reçue : {ip}\n"
                f"⛔ Signature reçue : {signature}\n"
                "🔐 Vérification DNSSEC locale échouée ❌\n"
            )
            write_log("client", "Validation DNSSEC échouée.")
        return msg

    except socket.timeout:
        error_msg = "⏰ Temps d’attente dépassé. Pas de réponse du resolver."
        write_log("client", error_msg)
        return error_msg + "\n"
    except json.JSONDecodeError:
        error_msg = f"❌ Réponse reçue mais format JSON invalide : {data.decode()}"
        write_log("client", error_msg)
        return error_msg + "\n"
    except Exception as e:
        error_msg = f"❌ Erreur inattendue : {e}"
        write_log("client", error_msg)
        return error_msg + "\n"
    finally:
        finalize_resolution("client")

# 🔽 Mode ligne de commande (appelé avec un argument)
if len(sys.argv) == 2:
    domain_arg = sys.argv[1].strip()
    output = resolve(domain_arg)
    print(output)
    sys.exit(0)

# 🔁 Mode interactif
print("💻 Client DNS en cours d'exécution (Ctrl+C pour quitter)\n")
while True:
    domain = input("Nom de domaine ou IP (ou 'exit' pour quitter) : ").strip()
    if domain.lower() == "exit":
        print("🔚 Fermeture du client DNS.")
        break

    output = resolve(domain)
    print(output)
