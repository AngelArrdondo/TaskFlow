from app.database import get_db_connection, close_connection
from app.models import EtiquetaModel

class EtiquetaRepository:
    
    def get_all(self):
        connection = get_db_connection()
        if not connection:
            return []
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM etiquetas ORDER BY nombre")
        rows = cursor.fetchall()
        
        etiquetas = []
        for row in rows:
            etiqueta = EtiquetaModel(
                id=row['id'],
                nombre=row['nombre'],
                created_at=row['created_at']
            )
            etiquetas.append(etiqueta)
        
        close_connection(connection, cursor)
        return etiquetas
    
    def get_by_id(self, etiqueta_id):
        connection = get_db_connection()
        if not connection:
            return None
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM etiquetas WHERE id = %s", (etiqueta_id,))
        row = cursor.fetchone()
        
        if row:
            etiqueta = EtiquetaModel(
                id=row['id'],
                nombre=row['nombre'],
                created_at=row['created_at']
            )
            close_connection(connection, cursor)
            return etiqueta
        
        close_connection(connection, cursor)
        return None
    
    def get_by_nombre(self, nombre):
        connection = get_db_connection()
        if not connection:
            return None
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM etiquetas WHERE nombre = %s", (nombre,))
        row = cursor.fetchone()
        
        if row:
            etiqueta = EtiquetaModel(
                id=row['id'],
                nombre=row['nombre'],
                created_at=row['created_at']
            )
            close_connection(connection, cursor)
            return etiqueta
        
        close_connection(connection, cursor)
        return None
    
    def create(self, etiqueta_data):
        connection = get_db_connection()
        if not connection:
            return None
        
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO etiquetas (nombre) VALUES (%s)",
            (etiqueta_data.nombre,)
        )
        connection.commit()
        etiqueta_id = cursor.lastrowid
        close_connection(connection, cursor)
        
        return self.get_by_id(etiqueta_id)