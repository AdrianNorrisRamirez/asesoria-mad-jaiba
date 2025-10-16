from src.utils import id_generator, time_helper

class Product:
    def __init__(self, id=None, name=None, price=None, createdBy=None, **kwargs):
        
        if not name or not price:
            raise ValueError("El nombre y el precio del producto son requeridos.")

        self.id = id or id_generator.make_id()
        self.name = name
        self.price = float(price) if price else 0.0
        self.description = kwargs.get('description', '')
        self.category = kwargs.get('category', 'General')
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
            "price": self.price,
            "description": self.description,
            "category": self.category,
            "createdBy": self.createdBy,
            "createdAt": self.createdAt,
            "modifiedAt": self.modifiedAt,
            "deleted": self.deleted
        }