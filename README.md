# 🏡 HBnB - Holberton School AirBnB Clone

![Holberton](https://img.shields.io/badge/Holberton-School-red?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-API-lightgrey?style=flat-square&logo=flask)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?style=flat-square&logo=sqlite)

## 📖 Description

**HBnB** est une application web complète, calquée sur le modèle d'AirBnB. Ce projet constitue la pierre angulaire du cursus **Holberton School**, visant à nous faire construire une application de bout en bout ("Full-Stack").

L'objectif de ce projet est de comprendre et d'implémenter l'ensemble de l'architecture d'une application web RESTful moderne : de la modélisation des données persistantes jusqu'à l'authentification sécurisée, en passant par la création d'une interface web dynamique et "responsive".

Ce dépôt regroupe de manière itérative l'évolution de notre application, divisée en 4 grandes parties, allant de la conception abstraite à la réalisation finale incluant le Front-End.

---

## 🏗️ Architecture du Projet

Le projet a été développé de manière modulaire, en respectant plusieurs couches d'abstraction ("Layered Architecture") et les principes directeurs de la **Clean Architecture** (Façade, Référentiels, Modèles) :

1. **Couche de Présentation** : L'interface utilisateur (HTML/CSS/JS) et l'API (Routage avec Flask).
2. **Couche Logique (Business Logic)** : Traitement des données, vérifications, gestion de l'authentification (JWT, bcrypt) via une Façade (Facade Pattern).
3. **Couche de Persistance** : Sauvegarde des données à travers le "Repository Pattern" (en mémoire pour la partie 2, et via SQLite/Bases de données relationnelles pour les parties 3 et 4).

### 📂 Structure du dépôt

L'évolution du projet se fait étape par étape dans 4 dossiers distincts :

*   **`part1/` : Conception (Design & Architecture)**
    *   Diagrammes UML et package diagram.
    *   Planification de l'architecture logicielle globale de l'application.
*   **`part2/` : Modèles & Façade (Logique Métier)**
    *   Création des classes (Modèles) principales : `User`, `Place`, `Review`, `Amenity`.
    *   Implémentation du pattern Façade et d'un référentiel de stockage en mémoire d'API.
*   **`part3/` : Persistance & Base de Données**
    *   Intégration d'une vraie base de données.
    *   Mise en place de l'authentification JWT (JSON Web Tokens) et hachage des mots de passe.
*   **`part4/` : Interface Web Front-end**
    *   Liaison de notre API Rest avec une interface cliente dynamique.
    *   Pages de connexion (`login.html`), affichage dynamique de tous les lieux (`index.html`) et détails d'un lieu (`place.html`).

---

## 🛠️ Technologies Utilisées

*   **Langage :** Python 3 (Backend), JavaScript (Frontend)
*   **Framework Web :** Flask, Flask-RESTX (API)
*   **Base de données :** SQLite
*   **Authentification et Sécurité :** JWT (JSON Web Tokens), Bcrypt
*   **Interface :** HTML5, CSS3, DOM Manipulation (Fetch API)

---

## 🚀 Installation & Lancement

### 1. Cloner le projet

```bash
git clone https://github.com/add1ktion/holbertonschool-hbnb.git
cd holbertonschool-hbnb/part4/hbnb
```

### 2. Configurer l'environnement virtuel

Il est fortement recommandé d'utiliser un environnement virtuel.

```bash
python3 -m venv venv
source venv/bin/activate
# Sur Windows: venv\Scripts\activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Lancer l'application

Lancez le serveur Flask :

```bash
python3 run.py
```

Le serveur démarrera en local et l'interface Web ou l'API sera accessible sur `http://127.0.0.1:5000` (ou port spécifié).

---

## 👥 Auteurs

Ce projet a été réalisé en collaboration, dans la rigueur requise par le programme **Holberton School** :

*   **Antoine** : [GitHub Profile](https://github.com/add1ktion)
*   **Alexis** : [GitHub Profile](https://github.com/loties1533)

> Projet réalisé dans le cadre de la cohorte d'Holberton School.