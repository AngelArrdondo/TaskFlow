from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import date, datetime

# Esquemas para Etiqueta
class EtiquetaBase(BaseModel):
    nombre: str = Field(..., max_length=30)

class EtiquetaCreate(EtiquetaBase):
    pass

class Etiqueta(EtiquetaBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Esquemas para Tarea
class TareaBase(BaseModel):
    titulo: str = Field(..., max_length=100)
    descripcion: Optional[str] = Field(None, max_length=300)
    fecha_limite: Optional[date] = None
    completada: bool = False
    
    @validator('fecha_limite')
    def validar_fecha(cls, v):
        if v and v < date.today():
            raise ValueError('La fecha límite no puede ser anterior a hoy')
        return v

class TareaCreate(TareaBase):
    pass

class TareaUpdate(BaseModel):
    titulo: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=300)
    fecha_limite: Optional[date] = None
    completada: Optional[bool] = None

class Tarea(TareaBase):
    id: int
    created_at: datetime
    updated_at: datetime
    etiquetas: List[Etiqueta] = []
    
    class Config:
        from_attributes = True

class TareaConEtiquetas(Tarea):
    pass

# Esquema para asignar etiqueta
class AsignarEtiqueta(BaseModel):
    etiqueta_id: int