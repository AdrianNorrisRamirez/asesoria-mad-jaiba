

### Paso 1: Crear el Archivo del Logger

Crea un nuevo archivo en la carpeta `utils`.

**`src/utils/logger.py`**
```python
import os

class AppLogger:
    # Variable de clase para determinar el entorno. Se configurará al inicio de la app.
    environment: str = os.environ.get('LOGS', 'local')

    # Códigos de color para la terminal
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

    def __init__(self, name: str):
        self.name = name

    def debug(self, message: str, variable=''):
        if self.environment == 'local':
            # Imprime con colores y formato para desarrollo local
            print(f'{self.BOLD}{self.OKCYAN}[{self.name}] {self.OKGREEN}{message}{self.RESET}', variable)
        elif self.environment == 'dev':
            # Imprime sin colores para entornos de desarrollo en la nube (ej. CloudWatch)
            print(f'[{self.name}] DEBUG: {message}', variable)
        # En 'prod', no hace nada (return None implícito)

    def info(self, message: str, variable=''):
        if self.environment == 'local':
            print(f'{self.BOLD}{self.WARNING}[{self.name}] {self.OKBLUE}{message}{self.RESET}', variable)
        elif self.environment == 'dev':
            print(f'[{self.name}] INFO: {message}', variable)
        # En 'prod', no hace nada

    def error(self, message: str, variable=''):
        if self.environment in ['local', 'dev']:
            local_format = f'{self.BOLD}{self.FAIL}[{self.name}] {message}{self.RESET}'
            cloud_format = f'[{self.name}] ERROR: {message}'
            print(local_format if self.environment == 'local' else cloud_format, variable)
        # En 'prod', no hace nada
```

---

### Paso 2: Integrar el Logger en la Aplicación

Ahora, conectaremos este logger al resto del código.

#### 1. Actualiza `src/utils/__init__.py`
Exporta el `AppLogger` para que sea fácil de importar en otros módulos.

```python
from .id_generator import IdGenerator
from .time_helper import TimeHelper
from .logger import AppLogger # <--- AÑADE ESTA LÍNEA

id_generator = IdGenerator
time_helper = TimeHelper
logger = AppLogger # <--- AÑADE ESTA LÍNEA
```

#### 2. Configura las Variables de Entorno
Necesitamos añadir la variable `LOGS` a nuestros archivos de configuración.

**`envs/env.local.json` (actualizado)**
```json
{
  "DB_HOST": "tu_host",
  "DB_PORT": 5432,
  "DB_NAME": "tu_db",
  "DB_USER": "tu_usuario",
  "DB_PASS": "tu_contraseña_con_caracteres_raros",
  "LOGS": "local" 
}
```

**`serverless.yml` (actualizado)**
Añade `LOGS` a la sección de `environment`.

```yaml
# ... (otras partes de tu serverless.yml)
provider:
  name: aws
  runtime: python3.11
  region: us-west-1
  timeout: 10
  stage: ${opt:stage, 'local'}

  environment:
    STAGE: ${self:provider.stage}
    DB_HOST: ${file(./envs/env.${self:provider.stage}.json):DB_HOST}
    DB_PORT: ${file(./envs/env.${self:provider.stage}.json):DB_PORT}
    DB_NAME: ${file(./envs/env.${self:provider.stage}.json):DB_NAME}
    DB_USER: ${file(./envs/env.${self:provider.stage}.json):DB_USER}
    DB_PASS: ${file(./envs/env.${self:provider.stage}.json):DB_PASS}
    LOGS: ${file(./envs/env.${self:provider.stage}.json):LOGS, 'prod'} # <--- AÑADE ESTA LÍNEA

# ... (resto del archivo)
```
*Nota: `${... , 'prod'}` establece 'prod' como valor por defecto si la variable `LOGS` no se encuentra en el archivo de entorno. Es una buena práctica de seguridad para producción.*

#### 3. Usa el Logger en tu Código
Ahora reemplazaremos los `print()` con nuestro nuevo logger.

**`src/data_access/db_connector.py` (actualizado)**
Este es un lugar perfecto para usar el logger y ver si la conexión funciona o falla.

