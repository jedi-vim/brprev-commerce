from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model


class ORMClass(Model):
    @classmethod
    def get_one(cls, id):
        return cls.query.filter(cls.id == id).one()

    @classmethod
    def get_one_by(cls, **kw):
        return cls.query.filter_by(**kw).one()


db = SQLAlchemy(model_class=ORMClass)


def truncate_tables(*args, **kwargs):
    for table in db.metadata.sorted_tables:
        db.session.execute(f'TRUNCATE {table.name} RESTART IDENTITY CASCADE')
    db.session.commit()


def drop_create_tables(*args, **kwargs):
    db.metadata.drop_all()
    db.metadata.create_all()
