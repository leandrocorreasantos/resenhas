# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import (
    StringField, TextAreaField, SubmitField
)
from wtforms.validators import DataRequired, Email


class ContatoForm(FlaskForm):
    def __init__(self, label='', **kwargs):
        super(ContatoForm, self).__init__(label, **kwargs)

    nome = StringField(u'Nome', validators=[DataRequired()])
    email = StringField(u'Email', validators=[DataRequired(), Email()])
    assunto = StringField(u'Assunto', validators=[DataRequired()])
    mensagem = TextAreaField(u'Mensagem')
    submit = SubmitField('Enviar Mensagem')
