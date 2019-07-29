# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flaskext.mysql import MySQL
import MySQLdb.cursors


# On donne ensuite un nom à l’application ici ce sera app
app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = 'key'

# Intialize MySQL
mysql = MySQL()
mysql.init_app(app)

# Enter your database connection details below
app.config['MYSQL_DATABASE_USER'] = 'Laura'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'chat_room'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

# Ensuite vient la partie cruciale : définir une page (ou route) avec flask
# @app.route permet de préciser à quelle adresse ce qui suit va s’appliquer.
# Ici comme on est sur la page d’accueil, on met juste (“/”)

# Si session client ouvert => dirige vers chatroom, 
# sinon se dirige vers page connexion
@app.route("/")
def index():
    if "e_mail" in session:
        return redirect(url_for('chatroom.html'))
    else:
        return render_template('index.html')
    
@app.route("/sinscrire", methods=['GET', 'POST'])
def addUser():
    if request.method == "POST":

            # Informations Client
        details = request.form
        email = details['email']
        pseudo = details['pseudo']
        password = details['password']
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (user_email,user_pseudo,user_password) VALUES (%s, %s, %s)", (email,pseudo, password))
        
            # Fermer la connexion avec la BDD
        conn.commit()
        cursor.close()
        return 'Utilisateur ajouté'
    return render_template('sinscrire.html')

@app.route('/connexion', methods=['GET', 'POST'])
def seconnecter():
    error = None
    
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]   
        req_connection_client = "SELECT * FROM users where user_email = '%s' AND user_password = '%s' "
        cursor = mysql.connect().cursor()
        cursor.execute(req_connection_client % (email, password))
        resultat_connection_client = cursor.fetchall()
    
        if len(resultat_connection_client) == 0:
            session['email'] = None
            error = "Cette email ou ce mot de passe ne sont pas valides, veuillez reessayer"
            return render_template("connexion.html", error=error)
        else:
            session["email"] = request.form["email"]
            return redirect(url_for('chatroom'))

    elif request.method == "GET":
        return render_template("connexion.html")

@app.route("/chatroom")
def chatroom():
    return render_template('chatroom.html')

@app.route("/chatroom")
def ten_messages():
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT message_contenu FROM messages ORDER BY message_id desc LIMIT 10")
    result = cursor.fetchall()
    return jsonify(result)

#@app.route("/chatroom")
#def sendMsg():
#    return render_template('chatroom.html')
    
@app.route("/utilisateur")
def users():
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT user_pseudo FROM users")
    result = cursor.fetchall()
    return jsonify(result)

#@app.route('/logout')
#def logout():

# Cette dernière partie permet juste de faire en sorte que l’application se lance 
# quand on lance le code dans la console ou le terminal.
if __name__ == '__main__':
    app.run(debug=True,port=5001)
