# Ejercicio 3 - Catchs múltiples

import io
import math
import tkinter as tk
from contextlib import redirect_stdout
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
class CalculosNumericos:
    @staticmethod
    def logaritmo(valor):
        if valor <= 0:
            raise ArithmeticError("El valor debe ser un número positivo para calcular el logaritmo")
        return math.log(valor)

    @staticmethod
    def raiz_cuadrada(valor):
        if valor <= 0:
            raise ArithmeticError("El valor debe ser un número positivo para calcular la raíz cuadrada")
        return math.sqrt(valor)


def main(valor):
    try:
        resultado = CalculosNumericos.logaritmo(valor)
        print("Logaritmo neperiano =", round(resultado, 4))
    except ArithmeticError as error:
        print(error)
    except Exception:
        print("Ocurrió un error inesperado")

    try:
        resultado = CalculosNumericos.raiz_cuadrada(valor)
        print("Raíz cuadrada =", round(resultado, 4))
    except ArithmeticError as error:
        print(error)
    except Exception:
        print("Ocurrió un error inesperado")


class App:
    def __init__(self, ventana):
        self.ventana = ventana

        self.tarea = None
        self.lineas = []
        self.ejecutando = False

        ventana.title("Ejercicio 3 · Catchs múltiples")
        ventana.geometry("760x520")
        ventana.minsize(640, 460)
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

        tk.Label(encabezado, text="Ejercicio 3 · Catchs múltiples",
                 font=(self.letra, 20, "bold"), bg=FONDO, fg=TEXTO).pack(anchor="w")
        tk.Label(encabezado, text="Clase CálculosNuméricos: logaritmo y raíz cuadrada",
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
        self.salida.tag_configure("dato", foreground=ACENTO)
        self.salida.tag_configure("error", foreground=ERROR)
        self.salida.config(state="disabled")

    def crear_datos(self, padre):
        tk.Label(padre, text="DATO DE ENTRADA", font=(self.letra, 9, "bold"),
                 bg=FONDO, fg=GRIS).pack(anchor="w", pady=(0, 6))

        tarjeta = tk.Frame(padre, bg=TARJETA, highlightthickness=1, highlightbackground=BORDE)
        tarjeta.pack(fill="x")
        tarjeta.columnconfigure(1, weight=1)

        self.campo_valor = self.crear_campo(tarjeta, "Valor numérico", 0, "-200")

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

    def ejecutar(self):
        if self.ejecutando:
            return

        texto = self.campo_valor.get().strip()

        try:
            valor = float(texto.replace(",", "."))
        except ValueError:
            valor = None

        if valor is None or not math.isfinite(valor):
            self.estado.config(text="Revisa el dato: debe ser un número", fg=ERROR)
            return

        self.limpiar()
        self.ejecutando = True
        self.estado.config(text="Ejecutando...", fg=GRIS)

        lineas = [[("Valor numérico = ", "normal"), (texto, "dato")]]

        buffer = io.StringIO()
        with redirect_stdout(buffer):
            main(valor)

        for linea in buffer.getvalue().splitlines():
            if " = " in linea:
                partes = linea.split(" = ")
                lineas.append([(partes[0] + " = ", "normal"), (partes[1], "dato")])
            else:
                lineas.append([(linea, "error")])

        self.lineas = lineas
        self.mostrar_linea()

    def mostrar_linea(self):
        if len(self.lineas) == 0:
            self.ejecutando = False
            self.tarea = None
            self.estado.config(text="Ejecución terminada")
            return

        segmentos = self.lineas.pop(0)

        self.salida.config(state="normal")
        for texto, etiqueta in segmentos:
            self.salida.insert("end", texto, etiqueta)
        self.salida.insert("end", "\n")
        self.salida.config(state="disabled")

        self.tarea = self.ventana.after(450, self.mostrar_linea)

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
