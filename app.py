from flask import Flask, request,render_template
import requests
import psycopg2

app=Flask(__name__)

@app.route("/")
def index():
   return render_template("index.html")

@app.route("/games",methods=["GET"])
def games():
    game=requests.get('https://api-juegos-gzco.onrender.com/games')
    if games:
        return render_template('games.html',games=game.json())
    else:
        return render_template('games.html',games=False)
    
@app.route("/create_game",methods=["GET","POST"])
def create_game():
    if request.method == 'POST':
        titulo = request.form['titulo']
        plataforma = request.form['plataforma']
        desarrollador = request.form['desarrollador']
        year = request.form['year']
        clasificacion = request.form['clasificacion']

        game={"titulo":titulo,"desarrollador":desarrollador,"año lanzamiento":year,"plataforma":plataforma,"clasificacion":clasificacion}
        requests.post("https://api-juegos-gzco.onrender.com/new_game",json=game)
    return render_template("create_game.html")
if __name__=="__main__":
    app.run(debug=True)
