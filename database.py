"""
database.py
Funciones para conectar y trabajar con la base de datos SQLite
donde se guardan las tarjetas de vocabulario.
"""

import sqlite3

NOMBRE_BD = "vocabulario.db"


def conectar():
    """Abre (o crea si no existe) el archivo de base de datos."""
    return sqlite3.connect(NOMBRE_BD)


def crear_tabla():
    """Crea la tabla 'tarjetas' si todavía no existe."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarjetas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            palabra_fr TEXT NOT NULL,
            traduccion_es TEXT NOT NULL,
            fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP,
            veces_repasada INTEGER NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    try:
        cursor.execute("ALTER TABLE tarjetas ADD COLUMN veces_repasada INTEGER NOT NULL DEFAULT 0")
        conn.commit()
    except sqlite3.OperationalError:
        pass
    conn.close()


def guardar_tarjeta(palabra_fr, traduccion_es):
    """Inserta una nueva tarjeta en la base de datos."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tarjetas (palabra_fr, traduccion_es) VALUES (?, ?)",
        (palabra_fr, traduccion_es)
    )
    conn.commit()
    conn.close()

def existe_palabra(palabra_fr):
    """Comprueba si una palabra ya esta guardada (sin distinguir mayusculas/minusculas)."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT 1 FROM tarjetas WHERE LOWER(palabra_fr) = LOWER(?) LIMIT 1",
        (palabra_fr,)
    )
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None

def obtener_todas_las_tarjetas():
    """Devuelve una lista con todas las tarjetas guardadas."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, palabra_fr, traduccion_es FROM tarjetas")
    filas = cursor.fetchall()
    conn.close()
    return filas


def contar_tarjetas():
    """Devuelve el numero total de tarjetas guardadas."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM tarjetas")
    total = cursor.fetchone()[0]
    conn.close()
    return total


def obtener_tarjeta_aleatoria():
    """Devuelve una tarjeta al azar como (id, palabra_fr, traduccion_es), o None si no hay ninguna."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, palabra_fr, traduccion_es, veces_repasada  FROM tarjetas ORDER BY RANDOM() LIMIT 1"
    )
    fila = cursor.fetchone()
    conn.close()
    return fila

def obtener_tarjeta_aleatoria_sin_vistas(ids_vistos):
    """
    Devuelve una tarjeta al azar cuyo id NO este en ids_vistos, o None si
    ya no queda ninguna por ver (se han repasado todas).
    """
    conn = conectar()
    cursor = conn.cursor()
 
    if ids_vistos:
        interrogantes = ",".join("?" for _ in ids_vistos)
        cursor.execute(
            f"SELECT id, palabra_fr, traduccion_es, veces_repasada  FROM tarjetas "
            f"WHERE id NOT IN ({interrogantes}) ORDER BY RANDOM() LIMIT 1",
            tuple(ids_vistos)
        )
    else:
        cursor.execute(
            "SELECT id, palabra_fr, traduccion_es, veces_repasada FROM tarjetas ORDER BY RANDOM() LIMIT 1"
        )
 
    fila = cursor.fetchone()
    conn.close()
    return fila

def incrementar_veces_repasada(id_tarjeta):
    """Suma 1 al contador de veces que se ha repasado esa tarjeta, y devuelve el nuevo valor."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tarjetas SET veces_repasada = veces_repasada + 1 WHERE id = ?",
        (id_tarjeta,)
    )
    conn.commit()
    cursor.execute("SELECT veces_repasada FROM tarjetas WHERE id = ?", (id_tarjeta,))
    nuevo_valor = cursor.fetchone()[0]
    conn.close()
    return nuevo_valor


def eliminar_tarjeta(id_tarjeta):
    """Borra una tarjeta de la base de datos por su id."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tarjetas WHERE id = ?", (id_tarjeta,))
    conn.commit()
    conn.close()