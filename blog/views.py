# -*- coding: utf-8 -*-
from datetime import datetime
from flask_mail import Message
from resenhas import mail
from flask import (
    Blueprint, render_template, request, flash, redirect, url_for
)
from resenhas.models import Artigo
from resenhas import db
from sqlalchemy import func
from .forms import ContatoForm


blog = Blueprint(
    'blog',
    __name__,
    template_folder='templates',
    url_prefix='/'
)


@blog.route('/')
def index():
    artigos = Artigo.query.filter(
        Artigo.data_publicacao < datetime.now()
    ).filter(
        Artigo.publicado.is_(True)
    ).order_by(
        Artigo.data_publicacao
    ).limit(13).all()

    destaque = artigos[0]
    destaques = artigos[1:3]
    artigos = artigos[3:10]

    populares = Artigo.query.filter(
        Artigo.data_publicacao < datetime.now()
    ).filter(
        Artigo.publicado.is_(True)
    ).order_by(
        Artigo.cliques
    ).limit(10)

    return render_template(
        'index.html',
        destaque=destaque, destaques=destaques, artigos=artigos,
        populares=populares
    )


@blog.route('/artigo/<slug>-<id>')
def artigo(slug, id):
    try:
        artigo = Artigo.query.get(id)
    except Exception as e:
        print('Error while get artigo: {}'.format(e))

    artigo.cliques = int(artigo.cliques) + 1

    try:
        db.session.add(artigo)
        db.session.commit()
    except Exception as e:
        print('Error while increase clicks: {}'.format(e))

    # post anterior
    proximo_id = None
    anterior_id = None
    proximo = None
    anterior = None
    try:
        anterior_id = db.session.query(func.max(Artigo.id)).filter(
            Artigo.publicado.is_(True)
        ).filter(
            Artigo.data_publicacao < datetime.now()
        ).filter(
            Artigo.id < id
        ).first()[0]
    except Exception as e:
        print("Error while get previous post: {}".format(e))

    try:
        proximo_id = db.session.query(func.min(Artigo.id)).filter(
            Artigo.publicado.is_(True)
        ).filter(
            Artigo.data_publicacao < datetime.now()
        ).filter(
            Artigo.id > id
        ).group_by(Artigo.id).first()[0]
    except Exception as e:
        print("Error while get previous post: {}".format(e))

    if anterior_id:
        anterior = Artigo.query.get(anterior_id)
    if proximo_id:
        proximo = Artigo.query.get(proximo_id)

    return render_template(
        'artigo.html', artigo=artigo, anterior=anterior, proximo=proximo
    )


@blog.route('/contato', methods=['GET', 'POST'])
def contato():
    form = ContatoForm(request.form)
    if request.method == 'POST':
        # enviar mensagem via email
        msg = Message(
            form.assunto.data,
            sender=(form.nome.data, form.email.data),
            recipients=['contato@resenhasdefilmes.com']
        )
        print(msg)
        msg.body = form.mensagem.data
        try:
            with mail.connect() as conn:
                conn.send(msg)
            flash('Mensagem enviada com sucesso!', 'success')
        except Exception as e:
            print("Erro ao enviar mensagem: {}".format(e))

        redirect(url_for('blog.index'))
    return render_template('contato.html', form=form)


@blog.context_processor
def artigos_recentes():
    recentes = Artigo.query.filter(
        Artigo.data_publicacao < datetime.now()
    ).filter(
        Artigo.publicado.is_(True)
    ).order_by(Artigo.data_publicacao).limit(4)
    return {'artigos_recentes': recentes}


@blog.context_processor
def artigos_populares():
    populares = Artigo.query.filter(
        Artigo.data_publicacao < datetime.now()
    ).filter(
        Artigo.publicado.is_(True)
    ).order_by(Artigo.cliques).limit(4)
    return {'artigos_populares': populares}
