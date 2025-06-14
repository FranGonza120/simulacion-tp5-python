from objetos.VectorEstado import VectorEstado


class Simulador():
    def __init__(self, x, a_dc, b_dc, c_dc, b_c):
        self._func_tension, self._iteraciones_runge_kutta = self.obtener_func_tension(
            x, a_dc, b_dc, c_dc, b_c)
        self._cant_iteraciones = 0
        self._cant_dias_a_simular = None

    def simular(self, dias, j, i, a_c, b_c, a_llegada_cliente, b_llegada_cliente):
        self._vector_estado = VectorEstado(
            self._func_tension, dias, j, i, a_c, b_c, a_llegada_cliente, b_llegada_cliente)

        self._cant_dias_a_simular = dias

        ult_guardado = False
        vectores_guardados = []

        while not self._vector_estado.finalizo() and self._cant_iteraciones < 100000:
            self._vector_estado.simular()
            self._cant_iteraciones += 1

            if self._vector_estado.guardar(j) and len(vectores_guardados) < i:
                if self._cant_iteraciones == 100000:
                    ult_guardado = True
                vectores_guardados.append(self._vector_estado.crear_vector())

        max_cola_clientes = self._vector_estado.determinar_cant_clientes_vecs()
        if not ult_guardado:
            vectores_guardados.append(self._vector_estado.crear_vector())

        return vectores_guardados, max_cola_clientes

    def crear_salidas(self):
        info_simulacion = self._vector_estado.crear_salida_info_simulacion(
            self._cant_iteraciones)
        reporte_simulacion = self._vector_estado.crear_reporte_simulacion()

        return info_simulacion, reporte_simulacion

    @staticmethod
    def obtener_func_tension(x, a, b, c, b_c):
        # x creo que es la equivalencia en minutos para cada uno de los valores
        # La func_tension es nivel de tension y da la cantidad de minutos
        x1 = 0
        y1 = 0
        h = 0.01
        k1 = k2 = k3 = k4 = None
        xn1 = yn1 = None
        func_tension = {}
        vec_iteraciones = []
        func_tension[y1] = x1
        lim = b_c

        while y1 <= lim:
            k1 = (a*((y1 + b)**2) + c)

            y2 = y1 + k1 * h/2
            k2 = (a*((y2 + b)**2) + c)

            y3 = y1 + k2 * h/2
            k3 = (a*((y3 + b)**2) + c)

            y4 = y1 + k3 * h
            k4 = (a*((y4 + b)**2) + c)

            yn1 = y1 + (h/6)*(k1 + 2*k2 + 2*k3 + k4)
            xn1 = x1 + h
            func_tension[yn1] = xn1 / x
            vec_iteraciones.append(
                {"x1": x1, "y1": y1, "k1": k1, "k2": k2, "k3": k3,
                 "k4": k4, "xn1": xn1, "yn1": yn1})

            x1 = xn1
            y1 = yn1
        return func_tension, vec_iteraciones

    def get_iteraciones_runge_kutta(self):
        return self._iteraciones_runge_kutta
