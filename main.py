import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QStackedWidget

from core.utilidades import aplicar_estilo

from objetos.Id import Id

from paginas.PaginaInicio import PaginaInicio
from paginas.PaginaElegirVals import PaginaElegirVals
from paginas.PaginaResultados import PaginaResultados


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulador de Colas de Centro de Masajes Urbanos")
        self.setGeometry(100, 100, 800, 900)

        # Layout principal
        main_layout = QVBoxLayout(self)
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)

        # Página inicial
        inicio = PaginaInicio(
            callback_seleccion=self.elegir_vals,
            callback_volver=self.volver,
            callback_cerrar=self.cerrar_aplicacion,
        )
        self.stack.addWidget(inicio)

    def elegir_vals(self):
        elegir = PaginaElegirVals(
            callback_generado=self.ir_a_resultados,
            callback_volver=self.volver,
            callback_cerrar=self.cerrar_aplicacion,
        )
        self.stack.addWidget(elegir)
        self.stack.setCurrentWidget(elegir)

    def ir_a_resultados(self, dias, j, i, a_c, b_c, a_lc, b_lc, x, a_dc, b_dc, c_dc):
        resultados = PaginaResultados(
            callback_volver=self.volver,
            callback_cerrar=self.cerrar_aplicacion,
            dias=dias,
            j=j,
            i=i,
            a_c=a_c,
            b_c=b_c,
            a_lc=a_lc,
            b_lc=b_lc,
            x=x,
            a_dc=a_dc,
            b_dc=b_dc,
            c_dc=c_dc
        )
        self.stack.addWidget(resultados)
        self.stack.setCurrentWidget(resultados)

    def volver(self, pagina_actual):
        if isinstance(pagina_actual, PaginaResultados):
            Id().reset()
        self.stack.removeWidget(pagina_actual)
        self.stack.setCurrentIndex(self.stack.count() - 1)

    @staticmethod
    def cerrar_aplicacion(self):
        QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    aplicar_estilo(app, modo="oscuro")

    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec())
