from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, Email, EqualTo, DataRequired, ValidationError
from slim.models import User


class RegisterForm(FlaskForm):
    def validate_user_name(self, username_to_check):
        user=User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Пользователь с таким именем уже зарегистрирован. Попробуйте другое.')

    def validate_email(self, email_to_check):
        email=User.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError('Такой адрес электронной почты занят другим пользователем. Используйте другую почту.')

    user_name=StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email=StringField(label='Email Adress:', validators=[Email(), DataRequired()])
    password_1=PasswordField(label='Create Password:', validators=[Length(min=6), DataRequired()])
    password_2=PasswordField(label='Confirm Password:', validators=[EqualTo('password_1'), DataRequired()])
    submit=SubmitField(label='Submit')

class LoginForm(FlaskForm):
    user_name=StringField(label='Имя пользователя', validators=[DataRequired()])
    password=PasswordField(label='Пароль', validators=[DataRequired()])
    submit=SubmitField(label='Подтвердить')

class PurchaseItemForm(FlaskForm):
    submit=SubmitField(label='Заказать')


class SellItemForm(FlaskForm):
    submit=SubmitField(label='Вернуть')