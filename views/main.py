import os
from datetime import datetime
from sqlalchemy import distinct
from sqlalchemy.sql.expression import extract
from flask import (
    Blueprint, render_template, make_response, send_from_directory
)
from resenhas.models import Artigo


dotenv_path = os.path.join(os.getcwd(), '.env')
if os.path.isfile(dotenv_path):
    from dotenv import load_dotenv
    load_dotenv(dotenv_path)

SITE_URL = os.environ.get('SITE_URL')

main_bp = Blueprint(
    'main_bp',
    __name__,
    url_prefix='/'
)


@main_bp.route('/sitemap-<int:year>.xml')
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


@main_bp.route('/sitemap.xml')
def static_sitemap():
    sitemap = render_template('sitemap_static.xml', site=SITE_URL)
    response = make_response(sitemap)
    response.headers['Content-Type'] = 'application/xml'

    return response


@main_bp.route('/sitemaps.xml')
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


@main_bp.route('/feed')
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


@main_bp.route('/media/<path:filename>')
def media(filename):
    return send_from_directory('static/media/', filename)


@main_bp.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt')


@main_bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html', error=error), 404


@main_bp.app_errorhandler(500)
def internal_error(error):
    # db.session.rollback()
    return render_template(
        '500.html',
        error=error
    ), 500
