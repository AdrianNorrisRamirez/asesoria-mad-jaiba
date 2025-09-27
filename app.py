from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hola, bienvenido a mi aplicación Flask verguera!"