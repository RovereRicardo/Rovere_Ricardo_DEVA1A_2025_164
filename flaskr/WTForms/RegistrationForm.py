from flask_wtf.file import FileAllowed
from wtforms import Form, StringField, PasswordField, FileField, IntegerField, DateField , validators

### USER FORM ###

class RegistrationForm(Form):
    username = StringField('Username', validators=[validators.DataRequired()])
    email = StringField('Email', validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', validators=[validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password', validators=[validators.DataRequired()])
    role =  StringField('Role', validators=[validators.DataRequired()])

class LoginForm(Form):
    username = StringField('Username', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])

### PLAYER FORM ###

class RegisterPlayer(Form):
    name = StringField('Name', validators=[validators.DataRequired()])
    family_name = StringField('Family Name', validators=[validators.DataRequired()])
    picture = FileField('Picture', validators=[FileAllowed(['jpg', 'png'])])
    number = IntegerField('Number', validators=[validators.DataRequired(), validators.NumberRange(min=00, max=99)])
    position = IntegerField('Position Number', validators=[validators.DataRequired(), validators.NumberRange(min=1, max=5)])
    position_name = StringField('Position Name', validators=[validators.DataRequired(), validators.Length(min=1, max=2)])
    height = IntegerField('Height', validators=[validators.DataRequired()])
    birthday = DateField('Birthday', validators=[validators.DataRequired()])
    nationality = StringField('Nationality', validators=[validators.DataRequired(), validators.Length(min=1, max=2)])
    id_team = IntegerField('ID Team', validators=[validators.DataRequired()])

class EditPlayer(Form):
    name = StringField('Name', validators=[validators.DataRequired()])
    family_name = StringField('Family Name', validators=[validators.DataRequired()])
    number = IntegerField('Number', validators=[validators.DataRequired(), validators.NumberRange(min=00, max=99)])
    position = IntegerField('Position', validators=[validators.DataRequired(), validators.NumberRange(min=1, max=5)])
    position_name = StringField('Position Name', validators=[validators.DataRequired(), validators.Length(min=1, max=2)])
    height = IntegerField('Height', validators=[validators.DataRequired()])
    birthday = DateField('Birthday', validators=[validators.DataRequired()])
    nationality = StringField('Nationality', validators=[validators.DataRequired(), validators.Length(min=1, max=2)])

class DeletePlayer(Form):
    id_player = IntegerField('Player ID', validators=[validators.DataRequired()])
    id_team = IntegerField('Team ID', validators=[validators.DataRequired()])

### MATCH FORM ###

class RegisterMatch(Form):
    date = DateField('Date', validators=[validators.DataRequired()])
    id_home_team = IntegerField('Home Team', validators=[validators.DataRequired()])
    id_away_team = IntegerField('Away Team', validators=[validators.DataRequired()])

class DeleteMatch(Form):
    id_match = IntegerField('Match ID', validators=[validators.DataRequired()])

class EditMatch(Form):
    date_match = DateField('Date', validators=[validators.DataRequired()])
    id_home_team = IntegerField('Home Team', validators=[validators.DataRequired()])
    id_away_team = IntegerField('Away Team', validators=[validators.DataRequired()])
    home_score = IntegerField('Home Score', validators=[validators.DataRequired()])
    away_score = IntegerField('Away Score', validators=[validators.DataRequired()])

### TEAM FORM ###

class RegisterTeam(Form):
    team_name = StringField('Team Name', validators=[validators.DataRequired()])
    team_logo = IntegerField('Team Logo', validators=[validators.DataRequired()])
    address = StringField('Address', validators=[validators.DataRequired()])
    city = StringField('City', validators=[validators.InputRequired()])
    wins = IntegerField('Wins', validators=[validators.InputRequired(), validators.NumberRange(min=0)])
    loses = IntegerField('Loses', validators=[validators.InputRequired(), validators.NumberRange(min=0)])
    draws = IntegerField('Draws', validators=[validators.InputRequired(), validators.NumberRange(min=0)])
    points = IntegerField('Points', validators=[validators.InputRequired(), validators.NumberRange(min=0)])
    id_user = IntegerField('ID User', validators=[validators.DataRequired()])

class DeleteTeam(Form):
    id_team = IntegerField('Team ID', validators=[validators.DataRequired()])

class EditTeam(Form):
    team_name = StringField('Team Name', validators=[validators.DataRequired()])
    team_logo = IntegerField('Team Logo', validators=[validators.DataRequired()])
    address = StringField('Address', validators=[validators.DataRequired()])
    city = StringField('City', validators=[validators.DataRequired()])
    wins = IntegerField('Wins', validators=[validators.InputRequired(), validators.NumberRange(min=0)])
    loses = IntegerField('Loses', validators=[validators.InputRequired(), validators.NumberRange(min=0)])
    draws = IntegerField('Draws', validators=[validators.InputRequired(), validators.NumberRange(min=0)])
    points = IntegerField('Points', validators=[validators.InputRequired(), validators.NumberRange(min=0)])