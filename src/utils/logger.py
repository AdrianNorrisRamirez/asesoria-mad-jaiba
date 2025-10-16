import os
from src.utils.time_helper import TimeHelper

time = TimeHelper("America/Mexico_City")

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

    def _format_message(self, level: str, message: str):
        """Formatea el mensaje con timestamp y nombre del logger"""
        timestamp = time.format_timestamp()
        return f"[{timestamp}] [{self.name}] {level}: {message}"

    def debug(self, message: str, variable=''):
        if self.environment == 'local':
            # Imprime con colores y formato para desarrollo local
            formatted_msg = self._format_message('DEBUG', message)
            print(f'{self.BOLD}{self.OKCYAN}{formatted_msg}{self.RESET}', variable)
        elif self.environment == 'cloud':
            # Imprime sin colores para entornos de desarrollo en la nube (ej. CloudWatch)
            formatted_msg = self._format_message('DEBUG', message)
            print(formatted_msg, variable)
        # En 'prod', no hace nada (return None implícito)

    def info(self, message: str, variable=''):
        if self.environment == 'local':
            formatted_msg = self._format_message('INFO', message)
            print(f'{self.BOLD}{self.WARNING}{formatted_msg}{self.RESET}', variable)
        elif self.environment == 'cloud':
            formatted_msg = self._format_message('INFO', message)
            print(formatted_msg, variable)
        # En 'prod', no hace nada

    def error(self, message: str, variable=''):
        if self.environment in ['local', 'cloud']:
            formatted_msg = self._format_message('ERROR', message)
            if self.environment == 'local':
                print(f'{self.BOLD}{self.FAIL}{formatted_msg}{self.RESET}', variable)
            else:
                print(formatted_msg, variable)
        # En 'prod', no hace nada