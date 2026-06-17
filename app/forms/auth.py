from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User
from app.services.validation import validate_password


class RegistrationForm(FlaskForm):
    last_name = StringField("Nom", validators=[DataRequired(), Length(1, 100)])
    first_name = StringField("Prénom", validators=[DataRequired(), Length(1, 100)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(1, 255)])
    password = PasswordField(
        "Mot de passe",
        validators=[
            DataRequired(),
            Length(min=8, message="Le mot de passe doit contenir au moins 8 caractères."),
        ],
    )
    confirm_password = PasswordField(
        "Confirmer le mot de passe",
        validators=[
            DataRequired(),
            EqualTo("password", message="Les mots de passe ne correspondent pas."),
        ],
    )
    submit = SubmitField("S'inscrire")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Cet email est déjà utilisé.")

    def validate_password(self, field):
        if not validate_password(field.data):
            raise ValidationError(
                "Le mot de passe doit contenir au moins 8 caractères, "
                "une majuscule, une minuscule et un chiffre."
            )


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Mot de passe", validators=[DataRequired()])
    remember_me = BooleanField("Se souvenir de moi")
    submit = SubmitField("Se connecter")
