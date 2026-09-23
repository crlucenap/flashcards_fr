import customtkinter as ctk
from tkinter import messagebox

import database
import traductor

# ---------- PALETA DE COLORES DEL DISENO ----------
COLOR_FONDO = "#FFFFFF"        
COLOR_AMARILLO = "#F8D341"     # amarillo de botones/acentos
COLOR_AMARILLO_CLARO = "#FBEEB0"  # fondo de la caja de resultado traducido
COLOR_AZUL_CLARO = "#DCEAFB"   # fondo de la tarjeta de repaso
COLOR_NEGRO = "#171717"        # bordes y texto principal
COLOR_GRIS = "#8A8A8A"         # texto secundario
COLOR_VERDE = "#1C5E28"        # texto de traduccion correcta
COLOR_BLANCO = "#FFFFFF"
COLOR_NARANJA_CLARO = "#FED498"   
COLOR_NARANJA_OSCURO = "#D6590A"

FUENTE_TITULO = ("Arial", 20, "bold")
FUENTE_NORMAL = ("Arial", 14)
FUENTE_NEGRITA = ("Arial", 14, "bold")
FUENTE_PEQUENA = ("Arial", 12)
FUENTE_GRANDE_NEGRITA = ("Arial", 26, "bold")

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class AppFlashcards:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Quickcards!")
        self.raiz.geometry("460x700")
        self.raiz.configure(fg_color=COLOR_FONDO)

        database.crear_tabla()

        # Estado de la tarjeta que se esta repasando ahora mismo
        self.id_actual = None
        self.palabra_actual = None
        self.traduccion_actual = None
        self.mostrando_traduccion = False

        # Ids de las tarjetas ya vistas en la sesion de repaso actual,
        # para no repetir palabra hasta que se hayan visto todas
        self.ids_vistos = set()
        self.sesion_repaso_iniciada = False

        self._construir_cabecera()
        self._construir_barra_pestanas()

        # Contenedor donde se muestra el contenido de la pestana activa
        self.contenedor = ctk.CTkFrame(self.raiz, fg_color=COLOR_FONDO)
        self.contenedor.pack(fill="both", expand=True, padx=20, pady=(10, 0))

        self.frame_estudio = ctk.CTkFrame(self.contenedor, fg_color=COLOR_FONDO)
        self.frame_repaso = ctk.CTkFrame(self.contenedor, fg_color=COLOR_FONDO)

        self._construir_modo_estudio()
        self._construir_modo_repaso()

        self._mostrar_pestana("estudio")

    # ---------- CABECERA ("F" + Quickcards!) ----------

    def _construir_cabecera(self):
        cabecera = ctk.CTkFrame(self.raiz, fg_color=COLOR_FONDO)
        cabecera.pack(fill="x", padx=20, pady=(20, 15))

        logo = ctk.CTkFrame(
            cabecera, width=40, height=40, corner_radius=10,
            fg_color=COLOR_AMARILLO, border_width=2, border_color=COLOR_NEGRO
        )
        logo.pack(side="left")
        logo.pack_propagate(False)
        ctk.CTkLabel(
            logo, text="F", font=("Arial", 16, "bold"), text_color=COLOR_NEGRO
        ).pack(expand=True)

        ctk.CTkLabel(
            cabecera, text="Quickcards!", font=FUENTE_TITULO, text_color=COLOR_NEGRO
        ).pack(side="left", padx=10)

        ctk.CTkLabel(
            cabecera, text="✨", font=("Arial", 16), text_color=COLOR_AMARILLO
        ).pack(side="right")

    # ---------- BARRA DE PESTANAS (Estudio / Repaso) ----------

    def _construir_barra_pestanas(self):
        barra = ctk.CTkFrame(self.raiz, fg_color=COLOR_FONDO)
        barra.pack(fill="x", padx=20)

        self.boton_tab_estudio = ctk.CTkButton(
            barra, text="Estudio", font=FUENTE_NEGRITA, corner_radius=12,
            border_width=3, border_color=COLOR_NEGRO, height=40,
            command=lambda: self._mostrar_pestana("estudio")
        )
        self.boton_tab_estudio.pack(side="left", expand=True, fill="x", padx=(0, 6))

        self.boton_tab_repaso = ctk.CTkButton(
            barra, text="Repaso", font=FUENTE_NEGRITA, corner_radius=12,
            border_width=3, border_color=COLOR_NEGRO, height=40,
            command=lambda: self._mostrar_pestana("repaso")
        )
        self.boton_tab_repaso.pack(side="left", expand=True, fill="x", padx=(6, 0))

    def _mostrar_pestana(self, nombre):
        # Estilo del boton activo (amarillo) vs inactivo (blanco)
        if nombre == "estudio":
            self.boton_tab_estudio.configure(fg_color=COLOR_AMARILLO, text_color=COLOR_NEGRO, hover_color=COLOR_AMARILLO)
            self.boton_tab_repaso.configure(fg_color=COLOR_BLANCO, text_color=COLOR_NEGRO, hover_color=COLOR_BLANCO)
            self.frame_repaso.pack_forget()
            self.frame_estudio.pack(fill="both", expand=True)
        else:
            self.boton_tab_repaso.configure(fg_color=COLOR_AMARILLO, text_color=COLOR_NEGRO, hover_color=COLOR_AMARILLO)
            self.boton_tab_estudio.configure(fg_color=COLOR_BLANCO, text_color=COLOR_NEGRO, hover_color=COLOR_BLANCO)
            self.frame_estudio.pack_forget()
            self.frame_repaso.pack(fill="both", expand=True)
            # Solo arrancamos una sesion de repaso nueva la primera vez que
            # se entra a esta pestana; si vuelves de Estudio, se conserva
            # el progreso (las palabras ya vistas siguen sin repetirse).
            if not self.sesion_repaso_iniciada:
                self.sesion_repaso_iniciada = True
                self._nueva_tarjeta_aleatoria()

        self._actualizar_contadores()

    # ---------- MODO ESTUDIO ----------

    def _construir_modo_estudio(self):
        frame = self.frame_estudio

        caja = ctk.CTkFrame(
            frame, corner_radius=18, fg_color=COLOR_BLANCO,
            border_width=3, border_color=COLOR_NEGRO
        )
        caja.pack(fill="x", pady=(20, 15))

        ctk.CTkLabel(
            caja, text="ESCRIBE UNA PALABRA EN FRANCES:", font=FUENTE_NEGRITA,
            text_color=COLOR_NEGRO, anchor="w"
        ).pack(fill="x", padx=20, pady=(20, 2))

        ctk.CTkLabel(
            caja, text="Aprende una palabra nuevo y añádela a tu mazo.",
            font=FUENTE_PEQUENA, text_color=COLOR_GRIS, anchor="w"
        ).pack(fill="x", padx=20, pady=(0, 12))

        self.entrada_palabra = ctk.CTkEntry(
            caja, font=FUENTE_NORMAL, height=44, corner_radius=12,
            border_width=3, border_color=COLOR_NEGRO, fg_color=COLOR_BLANCO,
            placeholder_text="bonjour!"
        )
        self.entrada_palabra.pack(fill="x", padx=20, pady=(0, 15))
        self.entrada_palabra.bind("<Return>", lambda evento: self._traducir_y_guardar())

        # Caja de resultado (oculta hasta que se traduce la primera palabra)
        self.caja_resultado = ctk.CTkFrame(
            caja, corner_radius=12, fg_color=COLOR_AMARILLO_CLARO,
            border_width=3, border_color=COLOR_NEGRO
        )
        self.texto_resultado = ctk.StringVar(value="")
        self.etiqueta_resultado = ctk.CTkLabel(
            self.caja_resultado, textvariable=self.texto_resultado, font=FUENTE_NEGRITA,
            text_color=COLOR_VERDE, anchor="w", justify="left"
        )
        self.etiqueta_resultado.pack(padx=15, pady=10)

        ctk.CTkButton(
            frame, text="Traducir y guardar", font=FUENTE_NEGRITA, height=48,
            corner_radius=12, fg_color=COLOR_AMARILLO, text_color=COLOR_NEGRO,
            hover_color=COLOR_AMARILLO, border_width=3, border_color=COLOR_NEGRO,
            command=self._traducir_y_guardar
        ).pack(fill="x")

        self.contador_estudio = self._crear_badge_contador(frame)

    def _traducir_y_guardar(self):
        palabra = self.entrada_palabra.get().strip()

        if not palabra:
            messagebox.showwarning("Aviso", "Escribe una palabra primero.")
            return

        traduccion,fiable = traductor.traducir(palabra)

        if traduccion.startswith("[Error"):
            messagebox.showerror("Error", traduccion)
            return

        if not fiable:
            self.texto_resultado.set(
                f"⚠ No se ha podido traducir \"{palabra}\".\nPrueba a escribir la palabra de nuevo."
            )
            self.caja_resultado.configure(fg_color=COLOR_NARANJA_CLARO)
            self.etiqueta_resultado.configure(text_color=COLOR_NARANJA_OSCURO)
            self.caja_resultado.pack(fill="x", padx=20, pady=(0, 15))
            return

        if database.existe_palabra(palabra):
            self.texto_resultado.set(f"✓ {palabra} → {traduccion}")
        else:
            database.guardar_tarjeta(palabra, traduccion)
            self._actualizar_contadores()
            self.texto_resultado.set(f"✓ {palabra} → {traduccion}")

        self.caja_resultado.configure(fg_color=COLOR_AMARILLO_CLARO)
        self.etiqueta_resultado.configure(text_color=COLOR_VERDE)
        self.caja_resultado.pack(fill="x", padx=20, pady=(0, 15))

        self.entrada_palabra.delete(0, "end")
        self.entrada_palabra.focus()

    # ---------- MODO REPASO ----------

    def _construir_modo_repaso(self):
        frame = self.frame_repaso

        ctk.CTkLabel(
            frame, text="🖐  Pulsa la tarjeta para ver la traduccion",
            font=FUENTE_PEQUENA, text_color=COLOR_GRIS
        ).pack(pady=(20, 15))

        self.tarjeta = ctk.CTkFrame(
            frame, width=340, height=220, corner_radius=20,
            fg_color=COLOR_BLANCO, border_width=3, border_color=COLOR_NEGRO
        )
        self.tarjeta.pack(pady=(0, 15))
        self.tarjeta.pack_propagate(False)

        self.etiqueta_idioma = ctk.CTkLabel(
            self.tarjeta, text="FRANCES", font=("Arial", 11, "bold"), text_color=COLOR_GRIS
        )
        self.etiqueta_idioma.place(relx=0.5, rely=0.15, anchor="center")

        self.etiqueta_palabra = ctk.CTkLabel(
            self.tarjeta, text="", font=FUENTE_GRANDE_NEGRITA, text_color=COLOR_NEGRO
        )
        self.etiqueta_palabra.place(relx=0.5, rely=0.5, anchor="center")

        # Contador de veces repasada, abajo a la izquierda de la tarjeta
        self.etiqueta_veces_repasada = ctk.CTkLabel(
            self.tarjeta, text="", font=FUENTE_PEQUENA, text_color=COLOR_GRIS
        )
        self.etiqueta_veces_repasada.place(relx=0.08, rely=0.85, anchor="w")

        self.boton_borrar = ctk.CTkButton(
            self.tarjeta, text="🗑", width=36, height=36, corner_radius=10,
            fg_color=COLOR_BLANCO, text_color=COLOR_NEGRO, hover_color=COLOR_AMARILLO_CLARO,
            border_width=3, border_color=COLOR_NEGRO, font=("Arial", 14),
            command=self._borrar_tarjeta_actual
        )
        self.boton_borrar.place(relx=0.9, rely=0.85, anchor="center")

        # Toda la tarjeta responde al clic para voltearse (menos el boton de borrar)
        for widget in (self.tarjeta, self.etiqueta_idioma, self.etiqueta_palabra):
            widget.bind("<Button-1>", lambda evento: self._voltear_tarjeta())

        self.boton_siguiente_tarjeta = ctk.CTkButton(
            frame, text="Siguiente tarjeta", font=FUENTE_NEGRITA, height=48,
            corner_radius=12, fg_color=COLOR_AMARILLO, text_color=COLOR_NEGRO,
            hover_color=COLOR_AMARILLO, border_width=3, border_color=COLOR_NEGRO,
            command=self._nueva_tarjeta_aleatoria
        )
        self.boton_siguiente_tarjeta.pack(fill="x")

        # Boton de reinicio: se oculta hasta que se hayan repasado todas las tarjetas
        self.boton_reiniciar_repaso = ctk.CTkButton(
            frame, text="🔄️ Volver a empezar", font=FUENTE_NEGRITA, height=48,
            corner_radius=12, fg_color=COLOR_AMARILLO, text_color=COLOR_NEGRO,
            hover_color=COLOR_AMARILLO, border_width=3, border_color=COLOR_NEGRO,
            command=self._reiniciar_repaso
        )

        self.contador_repaso = self._crear_badge_contador(frame)

    def _nueva_tarjeta_aleatoria(self):
        fila = database.obtener_tarjeta_aleatoria_sin_vistas(self.ids_vistos)

        if fila is None:
            self.id_actual = None
            self.palabra_actual = None
            self.traduccion_actual = None
            self.boton_borrar.place_forget()
            self.etiqueta_veces_repasada.configure(text="")

            if database.contar_tarjetas() == 0:
                # Todavia no se ha guardado ninguna palabra
                self.etiqueta_idioma.configure(text="")
                self.etiqueta_palabra.configure(
                    text="No hay tarjetas todavia.\nAnade alguna en Estudio.",
                    font=FUENTE_NEGRITA
                )
                self.boton_siguiente_tarjeta.pack(fill="x")
                self.boton_reiniciar_repaso.pack_forget()
            else:
                # Se han visto todas las tarjetas disponibles en esta sesion
                self.etiqueta_idioma.configure(text="")
                self.etiqueta_palabra.configure(
                    text="🎉 ¡Has repasado\ntodas las tarjetas!",
                    font=FUENTE_NEGRITA
                )
                self.boton_siguiente_tarjeta.pack_forget()
                self.boton_reiniciar_repaso.pack(fill="x")
            return

        self.id_actual, self.palabra_actual, self.traduccion_actual, veces_repasada = fila
        veces_repasada = database.incrementar_veces_repasada(self.id_actual)
        self.ids_vistos.add(self.id_actual)
        self.mostrando_traduccion = False
        self.tarjeta.configure(fg_color=COLOR_AZUL_CLARO)
        self.etiqueta_idioma.configure(text="FRANCES")
        self.etiqueta_palabra.configure(text=self.palabra_actual, font=FUENTE_GRANDE_NEGRITA)
        veces_texto = "vista 1 vez" if veces_repasada == 1 else f"vista {veces_repasada} veces"
        self.etiqueta_veces_repasada.configure(text=veces_texto)
        self.boton_borrar.place(relx=0.9, rely=0.85, anchor="center")

        # Aseguramos que se ve el boton "Siguiente tarjeta" y no el de reinicio
        # (por si veniamos de haber agotado el mazo y se pulso "Volver a empezar")
        self.boton_reiniciar_repaso.pack_forget()
        self.boton_siguiente_tarjeta.pack(fill="x")

    def _reiniciar_repaso(self):
        self.ids_vistos = set()
        self._nueva_tarjeta_aleatoria()

    def _voltear_tarjeta(self):
        if self.palabra_actual is None:
            return

        self.mostrando_traduccion = not self.mostrando_traduccion

        if self.mostrando_traduccion:
            self.etiqueta_idioma.configure(text="ESPAÑOL")
            self.etiqueta_palabra.configure(text=self.traduccion_actual)
        else:
            self.etiqueta_idioma.configure(text="FRANCES")
            self.etiqueta_palabra.configure(text=self.palabra_actual)

    def _borrar_tarjeta_actual(self):
        if self.id_actual is None:
            return
        database.eliminar_tarjeta(self.id_actual)
        self._nueva_tarjeta_aleatoria()
        self._actualizar_contadores()

    # ---------- CONTADOR (comun a ambas pestanas) ----------

    def _crear_badge_contador(self, padre):
        contenedor = ctk.CTkFrame(padre, fg_color=COLOR_FONDO)
        contenedor.pack(side="bottom", pady=20)

        badge = ctk.CTkFrame(
            contenedor, corner_radius=14, fg_color=COLOR_FONDO,
            border_width=2, border_color=COLOR_NEGRO
        )
        badge.pack()

        variable = ctk.StringVar(value="")
        ctk.CTkLabel(
            badge, textvariable=variable, font=FUENTE_PEQUENA, text_color=COLOR_GRIS
        ).pack(padx=14, pady=6)

        return variable

    def _actualizar_contadores(self):
        total = database.contar_tarjetas()
        texto = f"Tarjetas guardadas: {total}"
        self.contador_estudio.set(texto)
        self.contador_repaso.set(texto)


if __name__ == "__main__":
    raiz = ctk.CTk()
    app = AppFlashcards(raiz)
    raiz.mainloop()