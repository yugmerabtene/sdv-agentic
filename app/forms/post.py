from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    content = TextAreaField(
        "Contenu",
        validators=[
            DataRequired(),
            Length(
                min=1,
                max=2000,
                message="Le contenu doit faire entre 1 et 2000 caractères.",
            ),
        ],
    )
    submit = SubmitField("Publier")
