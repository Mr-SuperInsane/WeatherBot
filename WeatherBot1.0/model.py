from app import app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy(app)
Migrate(app, db)

class Person(db.Model):

    __tablename__ = 'persons'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, unique=True, nullable=False)
    region = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    alarm = db.Column(db.Boolean)

    def __init__(self, user_id, region, url, alarm):
        self.user_id = user_id
        self.region = region
        self.url = url
        self.alarm = alarm

