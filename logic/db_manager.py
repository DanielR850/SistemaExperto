# logic/db_manager.py

import sqlite3
from datetime import datetime

DB_PATH = "data/imc_database.db"

def conectar():
    return sqlite3.connect(DB_PATH)

def crear_tabla():
    """
    Crea la tabla si no existe.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS evaluaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            edad INTEGER,
            peso REAL,
            altura REAL,
            imc REAL,
            clasificacion TEXT,
            fuma INTEGER,
            ejercicio INTEGER,
            antecedentes INTEGER,
            fue_al_medico INTEGER,
            duerme_bien INTEGER,
            come_verduras INTEGER,
            es_sedentario INTEGER,
            duerme_mal INTEGER,
            estresado INTEGER,
            recomendacion TEXT
        )
    """)
    conn.commit()
    conn.close()

def guardar_evaluacion(
    edad, peso, altura, imc, clasificacion,
    fuma, ejercicio, antecedentes, fue_al_medico,
    duerme_bien, come_verduras, es_sedentario, duerme_mal, estresado,
    recomendacion
):
    """
    Guarda una evaluación nueva en la base de datos.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO evaluaciones (
            fecha, edad, peso, altura, imc, clasificacion,
            fuma, ejercicio, antecedentes, fue_al_medico,
            duerme_bien, come_verduras, es_sedentario, duerme_mal, estresado,
            recomendacion
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        edad, peso, altura, imc, clasificacion,
        int(fuma), int(ejercicio), int(antecedentes), int(fue_al_medico),
        int(duerme_bien), int(come_verduras), int(es_sedentario), int(duerme_mal), int(estresado),
        recomendacion
    ))
    conn.commit()
    conn.close()
