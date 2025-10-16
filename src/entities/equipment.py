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