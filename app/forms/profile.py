from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User
from app.services.validation import validate_password


class ProfileForm(FlaskForm):
    last_name = StringField("Nom", validators=[DataRequired(), Length(1, 100)])
    first_name = StringField("Prénom", validators=[DataRequired(), Length(1, 100)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(1, 255)])
    submit = SubmitField("Enregistrer")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_email = kwargs.get("obj").email if kwargs.get("obj") else None

    def validate_email(self, field):
        if field.data != self._original_email:
            if User.query.filter_by(email=field.data).first():
                raise ValidationError("Cet email est déjà utilisé.")


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField("Mot de passe actuel", validators=[DataRequired()])
    new_password = PasswordField(
        "Nouveau mot de passe",
        validators=[
            DataRequired(),
            Length(min=8, message="Le mot de passe doit contenir au moins 8 caractères."),
        ],
    )
    confirm_password = PasswordField(
        "Confirmer le nouveau mot de passe",
        validators=[
            DataRequired(),
            EqualTo("new_password", message="Les mots de passe ne correspondent pas."),
        ],
    )
    submit = SubmitField("Modifier le mot de passe")

    def validate_new_password(self, field):
        if not validate_password(field.data):
            raise ValidationError(
                "Le mot de passe doit contenir au moins 8 caractères, "
                "une majuscule, une minuscule et un chiffre."
            )


class DeleteAccountForm(FlaskForm):
    password = PasswordField("Mot de passe (confirmation)", validators=[DataRequired()])
    submit = SubmitField("Supprimer mon compte")
