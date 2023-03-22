from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_googlemaps import GoogleMaps
from flask_restful import Resource, Api
from models import db, Mapas


# Flask app
app = Flask(__name__)


# Configuramos la app 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecreto'

db.init_app(app)

# Configuramos google maps
app.config['GOOGLEMAPS_KEY'] = '611638969896-d57uu9m81bgbak25hha661uh8o4hnv2t.apps.googleusercontent.com'
GoogleMaps(app)
api = Api(app)

# Creamos una lista vacia para extraer los datos de la base de datos
markers = []

# Creamos una clase que nos permita extraer los datos de la base de datos
class Puntos(Resource):
    def get(self):
        # Creamos una variable que nos permita acceder a los datos
        puntos_mapa = Mapas.query.all()
        # Hacemos un bucle for que nos permita iterar los datos de esa variable nueva y los guardamos en la libreria markers
        for i in puntos_mapa:
            markers.append(
                { "nombre" : i.nombre, "latitud" : i.latitud, "longitud" : i.longitud }
            )
        # Retornamos la nueva lista cargada
        return markers 
# Llamamos a la funcion
api.add_resource(Puntos, '/api/puntos')

 # Creamos una ruta principal
@app.route("/")
def index():
    markers.clear()
    return render_template("index1.html")

# Creamos una ruta donde mostraremos los puntos
@app.route("/agregar", methods = ['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        lat = request.form['latitud']
        lng = request.form['longitud']
        nmb = request.form['nombre']
        
        #Guardamos los datos recibidos
        datos = Mapas(nombre = nmb, latitud = lat, longitud = lng)

        # Archivamos esos datos
        db.session.add(datos)
        db.session.commit()
        
        # Mandamos al usuario de vuelta a la pagina de inicio
        return redirect(url_for('index'))
    
    puntos_mapa = Mapas.query.all()
    print(puntos_mapa)

    return render_template('agregar.html')

# Cremos una ruta que renderize los datos de la bd
@app.route("/data")
def data():   
    #Guardamos los datos de la base en una variable
    ver_data = Mapas.query.all()
    #Renderizamos data y tambien las variables nuevas
    return render_template('puntos.html', ver_data=ver_data)

#Creamos una ruta y habilitamos los metodos fet y post 
@app.route("/eliminar/<id>", methods = ['GET', 'POST'])
def delete(id):

    #Creamos una condicional if con el metodo post
    nombre_lugar = Mapas.query.get(id)
    if request.method == 'POST':        
        #Guardamos la id de los datos en un variable
        eliminar_id = Mapas.query.get(id)
        print(eliminar_id)
        #Eliminamos el id
        db.session.delete(eliminar_id)
        #Confirmamos la eliminacion
        db.session.commit()
        #Le mostramos al usuario el listado actualizado
        return redirect(url_for('index'))
    #Devolvemos los datos que necesitamos mostrar
    return render_template("pengunta.html", id=id, nombre_lugar=nombre_lugar)

# Creamos una ruta que nos permita iniciar la carga desde el mapa
@app.route("/add", methods = ['GET', 'POST'])
def agregar_punto():
    # Guardamos los datos en variables
    return render_template('tabla.html')

@app.route("/mapa")
def mapa():
    return render_template('mapa.html')
        



# Corremos el programa
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=1000)