#!/usr/bin/env python3
import os
import subprocess
import time
import webbrowser
import signal

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
SERVERS_DIR = os.path.normpath(os.path.join(PROJECT_DIR, ".", "serveurs"))
APP_DIR = os.path.normpath(os.path.join(PROJECT_DIR, ".", "dns_web_app"))

processes = []

def run_in_background(script_path):
    """Lance un script Python en arrière-plan sans ouvrir de terminal."""
    proc = subprocess.Popen(
        ["python3", script_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        preexec_fn=os.setsid  # Permet de tuer tout le groupe de processus ensuite
    )
    processes.append(proc)

def start_components():
    print("🔧 Lancement des serveurs DNS en arrière-plan...")

    servers = ['resolver.py', 'dns_root.py', 'dns_tld.py', 'dns_auth.py']
    for server in servers:
        script_path = os.path.join(SERVERS_DIR, server)
        if os.path.exists(script_path):
            run_in_background(script_path)
            print(f"✅ {server} lancé.")
        else:
            print(f"❌ Script introuvable : {server}")

    print("🚀 Lancement de l'application Flask en arrière-plan...")
    flask_app_path = os.path.join(APP_DIR, 'app.py')
    run_in_background(flask_app_path)

    time.sleep(4)  # Laisse l'appli Flask démarrer
    webbrowser.open("http://localhost:5000")

def stop_all():
    print("\n🛑 Arrêt des processus lancés...")
    for proc in processes:
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
            print(f"🔒 Processus {proc.pid} terminé.")
        except Exception as e:
            print(f"⚠️ Erreur lors de l'arrêt du processus {proc.pid}: {e}")

if __name__ == "__main__":
    print("🚦 Initialisation du système DNSSEC Tracer...")
    start_components()
    print("✅ Système opérationnel sur http://localhost:5000")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_all()
        print("👋 Arrêt complet.")
