from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'usuariosdb'

mysql = MySQL(app)

def crear_tabla():
    cursor = mysql.connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT PRIMARY KEY AUTO_INCREMENT,
            nombre VARCHAR(50) NOT NULL,
            apellido_paterno VARCHAR(50) NOT NULL,
            apellido_materno VARCHAR(50) NOT NULL,
            email VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        );
    ''')
    mysql.connection.commit()
    cursor.close()

with app.app_context():
    crear_tabla()

def email_existe(email):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
    existe = cursor.fetchone()
    cursor.close()
    return existe is not None


def registrar_usuario(nombre, ap_paterno, ap_materno, email, password):
    if email_existe(email):
        return False

    hashed_password = generate_password_hash(password)

    cursor = mysql.connection.cursor()
    cursor.execute('''
        INSERT INTO usuarios (nombre, apellido_paterno, apellido_materno, email, password)
        VALUES (%s, %s, %s, %s, %s)
    ''', (nombre, ap_paterno, ap_materno, email, hashed_password))

    mysql.connection.commit()
    cursor.close()
    return True

def obtener_usuario_por_email(email):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id, nombre, apellido_paterno, apellido_materno, email, password FROM usuarios WHERE email = %s", (email,))
        usuario = cursor.fetchone()
        cursor.close()

        if usuario is None:
            return None
        return {
            "id": usuario[0],
            "nombre": usuario[1],
            "apellido_paterno": usuario[2],
            "apellido_materno": usuario[3],
            "email": usuario[4],
            "password": usuario[5]
        }

    except Exception as e:
        print(f"Error obteniendo usuario: {e}")
        return None



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

@app.route("/registrame", methods=["POST"])
def registrame():
    nombre = request.form["nombre"]
    ap_paterno = request.form["apellido_paterno"]
    ap_materno = request.form["apellido_materno"]
    email = request.form["email"]
    password = request.form["password"]
    confirmPassword = request.form["confirmPassword"]

    if not nombre or not ap_paterno or not ap_materno or not email or not password:
        flash("Todos los campos son obligatorios", "error")
        return redirect(url_for("registro"))

    if password != confirmPassword:
        flash("Las contraseñas no coinciden", "error")
        return redirect(url_for("registro"))

    if registrar_usuario(nombre, ap_paterno, ap_materno, email, password):
        flash("Registro exitoso", "success")
        return redirect(url_for("login"))
    else:
        flash("El correo ya está registrado", "error")
        return redirect(url_for("registro"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if 'usuario_id' in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Complete todos los campos", "error")
            return render_template("login.html")

        usuario = obtener_usuario_por_email(email)

        if usuario is None:
            flash("El correo no está registrado", "error")
            return render_template("login.html")

        if check_password_hash(usuario["password"], password):
            session["usuario_id"] = usuario["id"]
            session["usuario_nombre"] = usuario["nombre"]
            session["usuario_email"] = usuario["email"]

            flash("Inicio de sesión exitoso", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Contraseña incorrecta", "error")
            return render_template("login.html")

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "usuario_id" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada correctamente", "success")
    return redirect(url_for("index"))


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
            imc = round(peso / (estatura * estatura), 2)
            return render_template("calculadoraIMC.html", resultado_imc=imc)
        except:
            return render_template("calculadoraIMC.html", error="Datos inválidos")

    return render_template("calculadoraIMC.html")

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
        proteinas = round((calorias * 0.30) / 4)
        grasas = round((calorias * 0.25) / 9)
        carbohidratos = round((calorias * 0.45) / 4)

    return render_template("calculadoraMACRO.html",proteinas=proteinas, grasas=grasas, carbohidratos=carbohidratos)

@app.route("/analisis")
def analisis():
    return render_template("analisis.html")

if __name__ == '__main__':
    app.run(debug=True)
