from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, get_db
from app.models import Base, SyncLog
from app.models import Docente
from app.services.sheets_service import (obtener_base_docentes, obtener_hojas_pago)
from app.crud import (guardar_docentes)

from app.services.services import (
    calcular_pago_estimado,
    obtener_estado,
    construir_timeline
)

from app.services.sync_service import (
    ejecutar_sincronizacion
)


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(

    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)


@app.get("/")
def inicio():

    return {
        "mensaje":"API funcionando"
    }


@app.get("/sincronizar-docentes")
def sincronizar_docentes(
    db: Session = Depends(get_db)
):

    datos = obtener_base_docentes()

    guardar_docentes(
        db,
        datos
    )

    return {
        "mensaje":"Docentes sincronizados"
    }

@app.get("/sincronizar-expedientes")
def sincronizar(db: Session = Depends(get_db)):

    resultado = ejecutar_sincronizacion(db)

    return {
        "mensaje":
        "Expedientes sincronizados",
        **resultado
    }

@app.get("/periodos")
def obtener_periodos():

    hojas = obtener_hojas_pago()

    meses = {
        "ENE": "Enero",
        "FEB": "Febrero",
        "MAR": "Marzo",
        "ABR": "Abril",
        "MAY": "Mayo",
        "JUN": "Junio",
        "JUL": "Julio",
        "AGO": "Agosto",
        "SEP": "Septiembre",
        "OCT": "Octubre",
        "NOV": "Noviembre",
        "DIC": "Diciembre"
    }

    resultado = []

    for hoja in hojas:

        partes = hoja.split()

        # DOC. NOV 25
        mes = partes[1]
        anio = partes[2] if len(partes) > 2 else ""

        label = meses.get(
            mes,
            mes
        )

        if anio:
            label += f" 20{anio}"

        resultado.append({
            "label": label,
            "value": hoja
        })

    return resultado

@app.get("/ultima-sincronizacion")
def ultima_sincronizacion(
    db: Session = Depends(get_db)
):

    ultimo = (
        db.query(SyncLog)
        .order_by(
            SyncLog.fecha_inicio.desc()
        )
        .first()
    )

    return ultimo

@app.get("/health")
def health():

    return {
        "status": "ok"
    }

@app.get("/consulta")
def consultar_pago(
    ruc:str,
    periodo:str,
    db: Session = Depends(get_db)
):

    docente = db.query(
        Docente
    ).filter(
        Docente.ruc == ruc
    ).first()

    if not docente:
        raise HTTPException(
            status_code=404,
            detail="RUC no encontrado"
        )

    resultados=[]

    for exp in docente.expedientes:

        if exp.periodo != periodo:
            continue

        resultados.append({

            "numero_expediente":
            exp.numero_expediente,

            "estado_actual":
            obtener_estado(exp),

            "linea_tiempo":
            construir_timeline(exp),

            "fecha_estimada_pago":
            calcular_pago_estimado(exp),

        })

    return {

        "docente":
        docente.nombre,

        "expedientes":
        resultados

    }