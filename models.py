from flask_user import UserMixin
from resenhas import db
from datetime import datetime
from slugify import slugify


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(
        'is_active', db.Boolean(), nullable=False, server_default='1'
    )
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    email_confirmed_at = db.Column(db.DateTime())
    # User information
    first_name = db.Column(db.String(100), nullable=False, server_default='')
    last_name = db.Column(db.String(100), nullable=False, server_default='')
    # Define the relationship to Role via UserRoles
    roles = db.relationship('Role', secondary='user_roles')


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)


class UserRoles(db.Model):
    __tablename__ = 'user_roles'

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(
        'users.id', ondelete='CASCADE'
    ))
    role_id = db.Column(db.Integer(), db.ForeignKey(
        'roles.id', ondelete='CASCADE'
    ))


class Artigo(db.Model):
    __tablename__ = 'artigos'

    id = db.Column(db.Integer(), primary_key=True)
    titulo = db.Column(db.String(255), nullable=False, unique=True)
    conteudo = db.Column(db.Text)
    capa = db.Column(db.String(255))
    criado_em = db.Column(db.DateTime(), default=datetime.now())
    publicado = db.Column(db.Boolean(), server_default='0')
    data_publicacao = db.Column(db.DateTime(), default=datetime.now())
    data_atualizacao = db.Column(db.DateTime(), onupdate=datetime.now())
    tags = db.relationship(
        'Tag',
        secondary='artigos_tags',
        backref=db.backref('artigo', uselist=True),
        primaryjoin="(Artigo.id == ArtigoTags.artigo_id)"
    )

    @property
    def slug(self):
        return "{}-{}".format(slugify(self.titulo), self.id)


class Tags(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(60), unique=True)
    artigos = db.relationship(
        'Artigo',
        secondary='artigos_tags',
        backref=db.backref('tag'),
        primaryjoin="(Tag.id == ArtigoTags.tag_id)"
    )

    @property
    def slug(self):
        return '{}'.format(slugify(self.nome))


class ArtigoTags(db.Model):
    __tablename__ = 'artigos_tags'

    id = db.Column(db.Integer(), primary_key=True)
    artigo_id = db.Column(db.Integer(), db.ForeignKey(
        'artigos.id', ondelete='CASCADE'
    ))
    tag_id = db.Column(db.Integer(), db.ForeignKey(
        'tags.id', ondelete='CASCADE'
    ))
