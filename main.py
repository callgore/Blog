from flask import Flask, render_template, request, session, redirect, url_for, flash
from DB_administration import *
from flask_wtf.csrf import CSRFProtect
import functools
import operator
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret"
csrf = CSRFProtect(app)


# manejo de errores
@app.errorhandler(404)
def pageNotFound(e):
    return redirect(url_for('ForWeb'))


# ruta principal
@app.route("/")
def home():
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop('username')
    return redirect(url_for('inicio'))


# sub ruta inicio sesion
@app.route("/inicio")
def inicio():
    return render_template("login.html")


# sub ruta registro
@app.route("/register")
def register():
    return render_template("register.html")


# iniciar sesion
@app.route("/inicioSesion", methods=["POST"])
def trySession():
    password = request.form['password']
    user = request.form['User']
    if initSession(user, password):
        session['username'] = user
        return render_template("index-foro.html", discussion=getDiscussion())
    else:
        error = "User or password was invalid!"
        flash(error)
        return render_template("login.html")


# registro de usuarios
@app.route("/oRegister", methods=["POST"])
def newUser():
    user = request.form['User']
    email = request.form['email']
    password = request.form['password']
    if addValuesUser(user, email, password):
        passed = "User was created successfully!"
        flash(passed)
        return render_template("login.html")
    else:
        error = "Try with another username"
        flash(error)
        return render_template("register.html")


# sub ruta foro inicial
@app.route("/ForWeb")
def ForWeb():
    return render_template("index-foro.html", discussion=getDiscussion())


# vista de foros
@app.route("/viewTopics/<int:id>", methods=['GET'])
def viewTopics(id):
    return render_template("topic.html", discussion=getAllDiscussion(id),
                           topic=functools.reduce(operator.add, (getTopic(id))), id=id)


# agregar comentario en foros
@app.route("/replyPost", methods=["POST"])
def replyPost():
    try:
        userOnline = session['username']
        id = request.form['id']
        topic = request.form['topic']
        comment = request.form['comment']
        time = datetime.now().date()
        addComents(id, topic, userOnline, comment, time)
        return render_template("topic.html", discussion=getAllDiscussion(id),
                               topic=functools.reduce(operator.add, (getTopic(id))), id=id)
    except:
        return redirect(url_for('inicio'))


# sub ruta crear nuevo topico
@app.route("/newTopic")
def newTopic():
    return render_template("new-topic.html")


# agregar nuevas discusiones
@app.route("/addNewTopic", methods=["POST"])
def addNewTopic():
    try:
        userOnline = session['username']
        a = getDiscussion()
        id = a[-1][0] + 1
        topic = request.form['title']
        comment = request.form['comment']
        time = datetime.now().date()
        addComents(id, topic, userOnline, comment, time)
        return render_template("topic.html", discussion=getAllDiscussion(id),
                               topic=functools.reduce(operator.add, (getTopic(id))), id=id)
    except:
        return redirect(url_for('inicio'))


if __name__ == "__main__":
    app.run(debug=True)
