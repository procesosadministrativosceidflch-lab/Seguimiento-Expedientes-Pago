from pathlib import Path
import re
from dotenv import load_dotenv
import gspread
import os
import json
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets.readonly"
]

google_credentials = os.getenv("GOOGLE_CREDENTIALS")


if google_credentials and google_credentials.strip().startswith("{"):
    credentials = Credentials.from_service_account_info(
        json.loads(google_credentials),
        scopes=SCOPES
    )
else:
    credentials = Credentials.from_service_account_file(
        "credentials.json",
        scopes=SCOPES
    )

client = gspread.authorize(credentials)

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

URL_HOJA = os.getenv("URL_HOJA")

SPREADSHEET = client.open_by_url(URL_HOJA)

if not URL_HOJA:
    raise ValueError(
        "No se encontró GOOGLE_SHEET_URL en el archivo .env"
    )


def obtener_base_docentes():

    worksheet = SPREADSHEET.worksheet("BASE_DOCENTES")

    return worksheet.get_all_records()


def obtener_hojas_pago():

    worksheets = SPREADSHEET.worksheets()

    hojas_pago = []

    patron = r"^DOC\.\s[A-Z]{3}(\s\d{2})?$"

    for ws in worksheets:

        nombre = ws.title.strip()

        if re.match(
            patron,
            nombre
        ):
            hojas_pago.append(nombre)

    return hojas_pago


def obtener_expedientes(nombre_hoja):

    worksheet = SPREADSHEET.worksheet(nombre_hoja)

    # Leer todo
    datos = worksheet.get_all_values()

    # fila 9 (índice 8)
    encabezados = datos[8]

    # reemplazar encabezados vacíos
    encabezados_limpios = []

    for i, encabezado in enumerate(encabezados):

        encabezado = encabezado.strip()

        if not encabezado:
            encabezado = f"columna_{i}"

        encabezados_limpios.append(
            encabezado
        )

    registros = []

    # desde fila 10 en adelante
    for fila in datos[9:]:

        # completar columnas faltantes
        while len(fila) < len(encabezados_limpios):
            fila.append("")

        registro = dict(
            zip(
                encabezados_limpios,
                fila
            )
        )

        registros.append(
            registro
        )

    return registros