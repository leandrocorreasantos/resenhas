import os
from flask import (
    Blueprint, render_template, url_for, request, flash, redirect
)
from flask_user import login_required
from resenhas.models import Artigo
from .forms import ArtigoForm, ArtigoEditForm
from resenhas import db
from werkzeug.utils import secure_filename


admin = Blueprint(
    'admin',
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/admin'
)
BLOG_IMG_FILE_DEST = 'static/blog/img/artigos/'


@admin.route('/')
@admin.route('/artigos')
def list_artigos():
    artigos = Artigo.query.all()
    return render_template(
        'artigos.html', artigos=artigos, title_page='Artigos'
    )


@admin.route('/artigos/novo', methods=['GET', 'POST'])
@login_required
def novo_artigo():
    form = ArtigoForm(request.form)
    if form.validate_on_submit() and request.method == 'POST':
        artigo = Artigo()
        form.populate_obj(artigo)
        file = request.files['capa']
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            path_file = os.path.join(BLOG_IMG_FILE_DEST, filename)
            file.save(path_file)
            artigo.capa = filename
        db.session.add(artigo)
        db.session.commit()
        flash('Artigo adicionado com sucesso!', 'success')
        return redirect(url_for('admin.list_artigos'))

    return render_template(
        'artigo_add.html', title_page='Novo Artigo', form=form
    )


@admin.route('/artigos/<int:id>/edit', methods=['GET', 'POST'])
def edit_artigo(id):
    old_capa = None
    artigo = Artigo.query.get_or_404(id)
    form = ArtigoEditForm(obj=artigo)
    if request.method == 'POST' and form.validate_on_submit():
        old_artigo = Artigo.query.get_or_404(form.id.data)
        print('old artigo capa {}'.format(old_artigo.capa))
        old_capa = os.path.join(BLOG_IMG_FILE_DEST, old_artigo.capa)

        form.populate_obj(artigo)
        file = request.files['capa']
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            path_file = os.path.join(BLOG_IMG_FILE_DEST, filename)
            try:
                file.save(path_file)
            except Exception as e:
                flash("Erro ao enviar arquivo. {}".format(e), "error")

            try:
                os.unlink(old_capa)
            except Exception as e:
                flash("Erro ao excluir capa antiga. {}".format(e), "error")
            artigo.capa = filename
        db.session.add(artigo)
        db.session.commit()
        flash('Artigo editado com sucesso!', 'success')
        return redirect(url_for('admin.list_artigos'))

    artigo_capa = os.path.join(BLOG_IMG_FILE_DEST, artigo.capa)
    return render_template(
        'artigo_edit.html', title_page='Editar Artigo',
        form=form, artigo_capa=artigo_capa, artigo=artigo,
    )


@admin.route('/artigos/<int:id>/delete', methods=['GET', 'POST', 'DELETE'])
def delete_artigo(id):
    artigo = Artigo.query.first_or_404(id)
    print('capa {}'.format(artigo.capa))
    capa_artigo = None
    if artigo.capa:
        capa_artigo = os.path.join(BLOG_IMG_FILE_DEST, artigo.capa)
    try:
        db.session.delete(artigo)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash("Erro ao excluir artigo. {}".format(e), "error")
        return redirect(url_for('admin.list_artigos'))
    if capa_artigo:
        os.unlink(capa_artigo)
    flash('Artigo excluído com sucesso!', 'success')
    return redirect(url_for('admin.list_artigos'))
