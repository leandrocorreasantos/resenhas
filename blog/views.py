# -*- coding: utf-8 -*-
from datetime import datetime
from flask import (
    Blueprint, render_template
)
from resenhas.models import Artigo
from resenhas import db
from sqlalchemy import func


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

    artigo.cliques += 1

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


@blog.route('/contato')
def contato():
    return render_template('contato.html')


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
