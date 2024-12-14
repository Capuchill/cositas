import streamlit as st
from sqlalchemy.orm import  sessionmaker
from datetime import datetime
from conexion import Tarea, engine
import pandas as pd

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

def agregar_tarea(titulo, descripcion=None, estado=False, fecha_creacion=None, fecha_vencimiento=None):
    nueva_tarea = Tarea(
        titulo=titulo, 
        descripcion=descripcion, 
        estado=estado, 
        fecha_creacion=fecha_creacion or datetime.utcnow(), 
        fecha_vencimiento=fecha_vencimiento
    )
    session.add(nueva_tarea)
    session.commit()

def eliminar_tarea(id_tarea):
    tarea = session.query(Tarea).filter(Tarea.id == id_tarea).first()
    if tarea:
        session.delete(tarea)
        session.commit()
    session.close()

def actualizar_tarea(id_tarea, nuevo_titulo=None, nueva_descripcion=None, nuevo_estado=None, nueva_fecha_vencimiento=None):
    tarea = session.query(Tarea).filter(Tarea.id == id_tarea).first()
    if tarea:
        if nuevo_titulo:
            tarea.titulo = nuevo_titulo
        if nueva_descripcion:
            tarea.descripcion = nueva_descripcion
        if nuevo_estado is not None:
            tarea.estado = nuevo_estado
        if nueva_fecha_vencimiento:
            tarea.fecha_vencimiento = nueva_fecha_vencimiento
        session.commit()
    session.close()

st.subheader("nueva tarea")

titulo = st.text_input("Título de la tarea")
descripcion = st.text_area("Descripción de la tarea")

estado = st.selectbox(
    'Elige una opción:',
    [True, False]
)

fecha_vencimiento = st.date_input("fecha de vencimiento")

if st.button('Agregar tarea'):
    if titulo:
        agregar_tarea(titulo, descripcion, estado, fecha_vencimiento)
        st.success('Tarea agregada con exito :)')
    else:
        st.warning('Pendejo le falto el titulo')

st.divider()
st.header("Lista de tareas")

def obtenerTareas():
    tareas = session.query(Tarea).all()
    session.close()
    return tareas

tareas = obtenerTareas()

for tarea in tareas:
    col1,col2,col3 = st.columns([1,1,1])
    with col1: 
        st.write(f"""
                 Título: {tarea.titulo}\n
                 Descripción: {tarea.descripcion}\n
                 Estado: {'Completada' if tarea.estado else 'Pendiente'}\n
                 Fecha de creación: {tarea.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')if tarea.fecha_creacion else 'No establecida'}\n
                 Fecha de vencimiento: {tarea.fecha_vencimiento.strftime('%Y-%m-%d %H:%M:%S') if tarea.fecha_vencimiento else 'No establecida'}
        """)

    with col2: 
        
        if st.button(f'Modificación', key=f'mod_{tarea.id}'):
            st.session_state.editar_id_tarea = tarea.id
            st.session_state.editar_datos_tarea = {
                'titulo': tarea.titulo,
                'descripción': tarea.descripcion,
                'estado': tarea.estado,
                'fecha_vencimiento' : tarea.fecha_vencimiento
            }

    
    with col3:
        if st.button(f'Eliminar', key=f'del_{tarea.id}'):
            eliminar_tarea(tarea.id)
            st.success(f'Tarea eliminada con éxito')