from models import db, Mapas
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask('app')

# Configuramos la app 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecreto'

db.init_app(app)

with app.app_context():
    db.create_all()

with app.app_context():
    #Creamos usuarios con la clase y le damos los datos
    estacion1 = Mapas(nombre="Base K2 de Bomberos Voluntarios", latitud=-25.50908951477699, longitud=-54.61372904860282, categoria="Estacion de bomberos" )
    estacion2 = Mapas(nombre="Lago de la Republica", latitud=-25.51555232619372, longitud=-54.62016117540243, categoria="Lago")

    db.session.add(estacion1)
    db.session.add(estacion2)
    db.session.commit()