"""
    app.py
    Objectif : Lancer l'application Flask en important et en enregistrant les routes définies dans routes.py.
    Auteur : Amolitho BALDE
    Date : 31 mai 2025
"""


from flask import Flask
from routes import main_routes

app = Flask(__name__)
app.register_blueprint(main_routes)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, port=5000)

