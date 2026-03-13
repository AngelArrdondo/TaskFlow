from datetime import datetime

class TareaModel:
    def __init__(self, id=None, titulo=None, descripcion=None, 
                 fecha_limite=None, completada=False, 
                 created_at=None, updated_at=None):
        self.id = id
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha_limite = fecha_limite
        self.completada = completada
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        self.etiquetas = []

class EtiquetaModel:
    def __init__(self, id=None, nombre=None, created_at=None):
        self.id = id
        self.nombre = nombre
        self.created_at = created_at or datetime.now()