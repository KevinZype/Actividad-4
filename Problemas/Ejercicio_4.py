# Ejercicio 4 - Validación de campos

import io
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
class Programador:
    def __init__(self, nombre, apellidos):
        self.nombre = nombre
        self.apellidos = apellidos


class EquipoMaratonProgramacion:
    def __init__(self, nombre, universidad, lenguaje, tamano):
        if tamano < 2 or tamano > 3:
            raise ValueError("El equipo debe tener mínimo dos y máximo tres programadores")
        self.nombre = nombre
        self.universidad = universidad
        self.lenguaje = lenguaje
        self.tamano = tamano
        self.programadores = []

    def esta_completo(self):
        return len(self.programadores) == self.tamano

    def anadir_programador(self, programador):
        if self.esta_completo():
            raise RuntimeError("El equipo está lleno, no se pueden añadir más programadores")
        self.programadores.append(programador)

    def validar_programador(self, programador):
        self.validar_texto(programador.nombre, "Nombre")
        self.validar_texto(programador.apellidos, "Apellidos")

    @staticmethod
    def validar_texto(texto, campo):
        if texto == "":
            raise ValueError(campo + ": no puede estar vacío")
        if not texto.replace(" ", "").isalpha():
            raise ValueError(campo + ": solo se permite texto (sin números ni símbolos)")
        if len(texto) >= 20:
            raise ValueError(campo + ": debe tener menos de 20 caracteres")


def main(nombre, universidad, lenguaje, tamano, integrantes):
    print("Nombre del equipo =")
    print(nombre)
    print("Universidad =")
    print(universidad)
    print("Lenguaje de programación =")
    print(lenguaje)
    equipo = EquipoMaratonProgramacion(nombre, universidad, lenguaje, tamano)

    print("Datos de los integrantes del equipo")
    for nombre_integrante, apellidos in integrantes:
        print("Nombre del integrante =")
        print(nombre_integrante)
        print("Apellidos del integrante =")
        print(apellidos)
        programador = Programador(nombre_integrante, apellidos)
        equipo.validar_programador(programador)
        equipo.anadir_programador(programador)

    return equipo


