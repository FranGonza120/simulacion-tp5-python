from PyQt5.QtWidgets import (
    QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QStackedWidget,
    QTableWidget, QTableWidgetItem, QWidget, QHeaderView,
    QAbstractScrollArea
)
from PyQt5.QtCore import Qt

from objetos.Simulador import Simulador

from .PaginaBase import PaginaBase


class PaginaResultados(PaginaBase):
    def __init__(
        self,
        callback_volver,
        callback_cerrar,
        dias,
        j,
        i,
        a_c,
        b_c,
        a_lc,
        b_lc,
        x,
        a_dc,
        b_dc,
        c_dc
    ):
        super().__init__("Resultados", callback_volver, callback_cerrar)
        self.boton_extra.hide()
        self.dias = dias
        self.j = j
        self.i = i
        self.a_c = a_c
        self.b_c = b_c
        self.a_lc = a_lc
        self.b_lc = b_lc
        self.x = x
        self.a_dc = a_dc
        self.b_dc = b_dc
        self.c_dc = c_dc

        simulador = Simulador(self.x, self.a_dc, self.b_dc, self.c_dc)
        # Aca vamos a tener que sacar los datos para hacer los reportes sobre las consginas pedidas
        # Faltan hacer la generacion de las tablas
        # Faltan mostrar lo reportes
        # Falta poder sacar los reportes de la Simulacion
        self.iteraciones, self.max_cant_clientes, self.reporte = simulador.simular(
            self.dias, self.j, self.i, self.a_c, self.b_c, self.a_lc, self.b_lc)
        self.info_simulacion = simulador.cuanto_se_simulo()
        self.runge_kutta = simulador.get_iteraciones_runge_kutta()

        self.agregar_widget(
            QLabel(f"<h2>Simulación de Centro de Masajes Urbanos</h2>"))
        self.stack = QStackedWidget()
        self.stack.addWidget(self._widget_vectores())
        self.stack.addWidget(self._widget_runge_kutta())

        # Botones de navegación de vistas
        botones = QHBoxLayout()
        for txt, handler in [
            ("Vectores Estado", self.mostrar_vectores),
            ("Runge Kutta", self.mostrar_runge_kutta)
        ]:
            btn = QPushButton(txt)
            btn.clicked.connect(handler)
            botones.addWidget(btn)
        self.contenedor.addLayout(botones)

        # Navegación interna de serie
        self.contenedor.addWidget(self.stack)

    def _widget_runge_kutta(self):
        contenedor = QWidget()
        layout = QVBoxLayout(contenedor)

        layout.addWidget(QLabel(f"""
            <h3>Aproximación iterativa de dC/dx = {self.a_dc}*(C(x) + {self.b_dc})^2 + {self.c_dc}</h3>
        """))

        tabla = QTableWidget(len(self.runge_kutta), 8)
        tabla.setHorizontalHeaderLabels(
            ["x i", "C i", "k1", "k2", "k3", "k4", "x i + 1", "C i + 1"]
        )
        tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for i, it in enumerate(self.runge_kutta):
            for j, clave in enumerate(it):
                item = QTableWidgetItem(f"{it[clave]:.4f}")
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                tabla.setItem(i, j, item)
        layout.addWidget(tabla)

        return contenedor

    def _widget_vectores(self):
        contenedor = QWidget()
        layout = QVBoxLayout(contenedor)

        layout.addWidget(QLabel(self.info_simulacion))
        layout.addWidget(QLabel(f"""
            <h3>Parametros Seleccionados</h3>
            <p>La distribucion de tension muscular es U({self.a_c}, {self.b_c}).</p>
            <p>La distribucion de llegada de los clientes es U({self.a_lc}, {self.b_lc}).</p>
            <p>Fueron recolectados {self.i} vectores a partir del minuto {self.j}.</p>
            """))
        layout.addWidget(QLabel(self.reporte))

        tabla = QTableWidget(len(self.iteraciones), 26 +
                             self.max_cant_clientes * 4)
        cabecera = ["Reloj", "Estado Actual", "C J Tiempo", "C J Prox Ev", "L C RND",
                    "L C Tiempo", "L C Prox Ev", "RND M", "Masajista Asig", "F J Tiempo",
                    "F J Prox Ev", "F S M A RND", "F S M A Tension", "F S M A Tiempo",
                    "F S M A Prox Ev", "F S M B RND", "F S M B Tiempo", "F S M B Prox Ev", "F S M Ap RND", "F S M Ap Tiempo", "F S M Ap Prox Ev", "M A Estado",
                    "M B Estado", "M Ap Estado", "Cola Max", "Acc Recaudacion Daria", "Acc Recaudacion Total", "Cant Dias Simulados"]

        for i in range(self.max_cant_clientes):
            cabecera.extend(["ID", "Estado", "Hora Llegada", "Tiempo Espera"])

        tabla.setHorizontalHeaderLabels(cabecera)

        for i, valores in enumerate(self.iteraciones):
            for j, v in enumerate(valores):
                item = QTableWidgetItem(v)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                item.setToolTip(item.text())
                tabla.setItem(i, j, item)

        tabla.resizeColumnsToContents()
        tabla.resizeRowsToContents()
        tabla.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        tabla.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        tabla.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        layout.addWidget(tabla)

        return contenedor

    # Vistas
    def mostrar_vectores(self):
        self.stack.setCurrentIndex(0)

    def mostrar_runge_kutta(self):
        self.stack.setCurrentIndex(1)
