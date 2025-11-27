from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"


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


@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form["nombre"]
        apellidos = request.form["apellidos"]
        email = request.form["email"]
        password = request.form["password"]
        confirmPassword = request.form["confirmPassword"]

        if not nombre or not apellidos or not email or not password:
            flash("Todos los campos son obligatorios", "error")
            return render_template("registro.html")

        if password != confirmPassword:
            flash("Las contraseñas no coinciden", "error")
            return render_template("registro.html")

        if registrar_usuario(nombre, apellidos, email, password):
            flash("¡Registro exitoso!", "success")
            return redirect(url_for("index"))
        else:
            flash("Error registrando usuario", "error")

    return render_template("registro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT email, pass_hash, nombre FROM usuarios WHERE email = %s", (email,))
        usuario = cursor.fetchone()
        cursor.close()

        if usuario is None:
            flash("Correo no registrado", "error")
            return render_template("login.html")

        if not check_password_hash(usuario[1], password):
            flash("Contraseña incorrecta", "error")
            return render_template("login.html")

        session["usuario_email"] = usuario[0]
        session["usuario_nombre"] = usuario[2]
        session["logeando"] = True

        flash("Inicio de sesión exitoso", "success")
        return redirect(url_for("index"))

    return render_template("login.html")

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

@app.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada correctamente", "success")
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)
