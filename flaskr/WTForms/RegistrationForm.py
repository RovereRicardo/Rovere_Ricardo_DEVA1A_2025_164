
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, FileField, IntegerField, DateField , validators
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import HiddenField, SubmitField, URLField
from wtforms.validators import Length, NumberRange, ValidationError


def file_size_limit(max_size):
    def _file_size_limit(form, field):
        if field.data:
            file_size = len(field.data.read())
            field.data.seek(0)  # Reset file pointer after reading
            if file_size > max_size:
                raise ValidationError(f"File size must not exceed {max_size / 1024 / 1024:.2f} MB.")
    return _file_size_limit

### USER FORM ###

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired()])
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

class RegisterPlayerForm(FlaskForm):
    name = StringField('Name', validators=[validators.DataRequired(), Length(1, 20)])
    family_name = StringField('Family Name', validators=[validators.DataRequired(), Length(1, 20)])
    picture = FileField('Picture', validators=[FileAllowed(['jpg', 'png']), file_size_limit(1 * 1024 * 1024)])
    number = IntegerField('Number', validators=[validators.DataRequired(), NumberRange(0, 99)])
    position = IntegerField('Position Number', validators=[validators.DataRequired(), NumberRange(1,5)])
    position_name = StringField('Position Name', validators=[validators.DataRequired(), Length(1,2)])
    height = IntegerField('Height', validators=[validators.DataRequired()])
    birthday = DateField('Birthday', validators=[validators.DataRequired()])
    nationality = StringField('Nationality', validators=[validators.DataRequired(), Length(1, 2)])
    submit = SubmitField()

class EditPlayerForm(FlaskForm):
    name = StringField('Name', validators=[validators.DataRequired()])
    family_name = StringField('Family Name', validators=[validators.DataRequired()])
    number = IntegerField('Number', validators=[validators.DataRequired(), validators.NumberRange(min=00, max=99)])
    position = IntegerField('Position', validators=[validators.DataRequired(), validators.NumberRange(min=1, max=5)])
    position_name = StringField('Position Name', validators=[validators.DataRequired(), validators.Length(min=1, max=2)])
    height = IntegerField('Height', validators=[validators.DataRequired()])
    birthday = DateField('Birthday', validators=[validators.DataRequired()])
    nationality = StringField('Nationality', validators=[validators.DataRequired(), validators.Length(min=1, max=2)])
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

class RegisterTeamForm(FlaskForm):
    team_name = StringField('Team Name', validators=[validators.DataRequired()])
    team_logo = FileField('Picture', validators=[FileAllowed(['jpg', 'png']), file_size_limit(5 * 1024 * 1024)])
    address = StringField('Address', validators=[validators.DataRequired()])
    city = StringField('City', validators=[validators.DataRequired()])
    wins = IntegerField('Wins', validators=[validators.InputRequired(), validators.NumberRange(min=0)])
    loses = IntegerField('Loses', validators=[validators.InputRequired(), validators.NumberRange(min=0)])
    draws = IntegerField('Draws', validators=[validators.InputRequired(), validators.NumberRange(min=0)])
    points = IntegerField('Points', validators=[validators.InputRequired(), validators.NumberRange(min=0)])
    submit = SubmitField('Register Team')
    id_user = HiddenField('ID User', validators=[validators.DataRequired()])

class DeleteTeamForm(FlaskForm):
    id_team = IntegerField('Team ID', validators=[validators.DataRequired()])

class EditTeamForm(FlaskForm):
    team_name = StringField('Team Name', validators=[validators.DataRequired()])
    team_logo = IntegerField('Team Logo', validators=[validators.DataRequired()])
    address = StringField('Address', validators=[validators.DataRequired()])
    city = StringField('City', validators=[validators.DataRequired()])
    wins = IntegerField('Wins', validators=[validators.InputRequired(), validators.NumberRange(min=0)])
    loses = IntegerField('Loses', validators=[validators.InputRequired(), validators.NumberRange(min=0)])
    draws = IntegerField('Draws', validators=[validators.InputRequired(), validators.NumberRange(min=0)])
    points = IntegerField('Points', validators=[validators.InputRequired(), validators.NumberRange(min=0)])
    submit = SubmitField('Edit Team')