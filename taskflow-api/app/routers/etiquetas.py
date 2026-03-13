from fastapi import APIRouter, status
from app.controllers.etiqueta_controller import EtiquetaController
from app.schemas import EtiquetaCreate

router = APIRouter(prefix="/api/v1/etiquetas", tags=["Etiquetas"])
controller = EtiquetaController()

@router.get("/")
async def get_etiquetas():
    return controller.get_all()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_etiqueta(etiqueta_data: EtiquetaCreate):
    return controller.create(etiqueta_data)