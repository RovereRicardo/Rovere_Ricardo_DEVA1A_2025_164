from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileSize
from wtforms import StringField, PasswordField, FileField, IntegerField, DateField , validators, widgets
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import HiddenField, SubmitField
from wtforms.validators import Length, NumberRange

### USER FORM ###

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired()])
    name = StringField('First and Last Name', validators=[validators.DataRequired()])
    email = StringField('Email', validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', validators=[validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match'), Length(5,150)])
    confirm = PasswordField('Confirm Password', validators=[validators.DataRequired()])
    role =  StringField('Role', validators=[validators.DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired(), Length(5,150)])
    submit = SubmitField()


### PLAYER FORM ###

class PlayerForm(FlaskForm):
    name = StringField('Name', validators=[validators.DataRequired(), Length(1, 20)])
    family_name = StringField('Family Name', validators=[validators.DataRequired(), Length(1, 20)])
    picture = FileField('Picture', validators=[FileAllowed(['jpg', 'png']), FileSize(2 * 1024 * 1024, message="File size must not exceed 2MB.")])
    number = IntegerField('Number', validators=[validators.DataRequired(), NumberRange(0, 99)])
    position = IntegerField('Position Number', validators=[validators.DataRequired(), NumberRange(1,5)])
    position_name = StringField('Position Name', validators=[validators.DataRequired(), Length(1,2)])
    height = IntegerField('Height', validators=[validators.DataRequired()])
    birthday = DateField('Birthday', validators=[validators.DataRequired()])
    nationality = StringField('Nationality', validators=[validators.DataRequired(), Length(1, 2)])
   # teams = SelectMultipleField('Teams')
    submit = SubmitField()

class DeletePlayerForm(FlaskForm):
    id_player = IntegerField('Player ID', validators=[validators.DataRequired()])
    id_team = IntegerField('Team ID', validators=[validators.DataRequired()])

### MATCH FORM ###

class RegisterMatchForm(FlaskForm):
    date = DateField('Date', validators=[validators.DataRequired()])
    id_home_team = SelectField('Home Team', validators=[validators.DataRequired()])
    id_away_team = SelectField('Away Team', validators=[validators.DataRequired()])
    submit = SubmitField('Register Match')

class DeleteMatchForm(FlaskForm):
    id_match = IntegerField('Match ID', validators=[validators.DataRequired()])

class EditMatchForm(FlaskForm):
    date_match = DateField('Date', validators=[validators.DataRequired()])
    id_home_team = SelectField('Home Team', validators=[validators.DataRequired()])
    id_away_team = SelectField('Away Team', validators=[validators.DataRequired()])
    home_score = IntegerField('Home Score', validators=[validators.DataRequired()])
    away_score = IntegerField('Away Score', validators=[validators.DataRequired()])
    submit = SubmitField('Update Match')
### TEAM FORM ###

class TeamForm(FlaskForm):
    team_name = StringField('Team Name', validators=[validators.DataRequired()])
    team_logo = FileField('Picture', validators=[FileAllowed(['jpg', 'png']), FileSize(2 * 1024 * 1024, message="File size must not exceed 2MB.")])
    address = StringField('Address', validators=[validators.DataRequired()])
    city = StringField('City', validators=[validators.DataRequired()])
    wins = IntegerField('Wins', validators=[validators.InputRequired(), validators.NumberRange(min=0)])
    loses = IntegerField('Loses', validators=[validators.InputRequired(), validators.NumberRange(min=0)])
    points = IntegerField('Points', validators=[validators.InputRequired(), validators.NumberRange(min=0)])
    submit = SubmitField('Register Team')
    id_user = HiddenField('ID User',)

class DeleteTeamForm(FlaskForm):
    id_team = IntegerField('Team ID', validators=[validators.DataRequired()])

