from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    id_austro = StringField('ID астронавта', validators=[DataRequired()])
    password_austro = PasswordField('Пароль астронавта', validators=[DataRequired()])
    id_captain = StringField('ID капитана', validators=[DataRequired()])
    password_captain = PasswordField('Пароль капитана', validators=[DataRequired()])
    submit = SubmitField('Доступ')