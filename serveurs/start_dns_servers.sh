#!/bin/bash

# Chemin du dossier contenant les scripts
PROJECT_DIR="~/Documents/Projets/DNSSECTracer/serveurs" # À adapter aux besoins

# Fonction pour lancer un terminal selon l'OS et l'environnement
open_terminal() {
    local title=$1
    local command=$2

    if command -v gnome-terminal &>/dev/null; then
        gnome-terminal --title="$title" -- bash -c "$command; exec bash"
    elif command -v xterm &>/dev/null; then
        xterm -T "$title" -e "$command"
    elif command -v konsole &>/dev/null; then
        konsole --new-tab -p tabtitle="$title" -e bash -c "$command"
    else
        echo "❌ Aucun terminal compatible trouvé. Lance les scripts manuellement."
        exit 1
    fi
}

echo "🚀 Lancement des serveurs DNS..."

open_terminal "Root DNS"      "python3 $PROJECT_DIR/dns_root.py"
open_terminal "TLD DNS"       "python3 $PROJECT_DIR/dns_tld.py"
open_terminal "Auth DNS"      "python3 $PROJECT_DIR/dns_auth.py"
open_terminal "Resolver"      "python3 $PROJECT_DIR/resolver.py"

echo "✅ Tous les serveurs ont été lancés dans des terminaux séparés."
