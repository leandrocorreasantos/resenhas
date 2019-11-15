# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from resenhas import db

errors = Blueprint('errors', __name__, template_folder='templates')


@errors.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html', error=error), 404


@errors.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html', error=error), 500
