from app.database import get_db_connection, close_connection
from app.models import TareaModel
from datetime import date

class TareaRepository:
    
    def get_all(self, completada=None, page=1, limit=10):
        connection = get_db_connection()
        if not connection:
            return []
        
        cursor = connection.cursor(dictionary=True)
        offset = (page - 1) * limit
        
        query = "SELECT * FROM tareas"
        params = []
        
        if completada is not None:
            query += " WHERE completada = %s"
            params.append(completada)
        
        query += " LIMIT %s OFFSET %s"
        params.extend([limit, offset])
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        # Obtener etiquetas para cada tarea
        tareas = []
        for row in rows:
            tarea = TareaModel(
                id=row['id'],
                titulo=row['titulo'],
                descripcion=row['descripcion'],
                fecha_limite=row['fecha_limite'],
                completada=bool(row['completada']),
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
            
            # Obtener etiquetas de esta tarea
            cursor.execute("""
                SELECT e.* FROM etiquetas e
                JOIN tarea_etiqueta te ON e.id = te.etiqueta_id
                WHERE te.tarea_id = %s
            """, (tarea.id,))
            etiquetas = cursor.fetchall()
            tarea.etiquetas = etiquetas
            
            tareas.append(tarea)
        
        close_connection(connection, cursor)
        return tareas
    
    def get_by_id(self, tarea_id):
        connection = get_db_connection()
        if not connection:
            return None
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tareas WHERE id = %s", (tarea_id,))
        row = cursor.fetchone()
        
        if row:
            tarea = TareaModel(
                id=row['id'],
                titulo=row['titulo'],
                descripcion=row['descripcion'],
                fecha_limite=row['fecha_limite'],
                completada=bool(row['completada']),
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
            
            # Obtener etiquetas
            cursor.execute("""
                SELECT e.* FROM etiquetas e
                JOIN tarea_etiqueta te ON e.id = te.etiqueta_id
                WHERE te.tarea_id = %s
            """, (tarea_id,))
            tarea.etiquetas = cursor.fetchall()
            
            close_connection(connection, cursor)
            return tarea
        
        close_connection(connection, cursor)
        return None
    
    def create(self, tarea_data):
        connection = get_db_connection()
        if not connection:
            return None
        
        cursor = connection.cursor()
        query = """
            INSERT INTO tareas (titulo, descripcion, fecha_limite, completada)
            VALUES (%s, %s, %s, %s)
        """
        values = (
            tarea_data.titulo,
            tarea_data.descripcion,
            tarea_data.fecha_limite,
            tarea_data.completada
        )
        
        cursor.execute(query, values)
        connection.commit()
        tarea_id = cursor.lastrowid
        close_connection(connection, cursor)
        
        return self.get_by_id(tarea_id)
    
    def update(self, tarea_id, tarea_data):
        connection = get_db_connection()
        if not connection:
            return None
        
        cursor = connection.cursor()
        query = """
            UPDATE tareas 
            SET titulo = %s, descripcion = %s, fecha_limite = %s, completada = %s
            WHERE id = %s
        """
        values = (
            tarea_data.titulo,
            tarea_data.descripcion,
            tarea_data.fecha_limite,
            tarea_data.completada,
            tarea_id
        )
        
        cursor.execute(query, values)
        connection.commit()
        close_connection(connection, cursor)
        
        return self.get_by_id(tarea_id)
    
    def patch(self, tarea_id, data):
        connection = get_db_connection()
        if not connection:
            return None
        
        cursor = connection.cursor()
        fields = []
        values = []
        
        if 'completada' in data:
            fields.append("completada = %s")
            values.append(data['completada'])
        
        if fields:
            query = f"UPDATE tareas SET {', '.join(fields)} WHERE id = %s"
            values.append(tarea_id)
            cursor.execute(query, values)
            connection.commit()
        
        close_connection(connection, cursor)
        return self.get_by_id(tarea_id)
    
    def delete(self, tarea_id):
        connection = get_db_connection()
        if not connection:
            return False
        
        cursor = connection.cursor()
        cursor.execute("DELETE FROM tareas WHERE id = %s", (tarea_id,))
        connection.commit()
        affected = cursor.rowcount
        close_connection(connection, cursor)
        
        return affected > 0
    
    def asignar_etiqueta(self, tarea_id, etiqueta_id):
        connection = get_db_connection()
        if not connection:
            return False
        
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO tarea_etiqueta (tarea_id, etiqueta_id) VALUES (%s, %s)",
                (tarea_id, etiqueta_id)
            )
            connection.commit()
            success = True
        except:
            success = False
        
        close_connection(connection, cursor)
        return success
    
    def count(self, completada=None):
        connection = get_db_connection()
        if not connection:
            return 0
        
        cursor = connection.cursor()
        query = "SELECT COUNT(*) FROM tareas"
        if completada is not None:
            query += " WHERE completada = %s"
            cursor.execute(query, (completada,))
        else:
            cursor.execute(query)
        
        count = cursor.fetchone()[0]
        close_connection(connection, cursor)
        return count