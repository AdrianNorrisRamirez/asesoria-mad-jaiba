import os
from flask import Flask, jsonify, request
#from src.entities import Equipment, Product
#from src.data_access import EquipmentDB, ProductDB
from src.utils import logger

# Configura el logger para la aplicación
logger.environment = os.environ.get('LOGS', 'local')
log = logger('Flask_App')

app = Flask(__name__)

log.debug("Corriendo app flask")

log.info("Corriendo app flask")

log.error("Corriendo app flask")

# Instancias de los data access
#equipment_db = EquipmentDB()
#product_db = ProductDB()

@app.route('/')
def index():
    log.info("Ruta raíz '/' fue accedida.")
    return "API de Equipos y Productos lista."


if __name__ == '__main__':
    app.run(debug=True)