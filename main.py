from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

@app.route('/')
def default():
    return jsonify(message="Bienvenido a la API")

@app.route('/hello')
def hello():
    # Obtener parámetros de la URL
    nombre = request.args.get('nombre', 'Mundo')  # Valor por defecto: "Mundo"
    edad = request.args.get('edad')

    # Respuesta básica
    respuesta = {
        "message": f"Hola, {nombre}!"
    }

    # Si también se pasa edad, la incluimos
    if edad:
        respuesta["edad"] = f"Tienes {edad} años"

    return jsonify(respuesta)

@app.route('/api/datos', methods=['POST'])
def recibir_datos():
    """Recibe un JSON por POST y lo devuelve con una respuesta"""
    datos = request.get_json()

    if not datos:
        return jsonify(error="No se recibió JSON"), 400

    # Aquí podrías procesar los datos como necesites
    return jsonify(
        message="Datos recibidos correctamente",
        datos=datos
    )

if __name__ == '__main__':
    app.run(debug=True)