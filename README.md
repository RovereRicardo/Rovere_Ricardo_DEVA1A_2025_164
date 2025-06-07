# 🏀 Basket Stats

📊 Application de statistiques de basketball pour les entraîneurs : gestion d'équipes, suivi des performances, visualisation des matchs et bien plus.

---

## 📚 Table des matières
- [📌 Description du projet](#-description-du-projet)
- [🛠 Technologies utilisées](#-technologies-utilisées)
- [✨ Fonctionnalités](#-fonctionnalités)
- [🔧 Installation](#-installation)
- [🚀 Lancement de l'application](#-lancement-de-lapplication)
- [🗂 Structure de l'application Flask](#-structure-de-lapplication-flask)
- [👥 Comptes de connexion](#-comptes-de-connexion)
- [🖼 Visuels](#-visuels)
- [🧑‍💻 Contributions](#-contributions)

---

## 📌 Description du projet

**Basket Stats** est une application web permettant aux entraîneurs de :
- Gérer leurs équipes et joueurs
- Enregistrer et suivre les matchs
- Collecter et visualiser des statistiques comme les points, passes, rebonds, etc.

L’objectif est de centraliser toutes les données pour une meilleure analyse et prise de décision.

---

## 🛠 Technologies utilisées

- ![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
- ![Flask](https://img.shields.io/badge/Flask-000000?logo=flask&logoColor=white)
- ![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?logo=bootstrap&logoColor=white)
- ![PyCharm](https://img.shields.io/badge/PyCharm-000000?logo=pycharm&logoColor=white)

---

## ✨ Fonctionnalités

- ✅ Création et édition des matchs
- ✅ Enregistrement des équipes et des joueurs
- ✅ Saisie des statistiques (points, rebonds, passes, etc.)
- ✅ Classements et graphiques par joueur ou équipe
- ✅ Interface dédiée aux coachs et à l’admin
- ✅ Interface responsive avec Bootstrap

---

## 🔧 Installation

```bash
# 1. Cloner le dépôt
git clone https://github.com/RovereRicardo/Rovere_Ricardo_DEVA1A_2025_164.git
cd Rovere_Ricardo_DEVA1A_2025_164

# 2. Créer un environnement virtuel
python -m venv venv            # Windows
# ou
python3.12 -m venv venv        # macOS/Linux

# 3. Activer l'environnement virtuel
venv\Scripts\activate          # Windows
# ou
source venv/bin/activate       # macOS/Linux

# 4. Installer les dépendances
pip install -r requirements.txt
```

## 🚀 Lancement de l'application

# Lancer en mode développement (debug)
```
flask --app flaskr --debug run
```
# Ou en mode normal
```
flask --app flaskr run
```
```
Depuis PyCharm
👉 Clic droit sur run_app.py → Exécuter
```
<img src="./flaskr/Doc/run.png">

## 🗂 Structure de l'application Flask
```
.
├── run_app.py
├── .env
├── README.md
├── Rovere_Paulo_DEVA1A_Cahier_Charges.pdf
└── flaskr/
    ├── controller/
    │   ├── matchs.py
    │   ├── players.py
    │   ├── stats.py
    │   ├── teams.py
    │   └── user.py
    ├── database/
    │   ├── __init__.py
    │   ├── db.py
    │   └── rovere_ricardo_deva1a_basketstats_164_2025.sql
    ├── models/
    │   ├── matchs.py
    │   ├── players.py
    │   ├── stats.py
    │   ├── teams.py
    │   ├── total.py
    │   └── user.py
    ├── templates/
    │   ├── base.html
    │   ├── index.html
    │   ├── auth/
    │   │   ├── login.html
    │   │   └── register.html
    │   ├── macros/
    │   │   └── forms.html
    │   ├── matchs/
    │   ├── players/
    │   ├── teams/
    │   └── WTForms/
    ├── static/
    │   ├── css/
    │   └── font-awesome-4.7.0/
    └── Doc/
```
## 👥  Comptes de connexion
```
👑 Administrateur
Identifiant: admin
Mot de pass: admin
```

```
🧑‍🏫 Entraîneurs
| Équipe    | Identifiant | Mot de passe    |
| --------- |-------------| --------------- |
| Bulle     | bulle       | bullebasket     |
| Sarine    | sarine      | sarinebasket    |
| Veveyse   | veveyse     | veveysebasket   |
| Villars   | villars     | villarsbasket   |
| Payerne   | payerne     | payernebasket   |
| Fribourg  | fribourg    | fribourgbasket  |
| Courtepin | courtepin   | courtepinbasket |
| Marly     | marly       | marlybasket     |
```

## 🖼 Visuels
### 🏠 Accueil
<img src="./flaskr/Doc/homepage.png" >

### 🏀 Match
<img src="./flaskr/Doc/match.png">

### ➕ Créer un équipe
<img src="./flaskr/Doc/Create.png">

### 👤 Vue joueur
<img src="./flaskr/Doc/playerview.png">

### 👥 Vue équipe
<img src="./flaskr/Doc/teamview.png">

## 🧑‍💻 Contributions
### 👩‍💻 Ricardo Rovere

[<img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"> ](https://github.com/RovereRicardo)

