# Ejercicio 5 - Lectura de archivos

import io
import os
import tkinter as tk
from contextlib import redirect_stdout
from tkinter import filedialog
from tkinter import font as tkfont

# Colores
FONDO = "#F6F6F3"
TARJETA = "#FFFFFF"
BORDE = "#E3E3DE"
TEXTO = "#1F2933"
GRIS = "#8A94A0"
ACENTO = "#2F5BEA"
ACENTO_HOVER = "#2449C4"
ERROR = "#D64545"


# Programa del ejercicio
def main(ruta):
    flujo = open(ruta, "rb")
    lector = io.TextIOWrapper(flujo, encoding="utf-8")

    try:
        linea = lector.readline()
        while linea != "":
            print(linea.rstrip("\n"))
            linea = lector.readline()
    finally:
        lector.close()


class App:
    def __init__(self, ventana):
        self.ventana = ventana

        self.tarea = None
        self.lineas = []
        self.ejecutando = False
        self.resumen = ""
        self.pausa = 120
        self.carpeta = os.path.dirname(os.path.abspath(__file__))

        ventana.title("Ejercicio 5 · Lectura de archivos")
        ventana.geometry("760x660")
        ventana.minsize(640, 560)
        ventana.configure(bg=FONDO)
        ventana.bind("<Return>", lambda e: self.ejecutar())

        self.letra = self.buscar_fuente(
            ["Inter", "Segoe UI", "SF Pro Text", "Helvetica Neue", "Ubuntu", "Arial"],
            "Helvetica")
        self.mono = self.buscar_fuente(
            ["JetBrains Mono", "Cascadia Code", "Consolas", "Menlo", "DejaVu Sans Mono", "Courier New"],
            "Courier")

        self.crear_encabezado()
        self.crear_pie()
        self.crear_cuerpo()

    def buscar_fuente(self, opciones, por_defecto):
        instaladas = tkfont.families()
        for nombre in opciones:
            if nombre in instaladas:
                return nombre
        return por_defecto

    def crear_encabezado(self):
        encabezado = tk.Frame(self.ventana, bg=FONDO)
        encabezado.pack(fill="x", padx=32, pady=(28, 12))

        tk.Label(encabezado, text="Ejercicio 5 · Lectura de archivos",
                 font=(self.letra, 20, "bold"), bg=FONDO, fg=TEXTO).pack(anchor="w")
        tk.Label(encabezado, text="Clase LeerArchivo: lectura de prueba.txt con un flujo de bytes",
                 font=(self.letra, 11), bg=FONDO, fg=GRIS).pack(anchor="w", pady=(2, 0))

    def crear_cuerpo(self):
        cuerpo = tk.Frame(self.ventana, bg=FONDO)
        cuerpo.pack(fill="both", expand=True, padx=32, pady=8)

        self.crear_datos(cuerpo)

        tk.Label(cuerpo, text="SALIDA", font=(self.letra, 9, "bold"),
                 bg=FONDO, fg=GRIS).pack(anchor="w", pady=(16, 6))

        marco = tk.Frame(cuerpo, bg=TARJETA, highlightthickness=1, highlightbackground=BORDE)
        marco.pack(fill="both", expand=True)

        self.salida = tk.Text(marco, font=(self.mono, 12), bg=TARJETA, fg=TEXTO,
                              relief="flat", bd=0, highlightthickness=0,
                              padx=20, pady=18, wrap="word", cursor="arrow",
                              spacing1=3, spacing3=3, insertwidth=0, width=10, height=10)
        self.salida.pack(fill="both", expand=True)

        self.salida.tag_configure("normal", foreground=TEXTO)
        self.salida.tag_configure("error", foreground=ERROR)
        self.salida.config(state="disabled")

    def crear_datos(self, padre):
        tk.Label(padre, text="ARCHIVO DE TEXTO", font=(self.letra, 9, "bold"),
                 bg=FONDO, fg=GRIS).pack(anchor="w", pady=(0, 6))

        tarjeta = tk.Frame(padre, bg=TARJETA, highlightthickness=1, highlightbackground=BORDE)
        tarjeta.pack(fill="x")
        tarjeta.columnconfigure(1, weight=1)

        self.campo_archivo = self.crear_campo(tarjeta, "Archivo", 0, "prueba.txt")

        boton_examinar = self.crear_boton(tarjeta, "Examinar", self.examinar,
                                          TARJETA, TEXTO, "#EFEFEA", BORDE)
        boton_examinar.grid(row=0, column=2, padx=(0, 18), pady=10)

    def crear_campo(self, padre, texto, fila, valor):
        tk.Label(padre, text=texto, font=(self.letra, 10),
                 bg=TARJETA, fg=GRIS).grid(row=fila, column=0, sticky="w", padx=(18, 12), pady=10)

        campo = tk.Entry(padre, font=(self.letra, 12), bg=FONDO, fg=TEXTO,
                         relief="flat", highlightthickness=1, highlightbackground=BORDE,
                         highlightcolor=ACENTO, insertbackground=TEXTO)
        campo.grid(row=fila, column=1, sticky="ew", padx=(0, 18), pady=10, ipady=5)
        campo.insert(0, valor)
        return campo

    def crear_pie(self):
        pie = tk.Frame(self.ventana, bg=FONDO)
        pie.pack(side="bottom", fill="x", padx=32, pady=(8, 26))

        self.estado = tk.Label(pie, text="Listo para ejecutar",
                               font=(self.letra, 10), bg=FONDO, fg=GRIS)
        self.estado.pack(side="left")

        boton_ejecutar = self.crear_boton(pie, "Ejecutar", self.ejecutar,
                                          ACENTO, "#FFFFFF", ACENTO_HOVER, ACENTO)
        boton_ejecutar.pack(side="right")

        boton_limpiar = self.crear_boton(pie, "Limpiar", self.limpiar,
                                         TARJETA, TEXTO, "#EFEFEA", BORDE)
        boton_limpiar.pack(side="right", padx=(0, 10))

    def crear_boton(self, padre, texto, comando, fondo, color, hover, borde):
        boton = tk.Label(padre, text=texto, font=(self.letra, 11, "bold"),
                         bg=fondo, fg=color, padx=22, pady=9, cursor="hand2",
                         highlightthickness=1, highlightbackground=borde)
        boton.bind("<Button-1>", lambda e: comando())
        boton.bind("<Enter>", lambda e: boton.config(bg=hover))
        boton.bind("<Leave>", lambda e: boton.config(bg=fondo))
        return boton

    def examinar(self):
        ruta = filedialog.askopenfilename(title="Seleccionar archivo de texto",
                                          initialdir=self.carpeta,
                                          filetypes=[("Archivos de texto", "*.txt"),
                                                     ("Todos los archivos", "*.*")])
        if ruta != "":
            self.campo_archivo.delete(0, "end")
            self.campo_archivo.insert(0, ruta)

    def ejecutar(self):
        if self.ejecutando:
            return

        texto = self.campo_archivo.get().strip()
        if texto == "":
            self.estado.config(text="Escribe el nombre del archivo", fg=ERROR)
            return

        ruta = os.path.expanduser(texto)
        if not os.path.isabs(ruta):
            ruta = os.path.join(self.carpeta, ruta)

        if os.path.isfile(ruta) and os.path.getsize(ruta) > 100000:
            self.estado.config(text="El archivo es muy grande (máximo 100 KB)", fg=ERROR)
            return

        self.limpiar()
        self.ejecutando = True
        self.estado.config(text="Leyendo...", fg=GRIS)

        mensaje = None
        buffer = io.StringIO()
        try:
            with redirect_stdout(buffer):
                main(ruta)
        except FileNotFoundError:
            mensaje = "FileNotFoundError: no se encontró el archivo " + ruta
        except Exception as error:
            mensaje = type(error).__name__ + ": " + str(error)

        lineas = []
        for linea in buffer.getvalue().split("\n")[:-1]:
            lineas.append((linea, "normal"))

        if mensaje is not None:
            lineas.append((mensaje, "error"))
            self.resumen = "Lectura terminada con excepción"
        elif len(lineas) == 0:
            self.resumen = "Lectura terminada · el archivo está vacío"
        elif len(lineas) == 1:
            self.resumen = "Lectura terminada · 1 línea"
        else:
            self.resumen = "Lectura terminada · " + str(len(lineas)) + " líneas"

        if len(lineas) > 30:
            self.pausa = 0
        else:
            self.pausa = 120

        self.lineas = lineas
        self.mostrar_linea()

    def mostrar_linea(self):
        if len(self.lineas) == 0:
            self.ejecutando = False
            self.tarea = None
            self.estado.config(text=self.resumen)
            return

        texto, etiqueta = self.lineas.pop(0)

        self.salida.config(state="normal")
        self.salida.insert("end", texto + "\n", etiqueta)
        self.salida.see("end")
        self.salida.config(state="disabled")

        self.tarea = self.ventana.after(self.pausa, self.mostrar_linea)

    def limpiar(self):
        if self.tarea is not None:
            self.ventana.after_cancel(self.tarea)
            self.tarea = None

        self.lineas = []
        self.ejecutando = False

        self.salida.config(state="normal")
        self.salida.delete("1.0", "end")
        self.salida.config(state="disabled")
        self.estado.config(text="Listo para ejecutar", fg=GRIS)


if __name__ == "__main__":
    ventana = tk.Tk()
    App(ventana)
    ventana.mainloop()
