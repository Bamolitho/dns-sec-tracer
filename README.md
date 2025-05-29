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
- 🧠 But éducatif pour comprendre DNSSEC dans un contexte concret

---

## 📦 Technologies utilisées

- **Langage principal** : Python 3
- **Framework web** : Flask
- **Librairie DNS** : dnspython
- **Frontend** : HTML, CSS (Jinja2 Templates)

---

## 📁 Structure du projet
/DNSSECTracer/
├── client.py
├── resolver.py
├── dns_root.py
├── dns_tld.py
├── dns_auth.py
├── dnssec.py
├── dns_queries.log
├── launch_dnssec_tracer.py   # Lance automatiquement les serveurs DNS et flask en background et ouvre le navigateur par défaut avec l'interface web
├── dns_web_app/
│   ├── app.py                # Le backend Flask
│   ├── __init__.py           # (Pour un vrai package)
│   ├── routes.py             # Toutes les routes Flask séparées
│   ├── utils.py              # Fonctions annexes : clean logs, formattage...
│   ├── history.txt           # Contient l'historique des résulats des résolutions de l'usager actuel
├── templates/
│   └── index.html            # Page d'accueil
│   └── etapes.html           # Vue détaillée des étapes
├── static/
│   └── style.css             # CSS 
└── README.md


---

## Prérequis

- Python 3.8 ou plus récent
- Un environnement Unix/Linux ou Windows avec accès Internet
- Navigateur web (Brave, Firefox, chrome...)

---

## Extensions possibles

- Ajouter d'autres type de record (AAAA, MX, NS...). Actuellement A, PTR et CNAME sont implémentés.
- Remplir et tenir à jour une base données contenant des vraies adresses IP
- 🔐 Ajouter différents **algorithmes cryptographiques DNSSEC**
- 🧠 Support multilingue pour l’aspect éducatif

---

## 🛠️ Installation

```bash
# 1. Cloner le dépôt
git clone https://github.com/Bamolitho/dnssectracer.git
cd DNSSECTracer

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