```python
import os
import psycopg2
import psycopg2.extras
from src.utils import logger # <--- Importa el logger

log = logger('DB_Connector') # <--- Crea una instancia del logger

class DatabaseConnector:
    def __init__(self):
        self.db_host = os.environ.get("DB_HOST")
        self.db_port = os.environ.get("DB_PORT")
        self.db_name = os.environ.get("DB_NAME")
        self.db_user = os.environ.get("DB_USER")
        self.db_pass = os.environ.get("DB_PASS")
        self.connection = None

    def get_connection(self):
        try:
            self.connection = psycopg2.connect(
                host=self.db_host,
                port=self.db_port,
                dbname=self.db_name,
                user=self.db_user,
                password=self.db_pass,
                client_encoding='utf8'
            )
            log.debug("✅ Conexión a PostgreSQL exitosa.") # <--- Reemplaza print()
            return self.connection
        except Exception as e:
            log.error(f"❌ Error al conectar a PostgreSQL: ", e) # <--- Reemplaza print()
            raise

    def close_connection(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            log.debug("🔌 Conexión a PostgreSQL cerrada.") # <--- Reemplaza print()

# Instancia única que se usará en toda la aplicación
db_connector = DatabaseConnector()
```

**`src/app.py` (actualizado)**
Vamos a añadir logs a nuestras rutas para ver cuándo se ejecutan.

```python
from flask import Flask, jsonify
from src.entities import Organization, User
from src.data_access import organization_db, user_db
from src.utils import logger # <--- Importa el logger

# Configura el nivel del logger para toda la aplicación desde la variable de entorno
# Esta es la línea más importante para que el logger sepa en qué entorno está
logger.environment = os.environ.get('LOGS', 'local')

log = logger('Flask_App') # <--- Crea una instancia del logger para este archivo

app = Flask(__name__)

@app.route('/')
def index():
    log.info("Ruta raíz '/' fue accedida.")
    return "API de asesoría lista. Usa /create-test-data para empezar."

@app.route('/create-test-data', methods=['GET'])
def create_test_data():
    log.info("Iniciando la creación de datos de prueba...")
    try:
        # 1. Crear una organización
        log.debug("Creando instancia de Organization...")
        org = Organization(name="Mi Empresa", createdBy="system")
        created_org = organization_db.insert_one(org.get_id(), org.get_data())
        log.debug("Organización creada:", created_org)
        
        # 2. Crear un usuario y asociarlo a la organización
        log.debug("Creando instancia de User...")
        user = User(
            name="Juan Perez",
            email="juan.perez@miempresa.com",
            organization_id=org.get_id(),
            createdBy="system"
        )
        created_user = user_db.insert_one(user.get_id(), user.get_data())
        log.debug("Usuario creado:", created_user)
        
        return jsonify({
            "message": "Datos de prueba creados exitosamente!",
            "organization": created_org,
            "user": created_user
        }), 201

    except Exception as e:
        log.error("No se pudieron crear los datos de prueba:", e)
        return jsonify({"error": f"No se pudieron crear los datos de prueba: {str(e)}"}), 500

@app.route('/users', methods=['GET'])
def get_all_users():
    log.info("Solicitud para obtener todos los usuarios recibida.")
    try:
        users = user_db.find_all()
        log.debug(f"Se encontraron {len(users)} usuarios.")
        return jsonify(users), 200
    except Exception as e:
        log.error("Error al obtener usuarios:", e)
        return jsonify({"error": f"Error al obtener usuarios: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
```

---



```bash
[Flask_App] INFO: Iniciando la creación de datos de prueba...
[Flask_App] DEBUG: Creando instancia de Organization...
[DB_Connector] DEBUG: ✅ Conexión a PostgreSQL exitosa.
[DB_Connector] DEBUG: 🔌 Conexión a PostgreSQL cerrada.
[Flask_App] DEBUG: Organización creada: {'id': '...', 'name': 'Mi Empresa', ...}
[Flask_App] DEBUG: Creando instancia de User...
[DB_Connector] DEBUG: ✅ Conexión a PostgreSQL exitosa.
[DB_Connector] DEBUG: 🔌 Conexión a PostgreSQL cerrada.
[Flask_App] DEBUG: Usuario creado: {'id': '...', 'name': 'Juan Perez', ...}
```

