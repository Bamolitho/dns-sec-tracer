# `logs/` – Dossier de journaux DNS

Ce répertoire contient les **fichiers de log générés automatiquement** lors de chaque tentative de résolution DNS dans le cadre de ce projet.

---

## 📌 Fonctionnement

- Chaque composant du système DNS (client, résolveur, root, TLD, serveur faisant autorité, etc.) écrit ses propres journaux dans ce dossier.
- Les logs sont générés dynamiquement à chaque requête DNS.
- Chaque fichier de log est nommé selon le rôle du serveur (par exemple : `statut_resolver.log`, `statut_dns_root.log`, `statut_dns_tld.log`, etc.). statut est soit all (pour les logs de toutes les résolutions effectuées) soit current (pour les logs de la dernière résolution effectuée)

---

## 📄 Contenu typique

Les journaux contiennent des informations essentielles comme :

- Le domaine demandé
- L’adresse IP source de la requête
- Le serveur interrogé et la réponse retournée
- La signature DNSSEC associée et un message concernant sa validité
- Les erreurs rencontrées, le cas échéant

---

## ❗Important

> ⚠️ **Ce dossier est généré automatiquement.**  
> Il n’est pas nécessaire d’y ajouter manuellement des fichiers.  
> Il est principalement destiné à des fins de **débogage**, **suivi**, et **analyse du comportement** du système DNS simulé.

---

## 🧼 Nettoyage

Tu peux effacer les anciens logs manuellement ou via l'interface web si tu veux garder ce dossier propre avant de lancer de nouvelles résolutions.


