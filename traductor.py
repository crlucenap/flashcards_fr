"""
traductor.py
Funcion que llama a la API publica y gratuita de MyMemory
para traducir una palabra de frances a espanol.
No requiere API key ni registro.
"""

import requests
from wordfreq import zipf_frequency

URL_API = "https://api.mymemory.translated.net/get"

UMBRAL_FIABILIDAD = 0.85

def _parece_frances(palabra):
    """
    Comprueba, usando frecuencias de uso reales, si una palabra
    parece frances antes de gastar una llamada a la API.

    MyMemory por si solo NO detecta el idioma de lo que escribes (el
    langpair "fr|es" solo le dice en que diccionario buscar), asi que
    si escribes una palabra en español o en otro idioma, puede devolver
    una traduccion sin sentido con una fiabilidad alta. Por eso este
    chequeo se hace ANTES de llamar a la API.
    """
    frecuencia_fr = zipf_frequency(palabra, "fr")
    frecuencia_es = zipf_frequency(palabra, "es")

    if frecuencia_fr == 0:
        # No aparece en absoluto como palabra francesa conocida
        return False

    if frecuencia_es > frecuencia_fr:
        # Es mas comun en espanol que en frances -> probablemente
        # la escribiste ya en espanol por error
        return False

    return True


def traducir(palabra_fr):
    """
    Traduce una palabra de frances a espanol usando MyMemory.
    Devuelve una tupla (traduccion, fiable):
    - traduccion: el texto traducido al espanol (o un mensaje de aviso
      si no se ha podido traducir con garantias).
    - fiable: True si la palabra parece frances de verdad Y MyMemory
      encontro una traduccion de calidad alta; False en caso contrario.
    """
    palabra_fr = palabra_fr.strip()

    if not palabra_fr:
        return "", True

    if not _parece_frances(palabra_fr):
        return "", False

    parametros = {
        "q": palabra_fr,
        "langpair": "fr|es"
    }

    try:
        respuesta = requests.get(URL_API, params=parametros, timeout=10)
        respuesta.raise_for_status()
        resultado = respuesta.json()

        traduccion = resultado["responseData"]["translatedText"]
        fiabilidad = float(resultado["responseData"].get("match", 1.0))

        return traduccion, fiabilidad >= UMBRAL_FIABILIDAD

    except (requests.exceptions.RequestException, KeyError, ValueError) as error:
        return f"[Error de traduccion: {error}]", False