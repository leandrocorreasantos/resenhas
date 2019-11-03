import os
from sqlalchemy.sql.expression import extract
from sqlalchemy import distinct
from datetime import datetime
from flask import Flask, send_from_directory, render_template, make_response
from . import db, migrate, bootstrap, mail
from .errors.handlers import errors
from .admin.views import admin
from .blog.views import blog
from .models import User, Artigo
from flask_user import UserManager


SITE_URL = os.environ.get('SITE_URL')


def create_app(app_name='app', config_obj='resenhas.config.Config'):
    app = Flask(app_name)
    app.config.from_object(config_obj)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    bootstrap.init_app(app)
    app.register_blueprint(admin)
    app.register_blueprint(blog)
    app.register_blueprint(errors)
    user_manager = UserManager(app, db, User)  # noqa
    return app


app = create_app(__name__)


@app.route('/sitemap-<int:year>.xml')
def sitemap_by_year(year):
    artigos = Artigo.query.filter(
        Artigo.publicado.is_(True)
    ).filter(
        extract('year', Artigo.data_publicacao) == year
    ).filter(
        Artigo.data_publicacao < datetime.now()
    ).order_by(
        Artigo.data_publicacao.desc()
    ).all()
    sitemap_xml = render_template(
        'sitemap_template.xml', artigos=artigos, site=SITE_URL
    )
    response = make_response(sitemap_xml)
    response.headers['Content-Type'] = 'application/xml'

    return response


@app.route('/sitemap.xml')
def static_sitemap():
    sitemap = render_template('sitemap_static.xml', site=SITE_URL)
    response = make_response(sitemap)
    response.headers['Content-Type'] = 'application/xml'

    return response


@app.route('/sitemaps.xml')
def sitemap():
    years = Artigo.query.with_entities(
        distinct(extract('year', Artigo.data_publicacao))
    ).filter(
        Artigo.publicado.is_(True)
    ).all()
    sitemap_xml = render_template(
        'sitemap_list.xml', years=years, site=SITE_URL
    )
    response = make_response(sitemap_xml)
    response.headers['Content-Type'] = 'application/xml'

    return response


@app.route('/feed')
def feed_rss():
    artigos = Artigo.query.filter(
        Artigo.publicado.is_(True)
    ).filter(
        Artigo.data_publicacao < datetime.now()
    ).order_by(
        Artigo.data_publicacao.desc()
    ).paginate(1, 20).items
    feed = render_template('rss.xml', artigos=artigos, site=SITE_URL)
    response = make_response(feed)
    response.headers['Content-Type'] = 'application/xml'

    return response


@app.route('/media/<path:filename>')
def media(filename):
    return send_from_directory('static/media/', filename)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5000', debug=True, threaded=True)
