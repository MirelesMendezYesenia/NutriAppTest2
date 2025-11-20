from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'

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


@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada correctamente", "success")
    return redirect(url_for('index'))

@app.route("/calculadoraGCT")
def gct():
    return render_template("calculadoraGCT.html")

@app.route("/calculadoraIMC")
def imc():
    return render_template("calculadoraIMC.html")

@app.route("/calculadoraTMB")
def tmb():
    return render_template("calculadoraTMB.html")

@app.route("/calculadoraPCI")
def pci():
    return render_template("calculadoraPCI.html")

@app.route("/calculadoraMACRO")
def macro():
    return render_template("calculadoraMACRO.html")

@app.route("/analisis")
def analisis():
    return render_template("analisis.html")

if __name__ == '__main__':
    app.run(debug=True)
