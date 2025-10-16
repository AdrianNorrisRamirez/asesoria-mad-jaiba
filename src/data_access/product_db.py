import psycopg2.extras
from src.data_access.db_connector import db_connector
from src.entities import Product
from src.utils import logger

log = logger('Product_DB')

class ProductDB:
    def __init__(self):
        self.db = db_connector
        self.connection = None

    def get_connection(self):
        if not self.connection:
            self.connection = self.db.get_connection()
        return self.connection

    def close_connection(self):
        if self.connection:
            self.db.close_connection()
            self.connection = None

    def create_product(self, product_data):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            product = Product(
                name=product_data.get('name'),
                price=product_data.get('price'),
                description=product_data.get('description', ''),
                category=product_data.get('category', 'General'),
                createdBy=product_data.get('createdBy')
            )
            
            query = """
                INSERT INTO public."Product" (id, data)
                VALUES (%s, %s)
                RETURNING id
            """
            
            cursor.execute(query, (product.get_id(), product.get_data()))
            connection.commit()
            
            log.info(f"✅ Producto creado exitosamente con ID: {product.get_id()}")
            return product.get_id()
            
        except Exception as e:
            if connection:
                connection.rollback()
            log.error(f"❌ Error al crear producto: ", e)
            raise
        finally:
            if cursor:
                cursor.close()

    def get_product_by_id(self, product_id):
        try:
            connection = self.get_connection()
            cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            
            query = 'SELECT id, data FROM public."Product" WHERE id = %s'
            cursor.execute(query, (product_id,))
            result = cursor.fetchone()
            
            if result:
                data = result['data']
                product = Product(
                    id=result['id'],
                    name=data['name'],
                    price=data['price'],
                    description=data['description'],
                    category=data['category'],
                    createdBy=data['createdBy'],
                    createdAt=data['createdAt'],
                    modifiedAt=data['modifiedAt'],
                    deleted=data['deleted']
                )
                log.debug(f"✅ Producto encontrado con ID: {product_id}")
                return product
            else:
                log.warning(f"⚠️ No se encontró producto con ID: {product_id}")
                return None
                
        except Exception as e:
            log.error(f"❌ Error al obtener producto por ID: ", e)
            raise
        finally:
            if cursor:
                cursor.close()

    def get_all_products(self):
        try:
            connection = self.get_connection()
            cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            
            query = 'SELECT id, data FROM public."Product" WHERE data->>\'deleted\' = \'false\' ORDER BY data->>\'createdAt\' DESC'
            cursor.execute(query)
            results = cursor.fetchall()
            
            product_list = []
            for result in results:
                data = result['data']
                product = Product(
                    id=result['id'],
                    name=data['name'],
                    price=data['price'],
                    description=data['description'],
                    category=data['category'],
                    createdBy=data['createdBy'],
                    createdAt=data['createdAt'],
                    modifiedAt=data['modifiedAt'],
                    deleted=data['deleted']
                )
                product_list.append(product)
            
            log.debug(f"✅ Se encontraron {len(product_list)} productos")
            return product_list
            
        except Exception as e:
            log.error(f"❌ Error al obtener todos los productos: ", e)
            raise
        finally:
            if cursor:
                cursor.close()

    def update_product(self, product_id, product_data):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            # Obtener producto existente
            existing_product = self.get_product_by_id(product_id)
            if not existing_product:
                raise ValueError(f"Producto con ID {product_id} no encontrado")
            
            # Actualizar datos
            existing_product.name = product_data.get('name', existing_product.name)
            existing_product.price = product_data.get('price', existing_product.price)
            existing_product.description = product_data.get('description', existing_product.description)
            existing_product.category = product_data.get('category', existing_product.category)
            existing_product.modifiedAt = existing_product.modifiedAt
            
            query = """
                UPDATE public."Product"
                SET data = %s
                WHERE id = %s
            """
            
            cursor.execute(query, (existing_product.get_data(), product_id))
            connection.commit()
            
            log.info(f"✅ Producto actualizado exitosamente con ID: {product_id}")
            return product_id
            
        except Exception as e:
            if connection:
                connection.rollback()
            log.error(f"❌ Error al actualizar producto: ", e)
            raise
        finally:
            if cursor:
                cursor.close()

    def delete_product(self, product_id):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            # Obtener producto existente
            existing_product = self.get_product_by_id(product_id)
            if not existing_product:
                raise ValueError(f"Producto con ID {product_id} no encontrado")
            
            # Marcar como eliminado
            existing_product.deleted = True
            existing_product.modifiedAt = existing_product.modifiedAt
            
            query = """
                UPDATE public."Product"
                SET data = %s
                WHERE id = %s
            """
            
            cursor.execute(query, (existing_product.get_data(), product_id))
            connection.commit()
            
            log.info(f"✅ Producto eliminado (marcado como eliminado) con ID: {product_id}")
            return product_id
            
        except Exception as e:
            if connection:
                connection.rollback()
            log.error(f"❌ Error al eliminar producto: ", e)
            raise
        finally:
            if cursor:
                cursor.close()