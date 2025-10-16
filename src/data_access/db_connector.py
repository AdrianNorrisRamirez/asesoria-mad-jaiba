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