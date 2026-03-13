from app.repositories.tarea_repository import TareaRepository
from app.repositories.etiqueta_repository import EtiquetaRepository
from datetime import date

class TareaService:
    
    def __init__(self):
        self.tarea_repo = TareaRepository()
        self.etiqueta_repo = EtiquetaRepository()
    
    def get_all_tareas(self, completada=None, page=1, limit=10):
        tareas = self.tarea_repo.get_all(completada, page, limit)
        total = self.tarea_repo.count(completada)
        
        return {
            "tareas": tareas,
            "total": total,
            "page": page,
            "limit": limit,
            "pages": (total + limit - 1) // limit
        }
    
    def get_tarea_by_id(self, tarea_id):
        return self.tarea_repo.get_by_id(tarea_id)
    
    def create_tarea(self, tarea_data):
        # Validaciones adicionales
        if not tarea_data.titulo or len(tarea_data.titulo.strip()) == 0:
            raise ValueError("El título no puede estar vacío")
        
        return self.tarea_repo.create(tarea_data)
    
    def update_tarea(self, tarea_id, tarea_data):
        tarea = self.tarea_repo.get_by_id(tarea_id)
        if not tarea:
            return None
        
        return self.tarea_repo.update(tarea_id, tarea_data)
    
    def patch_tarea(self, tarea_id, data):
        tarea = self.tarea_repo.get_by_id(tarea_id)
        if not tarea:
            return None
        
        return self.tarea_repo.patch(tarea_id, data)
    
    def delete_tarea(self, tarea_id):
        tarea = self.tarea_repo.get_by_id(tarea_id)
        if not tarea:
            return False
        
        return self.tarea_repo.delete(tarea_id)
    
    def marcar_completada(self, tarea_id):
        tarea = self.tarea_repo.get_by_id(tarea_id)
        if not tarea:
            return None
        
        return self.tarea_repo.patch(tarea_id, {"completada": True})
    
    def asignar_etiqueta(self, tarea_id, etiqueta_id):
        tarea = self.tarea_repo.get_by_id(tarea_id)
        if not tarea:
            return None, "Tarea no encontrada"
        
        etiqueta = self.etiqueta_repo.get_by_id(etiqueta_id)
        if not etiqueta:
            return None, "Etiqueta no encontrada"
        
        success = self.tarea_repo.asignar_etiqueta(tarea_id, etiqueta_id)
        if success:
            return self.tarea_repo.get_by_id(tarea_id), None
        else:
            return None, "Error al asignar etiqueta (posiblemente ya estaba asignada)"