class App:
    def __init__(self, ventana):
        self.ventana = ventana

        self.tarea = None
        self.lineas = []
        self.ejecutando = False
        self.resumen = ""

        ventana.title("Ejercicio 4 · Validación de campos")
        ventana.geometry("1040x700")
        ventana.minsize(960, 640)
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

        tk.Label(encabezado, text="Ejercicio 4 · Validación de campos",
                 font=(self.letra, 20, "bold"), bg=FONDO, fg=TEXTO).pack(anchor="w")
        tk.Label(encabezado, text="Clase EquipoMaratónProgramación: validación de nombres y apellidos",
                 font=(self.letra, 11), bg=FONDO, fg=GRIS).pack(anchor="w", pady=(2, 0))

    def crear_cuerpo(self):
        cuerpo = tk.Frame(self.ventana, bg=FONDO)
        cuerpo.pack(fill="both", expand=True, padx=32, pady=8)
        cuerpo.columnconfigure(0, weight=1, uniform="col")
        cuerpo.columnconfigure(1, weight=1, uniform="col")
        cuerpo.rowconfigure(0, weight=1)

        izquierda = tk.Frame(cuerpo, bg=FONDO)
        izquierda.grid(row=0, column=0, sticky="nsew")
        self.crear_equipo(izquierda)
        self.crear_integrantes(izquierda)

        derecha = tk.Frame(cuerpo, bg=FONDO)
        derecha.grid(row=0, column=1, sticky="nsew", padx=(16, 0))

        tk.Label(derecha, text="SALIDA", font=(self.letra, 9, "bold"),
                 bg=FONDO, fg=GRIS).pack(anchor="w", pady=(0, 6))

        marco = tk.Frame(derecha, bg=TARJETA, highlightthickness=1, highlightbackground=BORDE)
        marco.pack(fill="both", expand=True)

        self.salida = tk.Text(marco, font=(self.mono, 11), bg=TARJETA, fg=TEXTO,
                              relief="flat", bd=0, highlightthickness=0,
                              padx=18, pady=16, wrap="word", cursor="arrow",
                              spacing1=2, spacing3=2, insertwidth=0, width=10, height=10)
        self.salida.pack(fill="both", expand=True)

        self.salida.tag_configure("normal", foreground=TEXTO)
        self.salida.tag_configure("dato", foreground=ACENTO)
        self.salida.tag_configure("error", foreground=ERROR)
        self.salida.config(state="disabled")

    def crear_equipo(self, padre):
        tk.Label(padre, text="DATOS DEL EQUIPO", font=(self.letra, 9, "bold"),
                 bg=FONDO, fg=GRIS).pack(anchor="w", pady=(0, 6))

        tarjeta = tk.Frame(padre, bg=TARJETA, highlightthickness=1, highlightbackground=BORDE)
        tarjeta.pack(fill="x")
        tarjeta.columnconfigure(1, weight=1)

        self.campo_nombre = self.crear_campo(tarjeta, "Equipo", 0, "EquipoUNAL")
        self.campo_universidad = self.crear_campo(tarjeta, "Universidad", 1, "Nacional")
        self.campo_lenguaje = self.crear_campo(tarjeta, "Lenguaje", 2, "Java")
        self.campo_tamano = self.crear_campo(tarjeta, "Tamaño", 3, "2")

    def crear_integrantes(self, padre):
        tk.Label(padre, text="INTEGRANTES", font=(self.letra, 9, "bold"),
                 bg=FONDO, fg=GRIS).pack(anchor="w", pady=(16, 6))

        tarjeta = tk.Frame(padre, bg=TARJETA, highlightthickness=1, highlightbackground=BORDE)
        tarjeta.pack(fill="x")
        tarjeta.columnconfigure(1, weight=1, uniform="campo")
        tarjeta.columnconfigure(2, weight=1, uniform="campo")

        tk.Label(tarjeta, text="Nombre", font=(self.letra, 9),
                 bg=TARJETA, fg=GRIS).grid(row=0, column=1, sticky="w", pady=(12, 0))
        tk.Label(tarjeta, text="Apellidos", font=(self.letra, 9),
                 bg=TARJETA, fg=GRIS).grid(row=0, column=2, sticky="w", pady=(12, 0))

        datos = [("Kevin", "Zype"), ("Vec", "Diaz"), ("", "")]
        self.integrantes = []

        for i in range(3):
            tk.Label(tarjeta, text="Integrante " + str(i + 1), font=(self.letra, 10),
                     bg=TARJETA, fg=GRIS).grid(row=i + 1, column=0, sticky="w", padx=(18, 12), pady=6)
            entrada_nombre = self.crear_entrada(tarjeta, i + 1, 1, datos[i][0], (0, 8))
            entrada_apellidos = self.crear_entrada(tarjeta, i + 1, 2, datos[i][1], (0, 18))
            self.integrantes.append((entrada_nombre, entrada_apellidos))

    def crear_campo(self, padre, texto, fila, valor):
        tk.Label(padre, text=texto, font=(self.letra, 10),
                 bg=TARJETA, fg=GRIS).grid(row=fila, column=0, sticky="w", padx=(18, 12), pady=6)
        return self.crear_entrada(padre, fila, 1, valor, (0, 18))

    def crear_entrada(self, padre, fila, columna, valor, padx):
        entrada = tk.Entry(padre, font=(self.letra, 12), bg=FONDO, fg=TEXTO,
                           relief="flat", highlightthickness=1, highlightbackground=BORDE,
                           highlightcolor=ACENTO, insertbackground=TEXTO)
        entrada.grid(row=fila, column=columna, sticky="ew", padx=padx, pady=6, ipady=5)
        entrada.insert(0, valor)
        return entrada

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

        nombre = self.campo_nombre.get().strip()
        universidad = self.campo_universidad.get().strip()
        lenguaje = self.campo_lenguaje.get().strip()

        try:
            tamano = int(self.campo_tamano.get())
        except ValueError:
            self.estado.config(text="Revisa el tamaño: debe ser un número entero", fg=ERROR)
            return

        integrantes = []
        for entrada_nombre, entrada_apellidos in self.integrantes:
            nombre_integrante = entrada_nombre.get().strip()
            apellidos = entrada_apellidos.get().strip()
            if nombre_integrante != "" or apellidos != "":
                integrantes.append((nombre_integrante, apellidos))

        self.limpiar()
        self.ejecutando = True
        self.estado.config(text="Ejecutando...", fg=GRIS)

        equipo = None
        excepcion = None
        buffer = io.StringIO()
        try:
            with redirect_stdout(buffer):
                equipo = main(nombre, universidad, lenguaje, tamano, integrantes)
        except Exception as error:
            excepcion = error

        lineas = []
        esperando_dato = False
        for linea in buffer.getvalue().splitlines():
            if esperando_dato:
                lineas.append((linea, "dato"))
                esperando_dato = False
            else:
                lineas.append((linea, "normal"))
                if linea.endswith(" ="):
                    esperando_dato = True

        if excepcion is not None:
            lineas.append((type(excepcion).__name__ + ": " + str(excepcion), "error"))
            self.resumen = "Ejecución terminada con excepción"
        elif equipo.esta_completo():
            self.resumen = "Ejecución terminada · equipo completo"
        else:
            self.resumen = ("Ejecución terminada · equipo incompleto ("
                            + str(len(equipo.programadores)) + " de " + str(equipo.tamano) + ")")

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

        self.tarea = self.ventana.after(150, self.mostrar_linea)

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
