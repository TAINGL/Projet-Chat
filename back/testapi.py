# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flaskext.mysql import MySQL


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
    return redirect(url_for('index'))
    
#    if "email" in session:
#        return redirect(url_for('chatroom'))
#    else:
#        return redirect(url_for('index'))
    
@app.route("/sinscrire", methods=['GET', 'POST'])
def addUser():    
    if request.method == "POST":
        try:
                # Informations Client
            # details = request.form
            response = request.get_json()
            pseudo = response['pseudo']
            email = response['email']
            password = response['password']
            req_enregister_client = ("INSERT INTO users (user_email, user_pseudo, user_password) VALUES (%s, %s, %s)")
            conn = mysql.connect()
            cursor = conn.cursor()
            data = (email, pseudo, password)
            cursor.execute(req_enregister_client, data)
            
            # Fermer la connexion avec la BDD
            conn.commit()
            cursor.close()
            return 'Utilisateur ajouté'
        except:
            return "Utilisateur déjà existant"

@app.route('/connexion', methods=['GET', 'POST'])
def seconnecter():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        response = request.form
        email = response['email']
        password = response['password']
        cursor = mysql.connect().cursor()
        cursor.execute("SELECT user_email, user_password FROM users where user_email = '{}' AND user_password = '{}'".format(str(email), str(password)))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['email'] = account[0]
            session['password'] = account[1]
            return 'Utilisateur loggé!'
        else:
            return 'Utilisateur inexistant!'
#    return render_template('connexion.html')
     
@app.route("/chatroom")
def chatroom():
    return render_template('chatroom.html')

@app.route("/chatroom", methods=['GET', 'POST'])
def sendMsg():
    
    if request.method == "POST":
        response = request.get_json()
        print(response['pseudo'])
        message = response['message']
        pseudo = response['pseudo']
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (message_contenu, user_pseudo ) VALUES (%s, %s) WHERE user_id = user_pseudo", (message, pseudo))
        
            # Fermer la connexion avec la BDD
        conn.commit()
        cursor.close()
        return 'Message ajouté'
    
    return render_template('chatroom.html')

@app.route("/chatroom")
def tenmessages():
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT message_contenu FROM messages ORDER BY message_id desc LIMIT 10")
    result = cursor.fetchall()
    return jsonify(result)

@app.route("/utilisateur")
def users():
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT user_pseudo FROM users")
    result = cursor.fetchall()
    return jsonify(result)

#Mofifier un pseudo utilisateur

@app.route("/settings", methods = ["GET", "POST"])
def update_users1():
    if request.method == "POST":
        user = request.form["pseudo"]
        modify_user = request.form["pseudonew"]
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET user_pseudo = (%s) WHERE user_pseudo = (%s)", (modify_user, user))
        conn.commit()
        cursor.close()
        return "Update réalisé avec succès !"
    return render_template("settings.html")

#Mofifier un email utilisateur

@app.route("/settings", methods = ["GET", "POST"])
def update_users2():
    if request.method == "POST":
        email1 = request.form["email"]
        modify_email = request.form["emailnew"]
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET user_email = (%s) WHERE user_email = (%s)", (modify_email, email1))
        conn.commit()
        cursor.close()
        return "Update réalisé avec succès !"
    return render_template("settings.html")

#Mofifier un mot de passe utilisateur

@app.route("/settings", methods = ["GET", "POST"])
def update_users3():
    if request.method == "POST":
        password = request.form["password"]
        modify_password = request.form["passwordnew"]
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET user_password = (%s) WHERE user_password = (%s)", (modify_password, password))
        conn.commit()
        cursor.close()
        return "Update réalisé avec succès !"
    return render_template("settings.html")

@app.route('/getsession/')
def getsession():
    if 'email' in session:
        return ("Utilisateur loggé : " + session['email'])
    return 'Non loggé'

@app.route('/deconnexion/')
def logout():
    session.pop('email', None)
    return 'Logout'
#   # Redirect to login page
#   return redirect(url_for('logout'))
    

# Cette dernière partie permet juste de faire en sorte que l’application se lance 
# quand on lance le code dans la console ou le terminal.
if __name__ == '__main__':
    app.run(debug=True,port=5000)
