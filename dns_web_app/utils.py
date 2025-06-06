"""
    utils.py
    Objectif : Fournir les fonctions utilitaires pour exécuter le client de résolution DNS, enregistrer les résultats dans les fichiers de logs, et lire/effacer les historiques.
    Auteur : Amolitho BALDE
    Date : 31 mai 2025
"""

import subprocess
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
LOGS_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "logs"))
HISTORY_FILE = os.path.join(LOGS_DIR, "all_resolutions.log")
CURRENT_FILE = os.path.join(LOGS_DIR, "current_resolution.log")

def resolve_domain(domain, etapes_resolveur):
    try:
        client_path = os.path.abspath(os.path.join(BASE_DIR, "..", "client.py"))

        if not os.path.isfile(client_path):
            raise Exception(f"❌ Fichier client.py introuvable à : {client_path}")

        etapes_resolveur.append("🚀 Lancement du client.py...")

        result = subprocess.run(["python3", client_path, domain],
                                capture_output=True, text=True, timeout=10)

        etapes_resolveur.append("📤 Résultat reçu du client.")

        if result.returncode != 0:
            raise Exception(result.stderr.strip())

        log_entry = f"[Résolution] Domaine/IP : {domain}\nRésultat -> {result.stdout.strip()}\n"

        with open(HISTORY_FILE, "a", encoding="utf-8") as hist_f:
            hist_f.write(log_entry + "\n")

        with open(CURRENT_FILE, "w", encoding="utf-8") as cur_f:
            cur_f.write(log_entry)

        return {"result": result.stdout.strip()}

    except subprocess.TimeoutExpired:
        raise Exception("⏱️ Timeout lors de l'exécution du client.")
    except Exception as e:
        raise Exception(f"💥 Erreur de résolution : {e}")

def clear_log_file():
    """Efface les logs globaux"""
    open(HISTORY_FILE, "w", encoding="utf-8").close()
    open(CURRENT_FILE, "w", encoding="utf-8").close()

def read_log_file():
    """Lit le contenu de l'historique global"""
    if not os.path.exists(HISTORY_FILE):
        return "⚠️ Aucun historique disponible."
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return f.read()
