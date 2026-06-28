from app.services.sheets_service import (obtener_base_docentes, obtener_hojas_pago, obtener_expedientes)
from app.crud import (guardar_docentes, guardar_expedientes)
from app.models import SyncLog
from datetime import datetime
from zoneinfo import ZoneInfo

LIMA = ZoneInfo("America/Lima")


def ejecutar_sincronizacion(db):

    inicio = datetime.now(LIMA)

    try:

        docentes = obtener_base_docentes()

        guardar_docentes(db, docentes)

        hojas = obtener_hojas_pago()

        total = 0

        for hoja in hojas:

            datos = obtener_expedientes(hoja)

            guardar_expedientes(db, datos, hoja)

            total += len(datos)

        log = SyncLog(
            fecha_inicio=inicio,
            fecha_fin=datetime.now(LIMA),
            cantidad_docentes = len(docentes),
            hojas=len(hojas),
            registros=total,
            estado="OK",
            error=None
        )

        db.add(log)

        db.commit()

        return {
            "Docentes": len(docentes),

            "hojas": len(hojas),

            "registros": total

        }

    except Exception as e:

        db.rollback()

        log = SyncLog(

            fecha_inicio=inicio,

            fecha_fin=datetime.now(),

            hojas=0,

            registros=0,

            estado="ERROR",

            error=str(e)

        )

        db.add(log)

        db.commit()

        raise