from flask import Flask, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Render: https://api-juegos-gzco.onrender.com

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

db = SQLAlchemy(app)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    desarrollador = db.Column(db.String(120), nullable=False)
    anio_lanzamiento = db.Column(db.Integer, nullable=False)
    plataforma = db.Column(db.String(120), nullable=False)
    clasificacion = db.Column(db.String(120), nullable=False)

    # Representación
    def __init__(self,titulo,desarrollador,year,plataforma,clasificacion):
        self.titulo=titulo
        self.desarrollador = desarrollador
        self.anio_lanzamiento = year
        self.plataforma = plataforma
        self.clasificacion = clasificacion

    def to_json(self):
        return{
            "id":self.id,
            "titulo":self.titulo,
            "desarrollador":self.desarrollador,
            "año lanzamiento":self.anio_lanzamiento,
            "plataforma":self.plataforma,
            "clasificacion":self.clasificacion
        }
    
    def __repr__(self):
        return f'<Game {self.name}>'

@app.route('/games',methods=["GET"])
def read():
    Games = Game.query.all()
    return jsonify([Game.to_json() for Game in Games])

@app.route('/new_game',methods=["POST"])
def create_game():
    if not request.json or 'titulo' not in request.json:
        abort(400)
    titulo=request.json["titulo"]
    desarrollo=request.json["desarrollador"]
    year=request.json["año lanzamiento"]
    plat=request.json["plataforma"]
    clasificacion=request.json["clasificacion"]

    game = Game(titulo,desarrollo,year,plat,clasificacion)  
    db.session.add(game)
    db.session.commit()
    return jsonify(game.to_json()),201

@app.route('/delete/<id>',methods=["DELETE"])
def delete(id):
    games=Game.query.get_or_404(id)
    db.session.delete(games)    
    db.session.commit()
    return jsonify({"status":"True"}),201

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=False)