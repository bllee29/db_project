from server import db
from server import config


class ExampleUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return '<ExampleUser %r>' % self.name