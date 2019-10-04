# -*- coding: utf-8 -*-
import os
from flask import (
    Blueprint, render_template, url_for, request, flash, redirect
)
from flask_user import login_required
from resenhas.models import Artigo, Tag
from resenhas.config import MediaConfig
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
            path_file = os.path.join(
                MediaConfig.BLOG_IMG_FILE_DEST.value,
                filename
            )
            file.save(path_file)
            artigo.capa = "{}/{}".format(
                MediaConfig.BLOG_IMG_FILE_SRC.value, filename
            )
        # saving the tags
        list_tags = form.list_tags.data.split(',')
        tag = Tag()
        for item in list_tags:
            new_tag = tag.get_or_create_tag(item)
            if new_tag is not None:
                artigo.tags.append(new_tag)
        db.session.add(artigo)
        db.session.commit()
        flash('Artigo adicionado com sucesso!', 'success')
        return redirect(url_for('admin.list_artigos'))

    return render_template(
        'artigo_add.html', form=form
    )


@admin.route('/artigos/<int:id>/edit', methods=['GET', 'POST'])
def edit_artigo(id):
    old_capa = None
    old_artigo = None
    artigo = Artigo.query.get_or_404(id)
    form = ArtigoEditForm(obj=artigo)
    if request.method == 'POST' and form.validate_on_submit():
        old_artigo = Artigo.query.get_or_404(form.id.data)
        old_capa = os.path.join(
            MediaConfig.STATIC_DIR.value,
            old_artigo.capa
        )
        form.populate_obj(artigo)
        if request.files['nova_capa'] is not None:
            file = request.files['nova_capa']
            if file and file.filename is not None:
                filename = secure_filename(file.filename)
                path_file = os.path.join(
                    MediaConfig.BLOG_IMG_FILE_DEST.value,
                    filename
                )
                try:
                    file.save(path_file)
                except Exception as e:
                    flash("Erro ao enviar arquivo. {}".format(e), "error")

                try:
                    os.unlink(old_capa)
                except Exception as e:
                    flash("Erro ao excluir capa antiga. {}".format(e), "error")
                artigo.capa = "{}/{}".format(
                    MediaConfig.BLOG_IMG_FILE_SRC.value, filename
                )
        # saving the tags
        tag = Tag()
        list_tags = map(lambda x: x.strip(), form.list_tags.data.split(','))
        old_tags = []
        for t in old_artigo.tags:
            old_tags.append(t.nome.strip())
            if t.nome.strip() not in list_tags:
                artigo.tags.remove(t)
        for item in list_tags:
            new_tag = tag.get_or_create_tag(item)
            if new_tag.nome not in old_tags:
                artigo.tags.append(new_tag)
        try:
            db.session.add(artigo)
            db.session.commit()
        except Exception as e:
            print("Erro ao editar artigo. {}".format(e))

        flash('Artigo editado com sucesso!', 'success')
        return redirect(url_for('admin.list_artigos'))

    list_tags = []
    for t in artigo.tags:
        list_tags.append(t.nome.strip())
    form.list_tags.data = ', '.join(list_tags)
    return render_template(
        'artigo_edit.html',
        form=form, artigo=artigo
    )


@admin.route('/artigos/<int:id>/delete', methods=['GET', 'POST', 'DELETE'])
def delete_artigo(id):
    artigo = Artigo.query.get(id)
    capa_artigo = None
    if artigo.capa:
        capa_artigo = os.path.join(
            MediaConfig.STATIC_DIR.value,
            artigo.capa
        )
    try:
        db.session.delete(artigo)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print("Erro ao excluir artigo. {}".format(e), "error")
        return redirect(url_for('admin.list_artigos'))
    if capa_artigo:
        os.unlink(capa_artigo)
    flash('Artigo excluido com sucesso!', 'success')
    return redirect(url_for('admin.list_artigos'))
