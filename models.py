from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Mapas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String)
    latitud = db.Column(db.Float(50))
    longitud = db.Column(db.Float(50))
    categoria = db.Column(db.String)