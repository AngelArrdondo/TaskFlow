from app.repositories.etiqueta_repository import EtiquetaRepository

class EtiquetaService:
    
    def __init__(self):
        self.etiqueta_repo = EtiquetaRepository()
    
    def get_all_etiquetas(self):
        return self.etiqueta_repo.get_all()
    
    def get_etiqueta_by_id(self, etiqueta_id):
        return self.etiqueta_repo.get_by_id(etiqueta_id)
    
    def create_etiqueta(self, etiqueta_data):
        # Validar que no exista una con el mismo nombre
        existente = self.etiqueta_repo.get_by_nombre(etiqueta_data.nombre)
        if existente:
            raise ValueError("Ya existe una etiqueta con ese nombre")
        
        if not etiqueta_data.nombre or len(etiqueta_data.nombre.strip()) == 0:
            raise ValueError("El nombre de la etiqueta no puede estar vacío")
        
        return self.etiqueta_repo.create(etiqueta_data)