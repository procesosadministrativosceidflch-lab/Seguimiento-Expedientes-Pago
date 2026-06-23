from sqlalchemy.orm import Session
from app.models import Expediente, Docente
from datetime import datetime

def guardar_docentes(db: Session, docentes):

    rucs_procesados = set()

    for docente in docentes:

        nombre = str(docente.get("DOCENTE", "")).strip()

        ruc = str(docente.get("RUC", "")).strip()

        if not ruc:
            continue

        if ruc in rucs_procesados:
            continue

        rucs_procesados.add(ruc)

        existe = (db.query(Docente).filter(Docente.ruc == ruc).first())

        if existe:
            existe.nombre = nombre

        else:

            nuevo = Docente(nombre=nombre, ruc=ruc)
            db.add(nuevo)

    db.commit()

def convertir_fecha(valor):

    if not valor:
        return None

    try:
        return datetime.strptime(valor, "%d/%m/%Y").date()

    except:
        return None


def guardar_expedientes(db, expedientes, periodo):

    for exp in expedientes:

        numero = str(exp.get("Numero de expediente", "")).strip()

        docente_nombre = str(exp.get("Docente", "")).strip()

        if not numero:
            continue

        docente = (db.query(Docente).filter(Docente.nombre == docente_nombre).first())

        if not docente:
            continue

        expediente = (db.query(Expediente).filter(Expediente.numero_expediente == numero).first())

        if not expediente:

            expediente = Expediente(numero_expediente=numero, docente_id=docente.id)
            db.add(expediente)

        expediente.periodo = periodo

        expediente.observacion = exp.get("OBSERVACION")

        expediente.enviado = convertir_fecha(exp.get("ENVIADO"))

        expediente.hr = convertir_fecha(exp.get("HR"))

        expediente.os = convertir_fecha(exp.get("OS"))

        expediente.envio_correo = convertir_fecha(exp.get("ENVÍO CORREO"))

        expediente.rxh = convertir_fecha(exp.get("RXH"))

        expediente.derivado = convertir_fecha(exp.get("DERIVADO"))

        expediente.fecha_pago = convertir_fecha(exp.get("FECHA DE PAGO"))

        expediente.docente_id = docente.id

    db.commit()