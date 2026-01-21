from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr, field_validator, ValidationError
from typing import Optional, List
from datetime import date
import re

app = FastAPI(title="Embajada")

# Servir archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Motor de plantillas
templates = Jinja2Templates(directory="app/templates")

@app.get("/ping")
def pingpong():
    return {"ping": "pong"}

@app.get("/", response_class=HTMLResponse)
def get_index(request: Request):
    return templates.TemplateResponse(
        "pages/index.html",
        {
            "request": request
        }
    )

from app.database import (
    fetch_all_residentes
)

class ResidenteDB(BaseModel):
    id: int
    nombre: str
    apellido: str
    fecha_nacimiento: date
    pasaporte: str
    email: str
    telefono: str
    direccion: str
    ocupacion: str
    estado_civil: str

# Modelo para crear cliente (sin ID)
class ResidenteCreate(ResidenteDB):
    pass


# Modelo para actualizar cliente (sin ID)
class ResidenteUpdate(ResidenteDB):
    pass


# Modelo completo de Cliente (con ID y validaciones)
class Residente(ResidenteDB):
    id: int

def map_rows_to_residente(rows: List[dict]) -> List[ResidenteDB]:
    """
    Convierte las filas del SELECT * FROM residentes (dict) 
    en objetos ResidenteDB (sin validaciones estrictas para datos existentes).
    """
    return [
        ResidenteDB(
            id=row["id"],
            nombre=row["nombre"],
            apellido=row["apellido"],
            fecha_nacimiento=row["fecha_nacimiento"],
            pasaporte=row["pasaporte"],
            email=row["email"],
            telefono=row.get("telefono"),
            direccion=row.get("direccion"),
            ocupacion=row.get("ocupacion"),
            estado_civil=row.get("estado_civil")
        )
        for row in rows
    ]

@app.get("/", response_class=HTMLResponse)
def get_index(request: Request):
    # 1️⃣ Obtenemos los datos desde MySQL
    rows = fetch_all_residentes()

    # 2️⃣ Convertimos cada fila a Residente (valida estructura)
    residentes = map_rows_to_residentes(rows)

    # 3️⃣ Enviamos a la plantilla
    return templates.TemplateResponse(
        "pages/index.html",
        {
            "request": request,
            "residentes": residentes
        }
    )