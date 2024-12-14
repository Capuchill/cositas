from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

usuario = 'root'
contrasena = 'asd123'
host = 'localhost'
base_datos = 'cositas'
url_conexion = f'mysql+pymysql://{usuario}:{contrasena}@{host}/{base_datos}'
Base = declarative_base()
engine = create_engine(url_conexion)

class Tarea(Base):
    __tablename__ = 'tareas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(100), nullable=False, unique=True)
    descripcion = Column(String(255), nullable=True)
    estado = Column(Boolean, nullable=False, default=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_vencimiento = Column(DateTime, nullable=True)

def crear_tablas():

    #crear_base_datos(engine)
    Base.metadata.create_all(engine)
    print("Tablas creadas con éxito.")

if __name__ == "__main__":
    crear_tablas()