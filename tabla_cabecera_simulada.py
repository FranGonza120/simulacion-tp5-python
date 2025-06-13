# tabla_cabecera_simulada.py
from PyQt5.QtWidgets import (
    QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout
)
import sys


def tabla_con_cabecera_agrupada():
    ventana = QWidget()
    ventana.setWindowTitle("Cabecera simulada con setSpan()")
    layout = QVBoxLayout(ventana)

    tabla = QTableWidget(7, 4)  # 5 filas de datos + 2 filas de encabezado
    tabla.setVerticalHeaderLabels(
        ["", ""] + [f"Fila {i}" for i in range(1, 6)])

    # Insertar títulos agrupados
    tabla.setSpan(0, 0, 1, 2)  # Agrupar columnas 0 y 1
    tabla.setSpan(0, 2, 1, 2)  # Agrupar columnas 2 y 3
    tabla.setItem(0, 0, QTableWidgetItem("Datos personales"))
    tabla.setItem(0, 2, QTableWidgetItem("Datos de contacto"))

    tabla.setItem(1, 0, QTableWidgetItem("Nombre"))
    tabla.setItem(1, 1, QTableWidgetItem("Edad"))
    tabla.setItem(1, 2, QTableWidgetItem("Email"))
    tabla.setItem(1, 3, QTableWidgetItem("Teléfono"))

    # Cargar datos
    for i in range(2, 7):
        tabla.setItem(i, 0, QTableWidgetItem(f"Persona {i-1}"))
        tabla.setItem(i, 1, QTableWidgetItem(str(20 + i)))
        tabla.setItem(i, 2, QTableWidgetItem(f"persona{i}@mail.com"))
        tabla.setItem(i, 3, QTableWidgetItem(f"1234-{i}"))

    layout.addWidget(tabla)
    ventana.resize(800, 300)
    ventana.show()
    return ventana


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = tabla_con_cabecera_agrupada()
    sys.exit(app.exec_())
