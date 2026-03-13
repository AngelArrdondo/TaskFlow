from fastapi import HTTPException, status
from app.services.etiqueta_service import EtiquetaService
from app.schemas import EtiquetaCreate
from datetime import datetime

class EtiquetaController:
    
    def __init__(self):
        self.service = EtiquetaService()
    
    def get_all(self):
        try:
            etiquetas = self.service.get_all_etiquetas()
            
            etiquetas_dict = []
            for etiqueta in etiquetas:
                etiqueta_dict = {
                    "id": etiqueta.id,
                    "nombre": etiqueta.nombre,
                    "created_at": etiqueta.created_at.isoformat() if etiqueta.created_at else None
                }
                etiquetas_dict.append(etiqueta_dict)
            
            return {
                "status": "success",
                "timestamp": datetime.utcnow().isoformat(),
                "message": "Lista de etiquetas",
                "data": etiquetas_dict
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
    
    def create(self, etiqueta_data: EtiquetaCreate):
        try:
            etiqueta = self.service.create_etiqueta(etiqueta_data)
            return {
                "status": "success",
                "timestamp": datetime.utcnow().isoformat(),
                "message": "Etiqueta creada correctamente",
                "data": {
                    "id": etiqueta.id,
                    "nombre": etiqueta.nombre
                }
            }
        except ValueError as e:
            if "Ya existe" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=str(e)
                )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )