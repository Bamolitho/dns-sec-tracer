# DNSSECTRACER

> _DNSSECTracer est un simulateur interactif de résolution récursive DNS sécurisée en 3 étapes (Root → TLD → Authoritative), avec vérification complète de l’intégrité via DNSSEC.

---

## 🧭 Table des matières

- [📸 Démo](#-démo)
- [🚀 Fonctionnalités principales](#-fonctionnalités-principales)
- [📦 Technologies utilisées](#-technologies-utilisées)
- [📁 Structure du projet](#-structure-du-projet)
- [Prérequis](#-prérequis)
- [Extensions possibles](#-Extensions-possibles)
- [🛠️ Installation](#️-installation)
- [👤 Auteur](#-auteur)

---

## 📸 Démo

Voici l’infographie montrant les étapes de la résolution DNS sécurisée avec DNSSEC :  
Chaque étape valide les signatures numériques à l’aide des enregistrements DS et DNSKEY.

![DNSSEC Simulation](./illustration.png)
> À VENIR

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
