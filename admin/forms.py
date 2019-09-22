from flask_wtf import FlaskForm
from wtforms import (
    StringField, TextAreaField, SubmitField, BooleanField, DateTimeField,
    FileField, HiddenField
)
from wtforms.validators import DataRequired
from datetime import datetime


class ArtigoForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired()])
    conteudo = TextAreaField('Conteúdo', id='summernote')
    publicado = BooleanField('Publicado')
    data_publicacao = DateTimeField(
        'Data da Publicação',
        validators=[DataRequired()],
        default=datetime.now(),
        format='%d/%m/%Y %H:%M')
    capa = FileField()
    submit = SubmitField('Enviar')


class ArtigoEditForm(ArtigoForm):
    id = HiddenField()
