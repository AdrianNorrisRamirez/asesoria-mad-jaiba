import datetime
import pytz

class TimeHelper:
    def __init__(self, timezone='UTC'):
        """
        Inicializa el TimeHelper con una zona horaria específica.
        
        Args:
            timezone (str): Zona horaria en formato string (ej: 'UTC', 'America/Mexico_City', 'Europe/Madrid')
        """
        try:
            self.timezone = pytz.timezone(timezone)
        except pytz.UnknownTimeZoneError:
            # Si la zona horaria no es válida, usar UTC por defecto
            self.timezone = pytz.UTC
            print(f"⚠️ Zona horaria '{timezone}' no válida. Se usará UTC por defecto.")

    def now(self):
        """Devuelve la fecha y hora actual en formato ISO 8601 con la zona horaria configurada"""
        now_utc = datetime.datetime.now(pytz.UTC)
        now_local = now_utc.astimezone(self.timezone)
        return now_local.isoformat()

    def format_timestamp(self, timestamp=None):
        """Formatea un timestamp en formato legible con la zona horaria configurada"""
        if timestamp is None:
            timestamp = datetime.datetime.now(pytz.UTC)
        elif isinstance(timestamp, str):
            try:
                # Intentar parsear como ISO format
                timestamp = datetime.datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            except ValueError:
                # Si no es ISO, asumir que es string y usar fromisoformat directamente
                timestamp = datetime.datetime.fromisoformat(timestamp)
        
        # Asegurarse de que el timestamp tenga información de zona horaria
        if timestamp.tzinfo is None:
            timestamp = pytz.UTC.localize(timestamp)
        
        # Convertir a la zona horaria local
        timestamp_local = timestamp.astimezone(self.timezone)
        return timestamp_local.strftime("%Y-%m-%d %H:%M:%S %Z")

    def now_utc(self):
        """Devuelve la fecha y hora actual en UTC en formato ISO 8601"""
        return datetime.datetime.now(pytz.UTC).isoformat()

    def format_timestamp_utc(self, timestamp=None):
        """Formatea un timestamp en formato UTC"""
        if timestamp is None:
            timestamp = datetime.datetime.now(pytz.UTC)
        elif isinstance(timestamp, str):
            try:
                timestamp = datetime.datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            except ValueError:
                timestamp = datetime.datetime.fromisoformat(timestamp)
        
        if timestamp.tzinfo is None:
            timestamp = pytz.UTC.localize(timestamp)
        
        return timestamp.strftime("%Y-%m-%d %H:%M:%S UTC")

# Instancia global por defecto (UTC)
time_helper = TimeHelper()

# Funciones compatibles para mantener retrocompatibilidad
def now():
    """Devuelve la fecha y hora actual en formato ISO 8601 (usando la instancia global)"""
    return time_helper.now()

def format_timestamp(timestamp=None):
    """Formatea un timestamp en formato legible (usando la instancia global)"""
    return time_helper.format_timestamp(timestamp)