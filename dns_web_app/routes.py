"""
    routes.py
    Objectif : Définir les routes Flask permettant la gestion de la résolution DNS, l'affichage des étapes de résolution, et la manipulation des fichiers de logs.
    Auteur : Amolitho BALDE
    Date : 31 mai 2025
"""

from flask import Blueprint, render_template, request, jsonify, send_file, abort, Response
from utils import resolve_domain, clear_log_file, read_log_file
import os

main_routes = Blueprint('main', __name__)
etapes_resolveur = []

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_LOG_DIR = os.path.normpath(os.path.join(BASE_DIR, "..", "logs"))
os.makedirs(BASE_LOG_DIR, exist_ok=True)

LOG_PATHS = {
    "client.all": os.path.join(BASE_LOG_DIR, "all_dns_client.log"),
    "client.current": os.path.join(BASE_LOG_DIR, "current_dns_client.log"),
    "resolveur.all": os.path.join(BASE_LOG_DIR, "all_dns_resolver.log"),
    "resolveur.current": os.path.join(BASE_LOG_DIR, "current_dns_resolver.log"),
    "root.all": os.path.join(BASE_LOG_DIR, "all_dns_root.log"),
    "root.current": os.path.join(BASE_LOG_DIR, "current_dns_root.log"),
    "tld.all": os.path.join(BASE_LOG_DIR, "all_dns_tld.log"),
    "tld.current": os.path.join(BASE_LOG_DIR, "current_dns_tld.log"),
    "autoritaire.all": os.path.join(BASE_LOG_DIR, "all_dns_auth.log"),
    "autoritaire.current": os.path.join(BASE_LOG_DIR, "current_dns_auth.log"),
}

GLOBAL_LOGS = {
    "current": os.path.join(BASE_LOG_DIR, "current_resolution.log"),
    "all": os.path.join(BASE_LOG_DIR, "all_resolutions.log"),
}

@main_routes.route('/')
def index():
    return render_template('index.html')

@main_routes.route('/etapes')
def voir_etapes():
    return render_template('etapes.html', etapes=etapes_resolveur)

@main_routes.route('/resolve', methods=['POST'])
def resolve():
    domain = request.form.get('domain', '').strip()
    if not domain:
        return jsonify({"error": "Champ vide"}), 400
    try:
        etapes_resolveur.clear()
        etapes_resolveur.append(f"🔍 Résolution demandée pour : {domain}")
        result = resolve_domain(domain, etapes_resolveur)
        etapes_resolveur.append("✅ Résolution terminée.")
        return jsonify(result)
    except Exception as e:
        etapes_resolveur.append(f"❌ Erreur : {str(e)}")
        return jsonify({"error": str(e)}), 500

@main_routes.route('/clear_history', methods=['POST'])
def clear_history():
    clear_log_file()
    return "🧹 Historique effacé."

@main_routes.route('/save_history', methods=['GET'])
def save_history():
    return read_log_file()

@main_routes.route("/logs/<component>")
def get_component_log(component):
    path = LOG_PATHS.get(component)
    if not path or not os.path.exists(path):
        return f"⚠️ Aucune trace disponible pour : {component}", 404
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    return Response(content, mimetype='text/plain; charset=utf-8')

@main_routes.route("/logs/<component>/download")
def download_log(component):
    path = LOG_PATHS.get(component)
    if not path or not os.path.exists(path):
        abort(404)
    return send_file(path, as_attachment=True)

@main_routes.route("/logs/clear_all", methods=["POST"])
def clear_all_logs():
    for path in LOG_PATHS.values():
        if os.path.exists(path):
            open(path, "w", encoding="utf-8").close()
    return "✅ Tous les logs des composants ont été vidés."

@main_routes.route('/logs/current')
def get_current_resolution_log():
    path = GLOBAL_LOGS["current"]
    if not os.path.exists(path):
        return "⚠️ Aucun log de résolution en cours disponible.", 404
    with open(path, "r", encoding="utf-8") as f:
        return Response(f.read(), mimetype='text/plain; charset=utf-8')

@main_routes.route('/logs/all')
def get_all_resolutions_log():
    path = GLOBAL_LOGS["all"]
    if not os.path.exists(path):
        return "⚠️ Aucun historique trouvé.", 404
    with open(path, "r", encoding="utf-8") as f:
        return Response(f.read(), mimetype='text/plain; charset=utf-8')

@main_routes.route('/logs/current/download')
def download_current_resolution_log():
    path = GLOBAL_LOGS["current"]
    if not os.path.exists(path):
        abort(404)
    return send_file(path, as_attachment=True)

@main_routes.route('/logs/all/download')
def download_all_resolutions_log():
    path = GLOBAL_LOGS["all"]
    if not os.path.exists(path):
        abort(404)
    return send_file(path, as_attachment=True)

@main_routes.route('/logs/clear_global', methods=['POST'])
def clear_global_logs():
    for path in GLOBAL_LOGS.values():
        if os.path.exists(path):
            open(path, "w", encoding="utf-8").close()
    return "🧹 Fichiers globaux vidés avec succès."
