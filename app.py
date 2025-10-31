from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Conexión a la base de datos SQLite
def get_db_connection():
    conn = sqlite3.connect("barberia.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/reservar", methods=["POST"])
def reservar():
    nombre = request.form["nombre"]
    telefono = request.form["telefono"]
    servicio = request.form["servicio"]
    fecha = request.form["fecha"]
    hora = request.form["hora"]

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO reservas (nombre, telefono, servicio, fecha, hora) VALUES (?, ?, ?, ?, ?)",
        (nombre, telefono, servicio, fecha, hora),
    )
    conn.commit()
    conn.close()

    return redirect("/ver_reservas")


@app.route("/ver_reservas")
def ver_reservas():
    conn = get_db_connection()
    cur = conn.cursor()

    # 🔹 Cambio clave: ordenar por id en lugar de creado_en
    cur.execute("SELECT * FROM reservas ORDER BY id DESC")

    reservas = cur.fetchall()
    conn.close()
    return render_template("ver_reservas.html", reservas=reservas)


if __name__ == "__main__":
    app.run(debug=True)









