from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class DepartForm(FlaskForm):
    title = StringField('Title of Department', validators=[DataRequired()])
    chief = IntegerField('Chief', validators=[DataRequired()])
    members = StringField('Members', validators=[DataRequired()])
    email = StringField('Department Email', validators=[DataRequired()])
    submit = SubmitField('Добавить')
