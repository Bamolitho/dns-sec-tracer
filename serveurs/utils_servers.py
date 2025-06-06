import time
import os

LOG_PATHS = {
    "client": "logs/dns_queries.log",
    "resolver": "logs/resolver.log",
    "root": "logs/dns_root.log",
    "tld": "logs/dns_tld.log",
    "auth": "logs/dns_auth.log"
}

def write_log(component, message):
    path = LOG_PATHS.get(component)
    if not path:
        return

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"

    # Lire l'ancien contenu pour afficher les logs du plus récent au plus ancien
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            old_content = f.read()
    else:
        old_content = ""

    # Écrire le nouveau log en haut du fichier
    with open(path, "a", encoding="utf-8") as f:
        f.write(log_entry + old_content)
