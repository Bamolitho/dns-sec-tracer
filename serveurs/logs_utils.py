import time
import os

# BASE_DIR : dossier où se trouve ce script Python
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Dossier logs relatif au script
BASE_LOG_DIR = os.path.normpath(os.path.join(BASE_DIR, "..", "logs"))

# S’assure que le dossier logs existe
os.makedirs(BASE_LOG_DIR, exist_ok=True)

LOG_PATHS = {
    "client": os.path.join(BASE_LOG_DIR, "dns_client.log"),
    "resolver": os.path.join(BASE_LOG_DIR, "dns_resolver.log"),
    "root": os.path.join(BASE_LOG_DIR, "dns_root.log"),
    "tld": os.path.join(BASE_LOG_DIR, "dns_tld.log"),
    "auth": os.path.join(BASE_LOG_DIR, "dns_auth.log")
}

def current_log_path(component):
    """Retourne le chemin du fichier log courant pour un composant donné."""
    return os.path.join(BASE_LOG_DIR, f"current_dns_{component}.log")

def all_log_path(component):
    """Retourne le chemin du fichier log global pour un composant donné."""
    return os.path.join(BASE_LOG_DIR, f"all_dns_{component}.log")

def clear_current_resolution_log(component):
    """Vide le fichier temporaire des logs de résolution courante pour le composant."""
    path = current_log_path(component)
    with open(path, "w", encoding="utf-8") as f:
        f.write("")

def write_log(component, message):
    """Écrit dans le fichier du composant ET dans le fichier temporaire ET dans le fichier global, en ajout à la fin du fichier."""

    path = LOG_PATHS.get(component)
    if not path:
        # Composant inconnu, on peut lever une erreur ou ignorer
        return

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{component.upper()}] {message}\n"

    # # 1. Ajoute à la fin du fichier du composant (append)
    # with open(path, "a", encoding="utf-8") as f:
    #     f.write(log_entry)

    # 2. Ajoute à la fin du fichier de la résolution courante spécifique au composant (append)
    with open(current_log_path(component), "a", encoding="utf-8") as f:
        f.write(log_entry)

    # 3. Ajoute à la fin du fichier global spécifique au composant (append)
    with open(all_log_path(component), "a", encoding="utf-8") as f:
        f.write(log_entry)

def finalize_resolution(component):
    """Ajoute une ligne vide pour séparer les résolutions dans le fichier global du composant."""
    with open(all_log_path(component), "a", encoding="utf-8") as f:
        f.write("\n")
