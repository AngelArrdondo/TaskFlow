from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.routers import tareas, etiquetas
from datetime import datetime


app = FastAPI(
    title="TaskFlow API",
    description="API para gestión de tareas personales",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # URL de React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(tareas.router)
app.include_router(etiquetas.router)

# Manejador de errores personalizado
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "timestamp": datetime.utcnow().isoformat(),
            "message": exc.detail,
            "error_code": "HTTP_ERROR"
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={
            "status": "error",
            "timestamp": datetime.utcnow().isoformat(),
            "message": "Error de validación",
            "error_code": "VALIDATION_ERROR",
            "details": str(exc)
        }
    )

@app.get("/")
async def root():
    return {
        "message": "TaskFlow API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }