from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash
import re
import requests

app.config['MYSQL_HOST'] = 'localhost'

app = Flask(__name__)
app.secret_key = 'your_secret_key'

USUARIOS_REGISTRADOS = {
    'admin@correo.com': {
        'password': 'admin123', 
        'nombre': 'administrador',
    }
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/recetas")
def recetas():
    return render_template("recetas.html")

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

@app.route("/registro", methods=["GET"])
def registro():
    return render_template("registro.html")

@app.route("/registrame", methods=["GET", "POST"])
def registrame():
    if request.method == "POST":
        nombreCompleto = request.form["nombreCompleto"]
        email = request.form["email"]
        password = request.form["password"]
        confirmPassword = request.form["confirmPassword"]

        error = None
        if not nombreCompleto or not email or not password or not confirmPassword:
            error = "Todos los campos son obligatorios"
        
        if password != confirmPassword:
            error = "La contraseña no coincide"
        
        if error:
            flash(error, 'error')
            return render_template("registro.html")
        else:
            flash(f"¡Registro exitoso para el usuario: {nombreCompleto}!", 'success')
            return redirect(url_for('index'))

    return render_template("registro.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash("Por favor, ingresa tu email y contraseña", "error")
        elif email not in USUARIOS_REGISTRADOS:
            flash("Correo no registrado", "error")
        elif USUARIOS_REGISTRADOS[email]['password'] != password:
            flash("Contraseña incorrecta", "error")
        else:
            session['usuario_email'] = email
            session['usuario_nombre'] = USUARIOS_REGISTRADOS[email]['nombre']
            session['logeando'] = True

            flash("Inicio de sesión exitoso", "success")
            return redirect(url_for('bienvenido'))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada correctamente", "success")
    return redirect(url_for('index'))

@app.route("/calculadoraGCT", methods=["GET", "POST"])
def gct():
    resultado = None

    if request.method == "POST":
        peso = float(request.form["peso"])
        estatura = float(request.form["estatura"])
        edad = int(request.form["edad"])
        genero = request.form["gender"]
        actividad = float(request.form["actividad"])

        if genero == "male":
            tmb = (10 * peso) + (6.25 * estatura) - (5 * edad) + 5
        else:
            tmb = (10 * peso) + (6.25 * estatura) - (5 * edad) - 161

        resultado = round(tmb * actividad)

    return render_template("calculadoraGCT.html", resultado=resultado)


@app.route("/calculadoraIMC", methods=["GET", "POST"])
def imc():
    if request.method == "POST":
        try:
            peso = float(request.form["peso"])
            estatura = float(request.form["estatura"]) / 100  

            imc = peso / (estatura * estatura)
            imc = round(imc, 2)

            return render_template("calculadoraIMC.html", resultado_imc=imc)
        
        except:
            return render_template("calculadoraIMC.html", error="Datos inválidos")
    return render_template("calculadoraIMC.html")


from flask import render_template, request

@app.route("/calculadoraTMB", methods=["GET", "POST"])
def tmb():
    resultado = None

    if request.method == "POST":
        peso = float(request.form["peso"])          
        estatura = float(request.form["estatura"])  
        edad = int(request.form["edad"])
        genero = request.form["genero"]

        if genero == "male":
            resultado = (10 * peso) + (6.25 * estatura) - (5 * edad) + 5
        else:  
            resultado = (10 * peso) + (6.25 * estatura) - (5 * edad) - 161

    return render_template("calculadoraTMB.html", resultado=resultado)


@app.route("/calculadoraPCI")
def pci():
    return render_template("calculadoraPCI.html")

@app.route("/calculadoraMACRO", methods=["GET", "POST"])
def macro():
    proteinas = grasas = carbohidratos = None

    if request.method == "POST":
        calorias = float(request.form["calorias"])

        pct_prot = 0.30
        pct_grasa = 0.25
        pct_carb = 0.45

        proteinas = round((calorias * pct_prot) / 4)
        grasas = round((calorias * pct_grasa) / 9)
        carbohidratos = round((calorias * pct_carb) / 4)

    return render_template("calculadoraMACRO.html",proteinas=proteinas,grasas=grasas,carbohidratos=carbohidratos)


@app.route("/analisis")
def analisis():
    return render_template("analisis.html")

if __name__ == '__main__':
    app.run(debug=True)