Si cambias el valor de `"LOGS"` a `"dev"` en tu `env.local.json`, los logs aparecerán sin colores, simulando cómo se verían en AWS CloudWatch. Si lo cambias a `"prod"`, no aparecerá ningún log de `debug` o `info`. de `debug` o `info`.




### Estructura de Archivos (sin cambios)

La estructura sigue siendo la misma, lo que demuestra la flexibilidad del diseño:

```
.
├── src/
│   ├── __init__.py
│   ├── app.py
│   │
│   ├── data_access/
│   │   ├── __init__.py
│   │   ├── db_connector.py
│   │   ├── equipment_db.py   # <-- CAMBIO
│   │   └── product_db.py     # <-- CAMBIO
│   │
│   ├── entities/
│   │   ├── __init__.py
│   │   ├── equipment.py      # <-- CAMBIO
│   │   └── product.py        # <-- CAMBIO
│   │
│   └── utils/
│       ├── __init__.py
│       ├── id_generator.py
│       ├── logger.py
│       └── time_helper.py
│
├── envs/
│   └── env.local.json
│
└── serverless.yml
```

---

### 1. SQL para Crear las Nuevas Tablas

Primero, ejecuta estas sentencias SQL en tu base de datos PostgreSQL para crear las tablas `equipment` y `products`.

```sql
-- Elimina las tablas viejas si existen, para empezar de cero
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS organizations;

-- Crear la tabla para Equipos (Equipment)
CREATE TABLE equipment (
    id UUID PRIMARY KEY,
    data JSONB
);

-- Crear la tabla para Productos (Products)
CREATE TABLE products (
    id UUID PRIMARY KEY,
    data JSONB
);
```

---

### 2. Archivos de Código Fuente (`src`) Actualizados

Aquí está el contenido de todos los archivos necesarios, actualizados para `Equipment` y `Product`. Los archivos de `utils` (`id_generator.py`, `time_helper.py`, `logger.py`, `__init__.py`) no cambian, así que los omitiré para mayor claridad.

#### `src/entities/equipment.py` (Nuevo)
Define la entidad `Equipment`.

```python
from src.utils import id_generator, time_helper

class Equipment:
    def __init__(self, id=None, name=None, location=None, createdBy=None, **kwargs):
        
        if not name or not location:
            raise ValueError("El nombre y la ubicación del equipo son requeridos.")

        self.id = id or id_generator.make_id()
        self.name = name
        self.location = location
        self.serial_number = kwargs.get('serial_number', 'N/A')
        self.createdBy = createdBy
        self.createdAt = kwargs.get('createdAt') or time_helper.now()
        self.modifiedAt = time_helper.now()
        self.deleted = kwargs.get('deleted', False)

    def get_id(self):
        return self.id

    def get_data(self):
        # Devuelve todos los datos que irán en la columna JSONB
        return {
            "name": self.name,
            "location": self.location,
            "serial_number": self.serial_number,
            "createdBy": self.createdBy,
            "createdAt": self.createdAt,
            "modifiedAt": self.modifiedAt,
            "deleted": self.deleted
        }
```

#### `src/entities/product.py` (Nuevo)
Define la entidad `Product` y su relación con `Equipment`.

```python
from src.utils import id_generator, time_helper

class Product:
    def __init__(self, id=None, name=None, sku=None, equipment_id=None, createdBy=None, **kwargs):

        if not name or not sku or not equipment_id:
            raise ValueError("Nombre, SKU y equipment_id son requeridos.")

        self.id = id or id_generator.make_id()
        self.name = name
        self.sku = sku
        self.equipment_id = equipment_id  # Clave de la relación
        self.createdBy = createdBy
        self.createdAt = kwargs.get('createdAt') or time_helper.now()
        self.modifiedAt = time_helper.now()
        self.deleted = kwargs.get('deleted', False)

    def get_id(self):
        return self.id

    def get_data(self):
        return {
            "name": self.name,
            "sku": self.sku,
            "equipment_id": self.equipment_id,
            "createdBy": self.createdBy,
            "createdAt": self.createdAt,
            "modifiedAt": self.modifiedAt,
            "deleted": self.deleted
        }
```

