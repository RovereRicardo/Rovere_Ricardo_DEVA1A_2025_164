# Basket Stats

### Cahier des charges
[PDF Cahier des charges](Rovere_Paulo_DEVA1A_Cahier_Charges.pdf)

## Description du projet
Mon projet est de développer une application de statistiques de basketball qui permet aux entraîneurs de gérer leurs
équipes et joueurs, de créer des matchs, et de suivre les performances des joueurs à travers
des statistiques comme les points, les rebonds, les passes décisives, etc. L'objectif est de centraliser
ces données afin d'y accéder rapidement et de les analyser efficacement.


## Technologie utilisée
- [ ] Flask <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white">
- [ ] Python <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue">
- [ ] Bootstrap <img src="https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white">
- [ ] Pycharm <img src="https://img.shields.io/badge/PyCharm-000000.svg?&style=for-the-badge&logo=PyCharm&logoColor=white">


## Installation
### Clone the repo
```python
https://github.com/RovereRicardo/Rovere_Ricardo_DEVA1A_2025_164.git
```
### Install Python 
```python
Download from official website : https://www.python.org/downloads/windows/
After  installing in the command line type : "python -V" This commands will tell if Python is installed
```

### Install pip
```python
py get-pip.py 
```
Run with debug mode :
```python
When everything is installed open the repo and type on the terminal : 
flask --app flaskr --debug run
```
Run without debug mode :
```python
flask --app flaskr run
```

## How to run the Application
```text
If you wish to change the Host, User or Password: 
Go to the .env file and change the credentials you wish.
```
<img src="./flaskr/Doc/env.jpg">

### Run
```text
You can either run the application by typing :
flask --app flaskr  run 
From the flaskr folder.
```
or
```text
Right click on the __init__.py file and choose Run [CTRL+SHIFT+F10]
```
<img src="./flaskr/Doc/run.png">

### APP Login 
```text
Username: admin
password: admin
```

## Flask Application Structure 
```
.
|──────flaskr/
| |────controller/
| | |────players.py
| | |────teams.py
| | |────user.py
| |────models/
| | |────db.py
| | |────players.py
| | |────teams.py
| | |────user.py
| |────static/
| |────bootstrap.bundle.min.js
| |────bootstrap.min.css
| | |────css/
| | | |────all.css
| | | |────brands.css
| | | |────fontawesome.css
| | | |────regular.css
| | | |────solid.css
| | | |────svg-with-js.css
| | | |────v4-font-face.css
| | | |────v4-shims.css
| | | |────v5-font-face.css
| | |────font-awesome-4.7.0/
| | |────webfonts/
| | |────user.py
| |────templates/
| | |────base.html
| | |────index.html
| | |────auth/
| | | |────login.html
| | | |────register.html
| | |────players/
| | | |────register_player.html
| | | |────update_player.html
| | | |────view_player.html
| | |────teams/
| | | |────register_team.html
| | | |────update_team.html
| | | |────view_team.html
|──────__init__.py

```
## Flask configuration
```python
def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=connection,
    )
```

## Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

### Homepage
<img src="./flaskr/Doc/homepage.png" >

### Match
<img src="./flaskr/Doc/match.png">

### Create
<img src="./flaskr/Doc/Create.png">

### View
<img src="./flaskr/Doc/playerview.png">

### TeamView
<img src="./flaskr/Doc/teamview.png">

## Contributions
### 👩‍💻 Ricardo Rovere

[<img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"> ](https://github.com/RovereRicardo)
[<img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white">](Link)

