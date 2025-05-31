# DNSSECTRACER

> _DNSSECTracer est un simulateur interactif de résolution DNS sécurisée en 3 étapes (Root → TLD → Authoritative), avec vérification complète de l’intégrité via DNSSEC.Les adresses IP sont simulées pour l’apprentissage._

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
- 📈 Affichage pédagogique étape par étape (infographie dynamique)

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
├── client.py                  # Client DNS pour tester les requêtes
├── launch_dnssec_tracer.py    # Lance les serveurs + l'interface web automatiquement
│
├── serveurs/                  # Les serveurs utilisés pour la résolution 
│   ├── resolver.py            # Résolveur principal implémentant DNSSEC
│   ├── __init__.py            # Rend le dossier utilisable comme module Python
│   ├── dns_root.py            # Serveur racine DNS
│   ├── dns_tld.py             # Serveur TLD DNS (par exemple : .com, .org)
│   ├── dns_auth.py            # Serveur DNS autoritaire (gère les domaines finaux)
│
├── dnssec/                    # Pour la vérification dnssec
│   ├── dnssec.py              # Contenant la clé utilisée pour les signatures, et permet de vérifier l'authenticité des signatures
│   ├── __init__.py            # Rend le dossier utilisable comme module Python
│ 
├── dns_web_app/               # Application Web Flask
│   ├── app.py                 # Backend principal Flask
│   ├── __init__.py            # Rend le dossier utilisable comme module Python
│   ├── routes.py              # Définit les routes de l'application web
│   ├── utils.py               # Fonctions utilitaires (logs, formatage...)
│   ├── history.txt            # Historique des résolutions de l'utilisateur
│   ├── templates/                 # Templates HTML pour Flask
│   │   ├── index.html             # Page d'accueil
│   │   └── etapes.html            # Vue détaillée des étapes de résolution
│   └── static/                    # Fichiers statiques (CSS, JS, images...)
│       └── style.css              # Feuille de style principale
│
├──logs/
├── dns_queries.log       # client
├── resolver.log          # résolveur
├── dns_root.log          # serveur root
├── dns_tld.log           # serveur TLD
├── dns_auth.log          # serveur autoritaire

│
└── README.md                  # Document de présentation du projet
```
---

## Prérequis

- Python 3.8 ou plus récent
- Un environnement Unix/Linux ou Windows avec accès Internet
- Navigateur web (Brave, Firefox, chrome...)

---

## Extensions possibles

- Ajouter d'autres types d'enregirstrements (AAAA, MX, NS...). Actuellement A, PTR et CNAME sont implémentés.
- Remplir et tenir à jour une base données contenant des vraies adresses IP
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