#### `src/entities/__init__.py` (Actualizado)

```python
from .equipment import Equipment
from .product import Product
```

#### `src/data_access/db_connector.py` (Sin cambios)
Este archivo es genérico y no necesita modificaciones.

```python
import os
import psycopg2
import psycopg2.extras
from src.utils import logger

log = logger('DB_Connector')

class DatabaseConnector:
    def __init__(self):
        self.db_host = os.environ.get("DB_HOST")
        self.db_port = os.environ.get("DB_PORT")
        self.db_name = os.environ.get("DB_NAME")
        self.db_user = os.environ.get("DB_USER")
        self.db_pass = os.environ.get("DB_PASS")
        self.connection = None

    def get_connection(self):
        try:
            self.connection = psycopg2.connect(
                host=self.db_host,
                port=self.db_port,
                dbname=self.db_name,
                user=self.db_user,
                password=self.db_pass,
                client_encoding='utf8'
            )
            log.debug("✅ Conexión a PostgreSQL exitosa.")
            return self.connection
        except Exception as e:
            log.error(f"❌ Error al conectar a PostgreSQL: ", e)
            raise

    def close_connection(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            log.debug("🔌 Conexión a PostgreSQL cerrada.")

db_connector = DatabaseConnector()
```

#### `src/data_access/equipment_db.py` (Nuevo)
El driver para las operaciones de la tabla `equipment`.

```python
import json
from .db_connector import db_connector

class EquipmentDb:
    def insert_one(self, eq_id, data):
        conn = db_connector.get_connection()
        try:
            with conn.cursor() as cursor:
                query = "INSERT INTO equipment (id, data) VALUES (%s, %s::jsonb)"
                cursor.execute(query, (eq_id, json.dumps(data)))
                conn.commit()
            return {"id": eq_id, **data}
        finally:
            db_connector.close_connection()

    def find_all(self):
        conn = db_connector.get_connection()
        try:
            with conn.cursor() as cursor:
                query = "SELECT id, data FROM equipment WHERE (data->>'deleted')::boolean = false"
                cursor.execute(query)
                results = [{"id": row[0], **row[1]} for row in cursor.fetchall()]
                return results
        finally:
            db_connector.close_connection()

equipment_db = EquipmentDb()
```

#### `src/data_access/product_db.py` (Nuevo)
El driver para la tabla `products`. Incluye una función para buscar productos por `equipment_id`.

```python
import json
from .db_connector import db_connector

class ProductDb:
    def insert_one(self, prod_id, data):
        conn = db_connector.get_connection()
        try:
            with conn.cursor() as cursor:
                query = "INSERT INTO products (id, data) VALUES (%s, %s::jsonb)"
                cursor.execute(query, (prod_id, json.dumps(data)))
                conn.commit()
            return {"id": prod_id, **data}
        finally:
            db_connector.close_connection()

    def find_by_equipment_id(self, equipment_id):
        conn = db_connector.get_connection()
        try:
            with conn.cursor() as cursor:
                # Consulta JSONB para filtrar por un campo dentro del objeto 'data'
                query = """
                    SELECT id, data 
                    FROM products 
                    WHERE data->>'equipment_id' = %s 
                    AND (data->>'deleted')::boolean = false
                """
                cursor.execute(query, (equipment_id,))
                results = [{"id": row[0], **row[1]} for row in cursor.fetchall()]
                return results
        finally:
            db_connector.close_connection()

product_db = ProductDb()
```

#### `src/data_access/__init__.py` (Actualizado)

```python
from .equipment_db import equipment_db
from .product_db import product_db
```

#### `src/app.py` (Actualizado)
La aplicación Flask con nuevas rutas para `equipment` y `products`.

