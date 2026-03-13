from fastapi import HTTPException, status
from app.services.tarea_service import TareaService
from app.schemas import TareaCreate, TareaUpdate, AsignarEtiqueta
from datetime import datetime

class TareaController:
    
    def __init__(self):
        self.service = TareaService()
    
    def get_all(self, completada=None, page=1, limit=10):
        try:
            result = self.service.get_all_tareas(completada, page, limit)
            
            # Convertir objetos a diccionarios
            tareas_dict = []
            for tarea in result["tareas"]:
                tarea_dict = {
                    "id": tarea.id,
                    "titulo": tarea.titulo,
                    "descripcion": tarea.descripcion,
                    "fecha_limite": str(tarea.fecha_limite) if tarea.fecha_limite else None,
                    "completada": tarea.completada,
                    "created_at": tarea.created_at.isoformat() if tarea.created_at else None,
                    "updated_at": tarea.updated_at.isoformat() if tarea.updated_at else None,
                    "etiquetas": tarea.etiquetas
                }
                tareas_dict.append(tarea_dict)
            
            return {
                "status": "success",
                "timestamp": datetime.utcnow().isoformat(),
                "message": "Lista de tareas",
                "data": tareas_dict,
                "meta": {
                    "page": result["page"],
                    "limit": result["limit"],
                    "total": result["total"],
                    "pages": result["pages"]
                }
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
    
    def get_by_id(self, tarea_id):
        try:
            tarea = self.service.get_tarea_by_id(tarea_id)
            if not tarea:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Tarea no encontrada"
                )
            
            return {
                "status": "success",
                "timestamp": datetime.utcnow().isoformat(),
                "message": "Tarea obtenida correctamente",
                "data": {
                    "id": tarea.id,
                    "titulo": tarea.titulo,
                    "descripcion": tarea.descripcion,
                    "fecha_limite": str(tarea.fecha_limite) if tarea.fecha_limite else None,
                    "completada": tarea.completada,
                    "created_at": tarea.created_at.isoformat() if tarea.created_at else None,
                    "updated_at": tarea.updated_at.isoformat() if tarea.updated_at else None,
                    "etiquetas": tarea.etiquetas
                }
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
    
    def create(self, tarea_data: TareaCreate):
        try:
            tarea = self.service.create_tarea(tarea_data)
            return {
                "status": "success",
                "timestamp": datetime.utcnow().isoformat(),
                "message": "Tarea creada correctamente",
                "data": {
                    "id": tarea.id,
                    "titulo": tarea.titulo,
                    "descripcion": tarea.descripcion,
                    "fecha_limite": str(tarea.fecha_limite) if tarea.fecha_limite else None,
                    "completada": tarea.completada
                }
            }
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
    
    def update(self, tarea_id: int, tarea_data: TareaUpdate):
        try:
            tarea = self.service.update_tarea(tarea_id, tarea_data)
            if not tarea:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Tarea no encontrada"
                )
            
            return {
                "status": "success",
                "timestamp": datetime.utcnow().isoformat(),
                "message": "Tarea actualizada correctamente",
                "data": {
                    "id": tarea.id,
                    "titulo": tarea.titulo,
                    "descripcion": tarea.descripcion,
                    "fecha_limite": str(tarea.fecha_limite) if tarea.fecha_limite else None,
                    "completada": tarea.completada
                }
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
    
    def delete(self, tarea_id: int):
        try:
            deleted = self.service.delete_tarea(tarea_id)
            if not deleted:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Tarea no encontrada"
                )
            
            return None  # 204 No Content
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
    
    def marcar_completada(self, tarea_id: int):
        try:
            tarea = self.service.marcar_completada(tarea_id)
            if not tarea:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Tarea no encontrada"
                )
            
            return {
                "status": "success",
                "timestamp": datetime.utcnow().isoformat(),
                "message": "Tarea actualizada correctamente",
                "data": {
                    "id": tarea.id,
                    "titulo": tarea.titulo,
                    "descripcion": tarea.descripcion,
                    "fecha_limite": str(tarea.fecha_limite) if tarea.fecha_limite else None,
                    "completada": tarea.completada,
                    "etiquetas": tarea.etiquetas
                }
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
    
    def asignar_etiqueta(self, tarea_id: int, data: AsignarEtiqueta):
        try:
            tarea, error = self.service.asignar_etiqueta(tarea_id, data.etiqueta_id)
            if error:
                if "no encontrada" in error:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=error
                    )
                else:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=error
                    )
            
            return {
                "status": "success",
                "timestamp": datetime.utcnow().isoformat(),
                "message": "Etiqueta asignada correctamente",
                "data": {
                    "id": tarea.id,
                    "titulo": tarea.titulo,
                    "descripcion": tarea.descripcion,
                    "fecha_limite": str(tarea.fecha_limite) if tarea.fecha_limite else None,
                    "completada": tarea.completada,
                    "etiquetas": tarea.etiquetas
                }
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )