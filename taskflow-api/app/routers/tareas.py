from fastapi import APIRouter, Query, Path, status
from typing import Optional
from app.controllers.tarea_controller import TareaController
from app.schemas import TareaCreate, TareaUpdate, AsignarEtiqueta

router = APIRouter(prefix="/api/v1/tareas", tags=["Tareas"])
controller = TareaController()

@router.get("/")
async def get_tareas(
    completada: Optional[bool] = Query(None, description="Filtrar por estado"),
    page: int = Query(1, ge=1, description="Número de página"),
    limit: int = Query(10, ge=1, le=100, description="Registros por página")
):
    return controller.get_all(completada, page, limit)

@router.get("/{tarea_id}")
async def get_tarea(tarea_id: int = Path(..., ge=1)):
    return controller.get_by_id(tarea_id)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_tarea(tarea_data: TareaCreate):
    return controller.create(tarea_data)

@router.put("/{tarea_id}")
async def update_tarea(
    tarea_data: TareaUpdate,
    tarea_id: int = Path(..., ge=1)
):
    return controller.update(tarea_id, tarea_data)

@router.patch("/{tarea_id}/completar")
async def marcar_completada(tarea_id: int = Path(..., ge=1)):
    return controller.marcar_completada(tarea_id)

@router.delete("/{tarea_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tarea(tarea_id: int = Path(..., ge=1)):
    return controller.delete(tarea_id)

@router.post("/{tarea_id}/etiquetas")
async def asignar_etiqueta(
    data: AsignarEtiqueta,
    tarea_id: int = Path(..., ge=1)
):
    return controller.asignar_etiqueta(tarea_id, data)