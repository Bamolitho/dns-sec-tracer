# DNSSECTRACER

> _DNSSECTracer est un simulateur interactif de résolution récursive DNS sécurisée en 3 étapes (Root → TLD → Authoritative), avec vérification complète de l’intégrité via DNSSEC.

---

## 🧭 Table des matières

- [📸 Démo](#-démo)
- [🚀 Fonctionnalités principales](#-fonctionnalités-principales)
- [📦 Technologies utilisées](#-technologies-utilisées)
- [📁 Structure du projet](#-structure-du-projet)
- [Prérequis](#-prérequis)
- [Extensions possibles](#-extensions-possibles)
- [🛠️ Installation](#️-installation)
- [👤 Auteur](#-auteur)

---

## 📸 Démo
L'image suivante illustre le fonctionnement d'une résolution dns récursive : 

![Fonctionnement d'une résolution dns récursive](./screenshots/dns_recursive.png)

(cf. https://www.varonis.com/fr/blog/dns-kezako)

J'ai implémenté exactement ce modèle, mais en plus, à chaque étape, des signatures numériques sont générées ou vérifiées pour garantir l'intégrité de la résolution.

1. Il y a le script ... qui permet de lancer le programme et d'ouvrir l'interface web sur le navigateur par défaut à l'adresse localhost:5000. Voici à quoi ressemble la page d'acceuil
![Page d'acceuil DNSSECTracer](./screenshots/page_acceuil_index.png)

2. On peut taper un nom de domaine quelconque dans la barre et apuiyer sur resolve pour faire une résolution
![Faire une résolution](./screenshots/une_resolution.png)
Comme résultat, on obtient une adresse IP associé au nom de domaine, une signature issue de la chaine de confiance et un message qui dit si DNSSEC est valide ou non. Au cas ou la signature n'était pas valide, un message s'afficherait sur l'interface disant qu'il y a un problème avec la validation dnssec et la résolution ne serait pas finalisée.

On peut télecharger l'historique des résolutions déjà effectuées ou bien vider complètement l'historique

3. On peut voir les étapes passées pour résoudre le nom de domaine. Je fais une résolution via 3 serveurs (ROOT, TLD, AUTORITAIRE).
![Page d'acceuil pour voir les étapes effectuées par les serveurs](./screenshots/page_acceuil_etapes.png)

On peut voir et télécharger l'hitorique des étapes passées pour toutes les résolutions faites dans la section active (... - Tous) ou uniquement pour la dernière résolution (... - Actuels).

![Choisir le serveur et le nombre de résolutions pour lesquelles on veut voir les étapes](./screenshots/selectionner_composant.png)

4. Quand on sélectionne un composant (ROOT, TLD OU AUTORITAIRE), une description sommaire de celle-ci apparait
![Description de la composante](./screenshots/composant_resolveur.png)

5. On peut alors choisir d'afficher, télécharger ou vider l'historique
![Étapes éffectuées par le résolveur pour contribuer à la dernière résolution](./screenshots/affichage_current_composant_resolveur.png)
![Étapes éffectuées par le serveur autoritaire pour contribuer à la dernière résolution](./screenshots/affichage_all_composant_auth.png)

![Télécharger l'historique des étapes de toutes les contributions du serveur autoritaire](./screenshots/telecharger_all_composant_auth.png)

Quand on veut vider une historique, il y a un message qui est affiché pour dire que cette action est irréversible.
![Vider une historique](./screenshots/attention_clear.png)


---

## 🚀 Fonctionnalités principales

- 🔍 Simulation complète de la **résolution DNS récursive**
- 🛡️ **Validation DNSSEC** à chaque niveau de la hiérarchie DNS
- 💬 **Interface web interactive** pour observer les échanges
- 🛑 Détection des erreurs de validation DNSSEC
- Système de **logs complet** pour suivre les résolutions étape par étape.

---

## 📦 Technologies utilisées

- **Langage principal** : Python 3
- **Framework web** : Flask
- **Librairies** : socket, json, time, datetime, hmac, hashlib, re, sys, os,webbrowser, subprocess, signal...
- **Frontend** : HTML, CSS 

---

## 📁 Structure du projet
```bash
/dns-sec-tracer/
├── client.py                       # Client DNS pour tester les requêtes
├── launch_dnssec_tracer.py        # Lance les serveurs + l'interface web automatiquement
│
├── serveurs/                      # Les serveurs utilisés pour la résolution 
│   ├── resolver.py                # Résolveur principal implémentant DNSSEC
│   ├── __init__.py                # Rend le dossier utilisable comme module Python
│   ├── dns_root.py                # Serveur racine DNS
│   ├── dns_tld.py                 # Serveur TLD DNS (ex: .com, .org)
│   ├── dns_auth.py                # Serveur DNS autoritaire (gère les domaines finaux)
│   ├── logs_utils.py              # Script que les serveurs utilisent pour faire leurs logs
│   └── start_dns_servers.sh       # Lance les serveurs dans des terminaux différents (utile pour déboggage; launch_dnssec_tracer.py suffit pour lancer le projet) 
│
├── dnssec/                        # Pour la vérification DNSSEC
│   ├── dnssec.py                  # Vérification des signatures et gestion des clés
│   ├── __init__.py                # Rend le dossier utilisable comme module Python
│ 
├── dns_web_app/                   # Application Web Flask
│   ├── app.py                     # Backend principal Flask
│   ├── __init__.py                # Rend le dossier utilisable comme module Python
│   ├── routes.py                  # Définit les routes de l'application web
│   ├── utils.py                   # Fonctions utilitaires (logs, formatage...)
│   ├── history.txt                # Historique des résolutions de l'utilisateur (tout)
│   ├── templates/                 # Templates HTML pour Flask
│   │   ├── index.html             # Page d'accueil
│   │   └── etapes.html            # Vue détaillée des étapes de résolution
│   └── static/                    # Fichiers statiques (CSS, JS, images…)
│       ├── style.css              # Feuille de style principale
│       └── logHandler.js          # Fichier JS utilisé par etapes.html
│
├── logs/                          # Fichiers de logs
│   ├── all_dns_client.log         # Toutes les requêtes envoyées par le client
│   ├── current_dns_client.log     # Requêtes client de la session en cours
│   ├── all_dns_resolver.log       # Tout ce qui passe par le résolveur principal
│   ├── current_dns_resolver.log   # Résolutions DNS de la session actuelle
│   ├── all_dns_root.log           # Trafic géré par le serveur root
│   ├── current_dns_root.log       # Requêtes root de la session courante
│   ├── all_dns_tld.log            # Requêtes vers les serveurs TLD
│   ├── current_dns_tld.log        # Session actuelle du serveur TLD
│   ├── all_dns_auth.log           # Résolutions finales par le serveur autoritaire
│   ├── current_dns_auth.log       # Logs en temps réel du serveur autoritaire
│
├── screenshots/                   # Contient les captures d'écrans utilisées pour la démo
│
├── requirements.txt               # Contient l'arsenal d'outils utilisés et à installer pour réaliser ce projet
└── README.md                      # Documentation et instructions du projet
```
---

## Prérequis

- Python 3.8 ou plus récent
- Un environnement Unix/Linux ou Windows avec accès Internet
- Navigateur web (Brave, Firefox, chrome...)

---

## Extensions possibles

- Ajouter d'autres types d'enregirstrements (AAAA, MX, NS...). Actuellement A, PTR et CNAME sont implémentés.
- Faire des bases de données type MYSQL ou SQLite en lieu et place des fichiers .log
- 🔐 Ajouter différents **algorithmes cryptographiques DNSSEC**
- 🧠 Support multilingue pour l’aspect éducatif
- Centraliser la recherche du reposertoire courant (BASE_DIR) et de celui de dnssec dans un script path.py

---

## 🛠️ Installation

```bash
# 1. Cloner le dépôt
git clone https://github.com/Bamolitho/dns-sec-tracer.git
cd dns-sec-tracer

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer les serveurs (DNS et Flask) et ouvrir le navigateur par défaut pour afficher l'interface web (http://localhost:5000)
python3 launch_dnssec_tracer.py
```
 ## 👤 Auteur

<img src="https://media.licdn.com/dms/image/v2/D4E03AQE0RS8O9YuIBQ/profile-displayphoto-shrink_800_800/profile-displayphoto-shrink_800_800/0/1731164064570?e=1752710400&v=beta&t=SL7J1e3sF2duZ7tIablBmQb0CzHfy6kArP7a2lzcw40" alt="Amolitho Baldé" width="120" style="border-radius: 50%; margin-right: 15px;" align="left">

**Amolitho Baldé**  
💼 *Étudiant en Télécommunications & Réseaux*  
🔗 [LinkedIn](https://www.linkedin.com/in/amolithobalde/) | [Portfolio](https://bamolitho.github.io/portfolio/)
<p>Université Sorbonne Paris Nord</p>

<br clear="left"/>
