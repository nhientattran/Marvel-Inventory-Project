from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateTimeField
from wtforms.validators import DataRequired, Optional

class UserLoginForm(FlaskForm):
    username = StringField('username', validators = [DataRequired()])
    password = PasswordField('password', validators = [DataRequired()])
    email = StringField('email', validators= [DataRequired()])
    submit_button = SubmitField()

class CharacterForm(FlaskForm):
    name = StringField('Name')
    description = StringField('Description',validators=[Optional()])
    movies_appeared = StringField('Appeared in Movies',validators=[Optional()])
    super_power = StringField('Super Power',validators=[Optional()])
    date_created = DateTimeField('Date Created',validators=[Optional()])
    submit_button = SubmitField()
