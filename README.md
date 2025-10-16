# API de Equipos y Productos

Esta es una API Flask para gestionar equipos y productos utilizando una arquitectura limpia con separación de responsabilidades.

## Estructura del Proyecto

```
.
├── src/
│   ├── __init__.py
│   ├── app.py                    # Aplicación Flask principal
│   ├── entities/                 # Capa de entidades
│   │   ├── __init__.py
│   │   ├── equipment.py          # Entidad Equipment
│   │   └── product.py            # Entidad Product
│   ├── data_access/              # Capa de acceso a datos
│   │   ├── __init__.py
│   │   ├── db_connector.py       # Conector a la base de datos
│   │   ├── equipment_db.py       # Acceso a datos de Equipment
│   │   └── product_db.py         # Acceso a datos de Product
│   └── utils/                    # Utilidades
│       ├── __init__.py
│       ├── id_generator.py       # Generador de IDs
│       ├── time_helper.py        # Helper de tiempo
│       └── logger.py             # Sistema de logging
├── envs/
│   └── env.local.json            # Configuración de entorno local
├── serverless.yml                # Configuración de Serverless
├── create_tables.sql             # Script para crear tablas
└── test_api.py                   # Script de prueba
```

## Características

- **Arquitectura limpia**: Separación de responsabilidades entre entidades, acceso a datos y lógica de negocio
- **Logging**: Sistema de logging configurable para diferentes entornos (local, dev, prod)
- **JSONB**: Almacenamiento de datos en formato JSONB en PostgreSQL
- **Soft Delete**: Los registros se marcan como eliminados en lugar de borrarse físicamente
- **UUID**: Identificadores únicos universales para los registros

## Configuración

### Entornos

La aplicación soporta tres entornos de logging:

1. **local**: Muestra logs con colores y formato para desarrollo local
2. **dev**: Muestra logs sin colores para entornos de desarrollo en la nube (ej. CloudWatch)
3. **prod**: No muestra logs de debug o info (solo errores)

### Variables de Entorno

Las variables de entorno se configuran en `envs/env.local.json`:

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

## Endpoints

### Equipment

- `POST /equipment` - Crear un nuevo equipo
- `GET /equipment` - Obtener todos los equipos
- `GET /equipment/<equipment_id>` - Obtener un equipo específico
- `PUT /equipment/<equipment_id>` - Actualizar un equipo
- `DELETE /equipment/<equipment_id>` - Eliminar un equipo (soft delete)

### Products

- `POST /products` - Crear un nuevo producto
- `GET /products` - Obtener todos los productos
- `GET /products/<product_id>` - Obtener un producto específico
- `PUT /products/<product_id>` - Actualizar un producto
- `DELETE /products/<product_id>` - Eliminar un producto (soft delete)

## Ejemplos de Uso

### Crear un equipo

```bash
curl -X POST http://127.0.0.1:5000/equipment \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Máquina de Ensamblaje A-1",
    "location": "Planta 1, Sección 3",
    "serial_number": "SN-A1-12345"
  }'
```

### Crear un producto

```bash
curl -X POST http://127.0.0.1:5000/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Widget Estándar",
    "price": 29.99,
    "description": "Widget estándar para ensamblaje",
    "category": "Componentes"
  }'
```

### Obtener todos los equipos

```bash
curl http://127.0.0.1:5000/equipment
```

## Ejecución

### 1. Configurar la base de datos

Ejecuta el script SQL para crear las tablas:

```bash
psql -h tu_host -U tu_usuario -d tu_db -f create_tables.sql
```

### 2. Configurar las variables de entorno

Asegúrate de que `envs/env.local.json` tenga la configuración correcta de tu base de datos.

### 3. Ejecutar la aplicación

```bash
python src/app.py
```

La aplicación se ejecutará en `http://127.0.0.1:5000`

### 4. Probar la API

Ejecuta el script de prueba:

```bash
python test_api.py
```

## Logging

El sistema de logging muestra diferentes niveles de información según el entorno:

- **local**: Logs con colores y formato para desarrollo
- **dev**: Logs sin colores para entornos de desarrollo en la nube
- **prod**: Solo errores (no muestra debug o info)

Puedes cambiar el entorno modificando el valor de `LOGS` en `envs/env.local.json`.

## Despliegue con Serverless

Para desplegar en AWS Lambda usando Serverless Framework:

```bash
serverless deploy
```

La configuración está en `serverless.yml` y utiliza las variables de entorno definidas en `envs/env.{stage}.json`.

## Consideraciones

- Todos los registros se almacenan en formato JSONB en PostgreSQL
- Los registros eliminados se marcan como `deleted: true` en lugar de borrarse físicamente
- Los IDs de los registros son UUID para garantizar unicidad
- El sistema de logging es configurable y se adapta a diferentes entornos