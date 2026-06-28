from sqlalchemy import Column, DateTime, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.database import Base

class Docente(Base):
    __tablename__ = "docentes"

    id = Column(Integer, primary_key=True, index=True)

    nombre = Column(String, nullable=False)
    ruc = Column(String, unique=True, nullable=False)

    expedientes = relationship(
        "Expediente",
        back_populates="docente"
    )


class Expediente(Base):

    __tablename__ = "expedientes"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    numero_expediente = Column(
        String,
        unique=True,
        nullable=False
    )

    periodo = Column(
        String,
        nullable=False
    )

    observacion = Column(Text)

    enviado = Column(Date)

    hr = Column(Date)

    os = Column(Date)

    envio_correo = Column(Date)

    rxh = Column(Date)

    derivado = Column(Date)

    fecha_pago = Column(Date)

    docente_id = Column(
        Integer,
        ForeignKey("docentes.id")
    )

    docente = relationship(
        "Docente",
        back_populates="expedientes"
    )

class SyncLog(Base):

    __tablename__ = "sync_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    fecha_inicio = Column(
        DateTime(timezone=True),
        nullable=False
    )

    fecha_fin = Column(
        DateTime(timezone=True),
        nullable=False
    )

    cantidad_docentes = Column(
        Integer,
        nullable=False,
        default=0
    )

    hojas = Column(
        Integer,
        nullable=False
    )

    registros = Column(
        Integer,
        nullable=False
    )

    estado = Column(
        String,
        nullable=False
    )

    error = Column(
        Text,
        nullable=True
    )