import psycopg2.extras
from src.data_access.db_connector import db_connector
from src.entities import Equipment
from src.utils import logger

log = logger('Equipment_DB')

class EquipmentDB:
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

    def create_equipment(self, equipment_data):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            equipment = Equipment(
                name=equipment_data.get('name'),
                location=equipment_data.get('location'),
                serial_number=equipment_data.get('serial_number', 'N/A'),
                createdBy=equipment_data.get('createdBy')
            )
            
            query = """
                INSERT INTO public."Equipment" (id, data)
                VALUES (%s, %s)
                RETURNING id
            """
            
            cursor.execute(query, (equipment.get_id(), equipment.get_data()))
            connection.commit()
            
            log.info(f"✅ Equipo creado exitosamente con ID: {equipment.get_id()}")
            return equipment.get_id()
            
        except Exception as e:
            if connection:
                connection.rollback()
            log.error(f"❌ Error al crear equipo: ", e)
            raise
        finally:
            if cursor:
                cursor.close()

    def get_equipment_by_id(self, equipment_id):
        try:
            connection = self.get_connection()
            cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            
            query = 'SELECT id, data FROM public."Equipment" WHERE id = %s'
            cursor.execute(query, (equipment_id,))
            result = cursor.fetchone()
            
            if result:
                data = result['data']
                equipment = Equipment(
                    id=result['id'],
                    name=data['name'],
                    location=data['location'],
                    serial_number=data['serial_number'],
                    createdBy=data['createdBy'],
                    createdAt=data['createdAt'],
                    modifiedAt=data['modifiedAt'],
                    deleted=data['deleted']
                )
                log.debug(f"✅ Equipo encontrado con ID: {equipment_id}")
                return equipment
            else:
                log.warning(f"⚠️ No se encontró equipo con ID: {equipment_id}")
                return None
                
        except Exception as e:
            log.error(f"❌ Error al obtener equipo por ID: ", e)
            raise
        finally:
            if cursor:
                cursor.close()

    def get_all_equipment(self):
        try:
            connection = self.get_connection()
            cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            
            query = 'SELECT id, data FROM public."Equipment" WHERE data->>\'deleted\' = \'false\' ORDER BY data->>\'createdAt\' DESC'
            cursor.execute(query)
            results = cursor.fetchall()
            
            equipment_list = []
            for result in results:
                data = result['data']
                equipment = Equipment(
                    id=result['id'],
                    name=data['name'],
                    location=data['location'],
                    serial_number=data['serial_number'],
                    createdBy=data['createdBy'],
                    createdAt=data['createdAt'],
                    modifiedAt=data['modifiedAt'],
                    deleted=data['deleted']
                )
                equipment_list.append(equipment)
            
            log.debug(f"✅ Se encontraron {len(equipment_list)} equipos")
            return equipment_list
            
        except Exception as e:
            log.error(f"❌ Error al obtener todos los equipos: ", e)
            raise
        finally:
            if cursor:
                cursor.close()

    def update_equipment(self, equipment_id, equipment_data):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            # Obtener equipo existente
            existing_equipment = self.get_equipment_by_id(equipment_id)
            if not existing_equipment:
                raise ValueError(f"Equipo con ID {equipment_id} no encontrado")
            
            # Actualizar datos
            existing_equipment.name = equipment_data.get('name', existing_equipment.name)
            existing_equipment.location = equipment_data.get('location', existing_equipment.location)
            existing_equipment.serial_number = equipment_data.get('serial_number', existing_equipment.serial_number)
            existing_equipment.modifiedAt = existing_equipment.modifiedAt
            
            query = """
                UPDATE public."Equipment"
                SET data = %s
                WHERE id = %s
            """
            
            cursor.execute(query, (existing_equipment.get_data(), equipment_id))
            connection.commit()
            
            log.info(f"✅ Equipo actualizado exitosamente con ID: {equipment_id}")
            return equipment_id
            
        except Exception as e:
            if connection:
                connection.rollback()
            log.error(f"❌ Error al actualizar equipo: ", e)
            raise
        finally:
            if cursor:
                cursor.close()

    def delete_equipment(self, equipment_id):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            # Obtener equipo existente
            existing_equipment = self.get_equipment_by_id(equipment_id)
            if not existing_equipment:
                raise ValueError(f"Equipo con ID {equipment_id} no encontrado")
            
            # Marcar como eliminado
            existing_equipment.deleted = True
            existing_equipment.modifiedAt = existing_equipment.modifiedAt
            
            query = """
                UPDATE public."Equipment"
                SET data = %s
                WHERE id = %s
            """
            
            cursor.execute(query, (existing_equipment.get_data(), equipment_id))
            connection.commit()
            
            log.info(f"✅ Equipo eliminado (marcado como eliminado) con ID: {equipment_id}")
            return equipment_id
            
        except Exception as e:
            if connection:
                connection.rollback()
            log.error(f"❌ Error al eliminar equipo: ", e)
            raise
        finally:
            if cursor:
                cursor.close()