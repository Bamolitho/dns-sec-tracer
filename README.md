# DNSSECTRACER

> _Ce projet implémente une simulation pédagogique de la résolution DNS récursive avec vérification DNSSEC. L’objectif est de visualiser, étape par étape, comment un résolveur DNS obtient une réponse vérifiée depuis les serveurs racines jusqu’au serveur faisant autorité, tout en validant les signatures DNSSEC._

---

## 🧭 Table des matières

- [📸 Démo](#-démo)
- [🚀 Fonctionnalités principales](#-fonctionnalités-principales)
- [📦 Technologies utilisées](#-technologies-utilisées)
- [📁 Structure du projet](#-structure-du-projet)
- [Prérequis](#-prérequis)
- [Extensions possibles](#-extensions-possibles)
- [🛠️ Installation](#️-installation)
- [👤 Auteurs](#-auteurs)

---

## 📸 Démo

Voici l’infographie montrant les étapes de la résolution DNS sécurisée avec DNSSEC :  
Chaque étape valide les signatures numériques à l’aide des enregistrements DS et DNSKEY.

![DNSSEC Simulation](./A_flat-design_digital_graphic_design_infographic_t.png)

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


---

## Prérequis

- Python 3.8 ou plus récent
- Un environnement Unix/Linux ou Windows avec accès Internet
- Navigateur web moderne

---

## Extensions possibles

- 🔄 **Simuler la validation de chaînes DNSSEC corrompues**
- 🔐 Ajouter différents **algorithmes cryptographiques DNSSEC**
- 🌍 **Visualisation de logs** (avec timestamps) pour chaque requête
- 🧠 Support multilingue pour l’aspect éducatif

---

## 🛠️ Installation

```bash
# 1. Cloner le dépôt
git clone https://github.com/Bamolitho/dnssectracer.git
cd dnssectracer

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer le serveur Flask
python app.py
```
 ## 👤 Auteur

<img src="https://media.licdn.com/dms/image/v2/D4E03AQE0RS8O9YuIBQ/profile-displayphoto-shrink_800_800/profile-displayphoto-shrink_800_800/0/1731164064570?e=1752710400&v=beta&t=SL7J1e3sF2duZ7tIablBmQb0CzHfy6kArP7a2lzcw40" alt="Amolitho Baldé" width="120" style="border-radius: 50%; margin-right: 15px;" align="left">

**Amolitho Baldé**  
💼 *Étudiant en Télécommunications & Réseaux*  
🔗 [LinkedIn](https://www.linkedin.com/in/amolithobalde/) | [Portfolio](https://bamolitho.github.io/portfolio/)
<p>Université Sorbonne Paris Nord</p>

<br clear="left"/>
