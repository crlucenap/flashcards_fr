![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-F8D341)
![SQLite](https://img.shields.io/badge/DB-SQLite-003B57?logo=sqlite&logoColor=white)
![Status](https://img.shields.io/badge/status-en%20desarrollo-yellow)

# Quickcards

App de escritorio para aprender vocabulario en francés. Escribes una palabra
mientras estudias, se traduce sola al español y se guarda como tarjeta; luego
la repasas en modo flashcard, sin que se te repita ninguna palabra hasta que
las hayas visto todas.

<!-- 🎥 Aquí va el GIF o enlace al vídeo de demo -->
<!-- ![demo](docs/demo.gif) -->

## Tecnologías usadas

- **Python 3.11**
- **CustomTkinter** — interfaz gráfica de escritorio
- **SQLite** (`sqlite3`, incluido en Python) — persistencia de las tarjetas
- **MyMemory API** — traducción automática francés → español
- **wordfreq** — comprobación de que la palabra introducida es realmente
  francesa antes de traducir (evita traducciones sin sentido si escribes
  en otro idioma por error)

## Funcionalidades

- ✅ Traducción automática francés → español al guardar una palabra
- ✅ Detección de palabras que no son francesas o mal escritas, antes de
  gastar una llamada a la API
- ✅ Aviso de fiabilidad baja en la traducción (por erratas dentro del francés)
- ✅ No se guardan palabras duplicadas 
- ✅ Modo Repaso con tarjetas aleatorias que no se repiten en la misma sesión
- ✅ Botón de reinicio del repaso cuando has visto todas las tarjetas
- ✅ Contador de cuántas veces se ha repasado cada palabra
- ✅ Borrado de tarjetas individuales desde la propia tarjeta de repaso
- ✅ Contador total de tarjetas guardadas

## Qué puede hacer el usuario

1. **Modo Estudio**: escribe una palabra en francés y pulsa "Traducir y
   guardar" (o Enter). La app la traduce y la añade a tu mazo de vocabulario.
2. **Modo Repaso**: pulsa la tarjeta para voltearla y ver la traducción.
   Usa "Siguiente tarjeta" para pasar a la siguiente palabra sin repetir
   ninguna hasta agotar el mazo, y "Volver a empezar" para repasarlo todo
   de nuevo.
3. **Borrar una tarjeta**: pulsa el icono 🗑 sobre la tarjeta que estás
   repasando para eliminarla del mazo.

## Atajos de teclado

| Atajo   | Acción                                    |
|---------|--------------------------------------------|
| `Enter` | Traduce y guarda la palabra (en Estudio)   |


## Cómo ejecutarlo

```bash
git clone https://github.com/tu-usuario/quickcards.git
cd quickcards
pip install -r requirements.txt
python main.py
```

Requiere Python 3.10+ y conexión a internet (para la traducción automática).

## Vídeo / demo

<!-- Sustituye esto por un enlace a un vídeo corto (Loom, YouTube sin listar,
     o un GIF subido a la carpeta docs/) enseñando la app en uso:
     escribir una palabra, ver que se traduce y guarda, y repasar tarjetas. -->

🎥 *(pendiente de grabar)*
