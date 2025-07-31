from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///viajes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de datos
class Viaje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    origen = db.Column(db.String(100), nullable=False)
    destino = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.String(50), nullable=False)
    pasajeros = db.Column(db.Integer, nullable=False)

# Rutas principales
@app.route('/')
def index():
    viajes = Viaje.query.all()
    return render_template('index.html', viajes=viajes)

@app.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        origen = request.form['origen']
        destino = request.form['destino']
        fecha = request.form['fecha']
        pasajeros = request.form['pasajeros']

        nuevo_viaje = Viaje(origen=origen, destino=destino, fecha=fecha, pasajeros=int(pasajeros))
        db.session.add(nuevo_viaje)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('crear.html')

@app.route('/eliminar/<int:id>')
def eliminar(id):
    viaje = Viaje.query.get_or_404(id)
    db.session.delete(viaje)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
