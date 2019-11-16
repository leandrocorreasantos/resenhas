# -*- coding: utf-8 -*-
import os
from enum import Enum


basedir = os.path.abspath(os.path.dirname(__file__))


dotenv_path = os.path.join(os.getcwd(), '.env')
if os.path.isfile(dotenv_path):
    from dotenv import load_dotenv
    load_dotenv(dotenv_path)


class MediaConfig(Enum):
    # upload
    STATIC_DIR = os.path.join(basedir, 'static')
    MEDIA_DIR = 'media/'
    MEDIA_ROOT = os.path.join(STATIC_DIR, 'media')
    BLOG_IMG_FILE = 'blog/img/artigos'
    BLOG_IMG_FILE_DEST = os.path.join(MEDIA_ROOT, BLOG_IMG_FILE)
    BLOG_IMG_FILE_SRC = "{}{}".format(MEDIA_DIR, BLOG_IMG_FILE)


class Config(object):
    FLASK_DEBUG = True
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # flask-user
    USER_APP_NAME = "Resenhas de Filmes"
    USER_ENABLE_EMAIL = True      # Disable email authentication
    USER_ENABLE_USERNAME = True    # Enable username authentication
    USER_REQUIRE_RETYPE_PASSWORD = False    # Simplify register form
    USER_ENABLE_REGISTER = True
    USER_EMAIL_SENDER_EMAIL = 'contato@resenhasdefilmes.com.br'
    USER_EMAIL_SENDER_NAME = 'Resenhas de Filmes'
    # flask-mail @TODO: change parameters on deploy
    MAIL_SERVER = os.environ.get('MAIL_SMTP_SERVER')
    MAIL_PORT = os.environ.get('MAIL_SMTP_PORT')
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MEDIA_ROOT = MediaConfig.MEDIA_ROOT
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
