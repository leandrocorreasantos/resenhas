# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import (
    StringField, TextAreaField, SubmitField, BooleanField, DateTimeField,
    FileField, HiddenField
)
from wtforms.validators import DataRequired
from datetime import datetime


class ArtigoForm(FlaskForm):
    titulo = StringField(u'Título', validators=[DataRequired()])
    conteudo = TextAreaField(u'Conteúdo', id='summernote')
    publicado = BooleanField('Publicado')
    data_publicacao = DateTimeField(
        u'Data da Publicação',
        validators=[DataRequired()],
        default=datetime.now(),
        format='%d/%m/%Y %H:%M:%S'
    )
    data_atualizacao = DateTimeField(
        u'Data de Atualização',
        default=datetime.now()
    )
    capa = FileField('Capa')
    list_tags = StringField('Tags')
    meta_keywords = StringField(u'Palavras-Chave')
    meta_description = StringField(u'Descrição Breve')
    submit = SubmitField('Salvar')


class ArtigoEditForm(ArtigoForm):
    id = HiddenField()
    nova_capa = FileField('Capa')