```python
import os
from flask import Flask, jsonify, request
from src.entities import Equipment, Product
from src.data_access import equipment_db, product_db
from src.utils import logger

# Configura el logger para la aplicación
logger.environment = os.environ.get('LOGS', 'local')
log = logger('Flask_App')

app = Flask(__name__)

@app.route('/')
def index():
    log.info("Ruta raíz '/' fue accedida.")
    return "API de Equipos y Productos lista."

@app.route('/equipment', methods=['POST'])
def create_equipment():
    """Crea un nuevo equipo."""
    log.info("Recibida solicitud para crear equipo.")
    try:
        data = request.get_json()
        if not data or 'name' not in data or 'location' not in data:
            raise ValueError("Los campos 'name' y 'location' son requeridos.")
        
        log.debug("Datos recibidos:", data)
        equipment = Equipment(
            name=data['name'],
            location=data['location'],
            serial_number=data.get('serial_number'),
            createdBy="api_user" # Simula un usuario autenticado
        )
        created_equipment = equipment_db.insert_one(equipment.get_id(), equipment.get_data())
        log.info("Equipo creado exitosamente:", created_equipment)
        
        return jsonify(created_equipment), 201

    except Exception as e:
        log.error("Error al crear equipo:", e)
        return jsonify({"error": str(e)}), 400

@app.route('/equipment', methods=['GET'])
def get_all_equipment():
    """Obtiene todos los equipos."""
    log.info("Recibida solicitud para obtener todos los equipos.")
    try:
        all_equipment = equipment_db.find_all()
        log.debug(f"Se encontraron {len(all_equipment)} equipos.")
        return jsonify(all_equipment), 200
    except Exception as e:
        log.error("Error al obtener equipos:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/products', methods=['POST'])
def create_product():
    """Crea un nuevo producto asociado a un equipo."""
    log.info("Recibida solicitud para crear producto.")
    try:
        data = request.get_json()
        if not data or 'name' not in data or 'sku' not in data or 'equipment_id' not in data:
            raise ValueError("Los campos 'name', 'sku' y 'equipment_id' son requeridos.")
            
        log.debug("Datos recibidos:", data)
        product = Product(
            name=data['name'],
            sku=data['sku'],
            equipment_id=data['equipment_id'],
            createdBy="api_user"
        )
        created_product = product_db.insert_one(product.get_id(), product.get_data())
        log.info("Producto creado exitosamente:", created_product)
        
        return jsonify(created_product), 201
        
    except Exception as e:
        log.error("Error al crear producto:", e)
        return jsonify({"error": str(e)}), 400

@app.route('/equipment/<equipment_id>/products', methods=['GET'])
def get_products_by_equipment(equipment_id):
    """Obtiene todos los productos de un equipo específico."""
    log.info(f"Buscando productos para el equipo con ID: {equipment_id}")
    try:
        products = product_db.find_by_equipment_id(equipment_id)
        log.debug(f"Se encontraron {len(products)} productos para este equipo.")
        return jsonify(products), 200
    except Exception as e:
        log.error(f"Error al obtener productos para el equipo {equipment_id}:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
```

### 3. Cómo Probar la Nueva Versión

1.  **Ejecuta el SQL** para crear las nuevas tablas.
2.  **Ejecuta tu aplicación Flask localmente**: `python -m src.app`.
3.  **Usa Postman o una herramienta similar** para interactuar con tu API:

    *   **Crear un Equipo:**
        *   `POST` a `http://127.0.0.1:5000/equipment`
        *   Body (raw, JSON):
            ```json
            {
                "name": "Máquina de Ensamblaje A-1",
                "location": "Planta 1, Sección 3",
                "serial_number": "SN-A1-12345"
            }
            ```
        *   Copia el `"id"` del equipo que se crea.

    *   **Crear un Producto para ese Equipo:**
        *   `POST` a `http://127.0.0.1:5000/products`
        *   Body (raw, JSON) - **usa el `id` del paso anterior**:
            ```json
            {
                "name": "Widget Estándar",
                "sku": "WID-STD-001",
                "equipment_id": "pega_el_id_del_equipo_aqui"
            }
            ```

    *   **Listar todos los Equipos:**
        *   `GET` a `http://127.0.0.1:5000/equipment`

    *   **Listar los Productos de un Equipo Específico:**
        *   `GET` a `http://127.0.0.1:5000/equipment/pega_el_id_del_equipo_aqui/products`

