# Basket Stats

## Description du projet
Mon projet est de développer une application de statistiques de basketball qui permet aux entraîneurs de gérer leurs
équipes et joueurs, de créer des matchs, et de suivre les performances des joueurs à travers
des statistiques comme les points, les rebonds, les passes décisives, etc. L'objectif est de centraliser
ces données afin d'y accéder rapidement et de les analyser efficacement.


## Technologie utilisée
- [ ] Flask
- [ ] Python

## Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Installation
Installer avec pip
```python
flask --app flaskr --debug run
```
ou 
```python
flask --app flaskr run
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
## Run Flask
### Mode debug
```python
flask --app flaskr --debug run
```
### Mode develop
```python
flask --app flaskr run
```
