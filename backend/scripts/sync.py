import sys
from app.database import SessionLocal
from app.services.sync_service import (
    ejecutar_sincronizacion
)


def main():

    db = SessionLocal()

    try:

        resultado = ejecutar_sincronizacion(
            db
        )

        print(
            f"Sincronización exitosa: "
            f"{resultado['registros']} registros "
            f"en {resultado['hojas']} hojas"
        )
        sys.exit(0)

    except Exception as e:

        print(
            f"Error durante la sincronización: {e}"
        )
        sys.exit(1)

        raise

    finally:

        db.close()


if __name__ == "__main__":

    main()