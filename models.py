# encoding: utf-8
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Thingy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )
    date_last_modified = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def __repr__(self):
        return '<User {}, {}, {}>'.format(self.id, self.date_created, self.date_last_modified)