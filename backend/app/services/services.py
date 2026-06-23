from app.models import Docente
from datetime import timedelta


def obtener_estado(exp):

    if exp.fecha_pago:
        return 6

    elif exp.derivado:
        return 5

    elif exp.rxh:
        return 4

    elif exp.envio_correo:
        return 3

    elif exp.os:
        return 2

    elif exp.hr:
        return 1

    elif exp.enviado:
        return 0

    return -1


def construir_timeline(exp):

    timeline=[]

    pasos=[

        ("Solicitud enviada", exp.enviado),

        ("Hoja de Requerimiento firmada", exp.hr),

        ("Orden de servicio remitida a CEID", exp.os),

        ("Puede emitir RXH", exp.envio_correo),

        ("RXH emitido", exp.rxh),

        ("Expediente enviado a unidad central", exp.derivado),

        ("Pago realizado", exp.fecha_pago)

    ]

    for nombre, fecha in pasos:

        if fecha:

            timeline.append({

                "etapa":nombre,

                "fecha":fecha.strftime(
                    "%d/%m/%Y"
                )

            })

    return timeline


def calcular_pago_estimado(exp):

    if exp.fecha_pago:
        return None

    if not exp.derivado:
        return None

    fecha_estimada = exp.derivado + timedelta(days=7)

    return fecha_estimada.strftime("%d/%m/%Y")