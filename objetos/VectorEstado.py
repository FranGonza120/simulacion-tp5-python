from objetos.LlegadaCliente import LlegadaCliente
from objetos.FinServicioMA import FinServicioMA
from objetos.FinServicioMAp import FinServicioMAp
from objetos.FinServicioMB import FinServicioMB
from objetos.Estado import Estado
from objetos.Cliente import Cliente
from objetos.Masajista import Masajista
from objetos.FinJornadaLaboral import FinJornadaLaboral
from objetos.ComienzoJornadaLaboral import ComienzoJornadaLaboral

# Hay que cambiar la implementación de los Clientes para que los objetos se
# reutilicen. Y que estos nos muevan de posición sino que solo se agregan
# clientes a la cola cuando cuando todos los demás se encuentran activos.

# El momento del calculo y el calculo de los proximos eventos de
# ComienzoJornadaLaboral, FinSimulacion y FinJornadaLaboral se
# deben cambiar según el profe, no se como


class VectorEstado():
    def __init__(self, func_tension, dias, j, i, a_c, b_c, a_llegada_cliente, b_llegada_cliente):
        self._reloj = 0
        self._eventos = {"C J": ComienzoJornadaLaboral(), "L C": LlegadaCliente(a_llegada_cliente, b_llegada_cliente),
                         "F J": FinJornadaLaboral(), "F M A": FinServicioMA(
            a_c, b_c, func_tension),
            "F M B": FinServicioMB(), "F M Ap": FinServicioMAp()}
        self._estados_cliente, self._estados_masajistas = self.inicializar_estados()
        self._masajistas = self.inicializar_masajistas()
        self._precio_masajistas = {"M A": 3500, "M B": 3500, "M Ap": 1800}
        self._clientes = {"M A":  [], "M B":  [], "M Ap": []}
        self._dias_a_simular = dias
        self._cant_dias_simulados = 0
        self._evento_actual = ""
        self._acc_recaudacion_diaria = 0
        self._acc_recaudacion_total = 0
        self._cant_max_cola = 0

    def simular(self):
        if self._cant_dias_simulados == self._dias_a_simular:
            return
        evento = self.determinar_prox_ev()
        self._reloj = evento.get_prox_ev()
        self._evento_actual = evento.get_nombre()
        # print("El evento actual es ", self._evento_actual)
        if self._evento_actual not in ("Fin Servicio M A",
                                       "Fin Servicio M B",
                                       "Fin Servicio M Ap"):
            evento.calcular_prox_ev(self._reloj)
        # Tengo que tomar en cuenta cuando un evento se cancela y cuando un
        # evento vuelve a necesitar calcular su tiempo
        if self._evento_actual == "Comienzo Jornada Laboral":
            llegada = self._eventos["L C"]
            llegada.calcular_prox_ev(self._reloj)
            if self._reloj != 0:
                self._cant_dias_simulados += 1
                self._acc_recaudacion_total += self._acc_recaudacion_diaria
                self._acc_recaudacion_diaria = 0
            else:
                fin_jornada = self._eventos["F J"]
                fin_jornada.calcular_prox_ev(self._reloj)

        elif self._evento_actual == "Fin Jornada Laboral":
            llegada = self._eventos["L C"]
            llegada.set_prox_ev_none()

        elif self._evento_actual == "Llegada Cliente":
            cod_masajista = evento.asignar_masajista()
            ocupado = self._masajistas[cod_masajista].estas(
                self._estados_masajistas["O"])
            self.nuevo_cliente(cod_masajista, ocupado, self._reloj)

            if not ocupado:
                self._masajistas[cod_masajista].set_estado(
                    self._estados_masajistas["O"])
                fin_servicio = self._eventos[f"F {cod_masajista}"]
                fin_servicio.calcular_prox_ev(self._reloj)
            else:
                long_cola = self.determinar_cant_cola()
                if self._cant_max_cola < long_cola:
                    self._cant_max_cola = long_cola

        elif self._evento_actual in ("Fin Servicio M A",
                                     "Fin Servicio M B", "Fin Servicio M Ap"):
            cod = self._evento_actual[13:]
            # Cambiar funcion cobrar_cliente para que sea en funcion al codgo o la categoria
            self.cobrar_cliente(cod)
            if not self.llamar_sig_cliente(cod):
                self._masajistas[cod].set_estado(
                    self._estados_masajistas["L"])
                evento.set_prox_ev_none()
            else:
                evento.calcular_prox_ev(self._reloj)

    def inicializar_estados(self):
        estados_cliente = {}
        estados_masajistas = {}

        for name, handler, categoria in [
            ("Esperando M A", "E M A", "Esperando"),
            ("Esperando M B", "E M B", "Esperando"),
            ("Esperando M Ap", "E M Ap", "Esperando"),
            ("Atendido Por M A", "A M A", "Atendido"),
            ("Atendido Por M B", "A M B", "Atendido"),
            ("Atendido Por M Ap", "A M Ap", "Atendido")
        ]:
            estado = Estado(name, categoria)
            estados_cliente[handler] = estado

        for name, handler, categoria in [
            ("Ocupado", "O", "Masajista"),
            ("Libre", "L", "Masajista")
        ]:
            estado = Estado(name, categoria)
            estados_masajistas[handler] = estado

        return estados_cliente, estados_masajistas

    def inicializar_masajistas(self):
        masajistas = {}

        for name, handler in [
            ("Masajita A", "M A"),
            ("Masajita B", "M B"),
            ("Masajista Ap", "M Ap")
        ]:
            masajista = Masajista(name, self._estados_masajistas["L"])
            masajistas[handler] = masajista

        return masajistas

    def cod_masajista_disponible(self):
        for codigo in ["M A", "M B", "M Ap"]:
            if self._masajistas[codigo].estas(self._estados_masajistas["L"]):
                return codigo
        return ""

    def determinar_cant_clientes_vecs(self):
        return len(self._clientes["M A"]) + len(self._clientes["M B"]) + len(self._clientes["M Ap"])

    def cola_es_mayor(self, n):
        if len(self._clientes) > n:
            return True
        return False

    def nuevo_cliente(self, cod_masajista, ocupado, hora):
        for c in self._clientes[cod_masajista]:
            if c.esta_fuera_del_sistema():
                if ocupado:
                    c.reutilizar(
                        self._estados_cliente[f"E {cod_masajista}"], hora)
                else:
                    c.reutilizar(
                        self._estados_cliente[f"A {cod_masajista}"], hora)
                return
        if ocupado:
            nuevo_cliente = Cliente(
                self._estados_cliente[f"E {cod_masajista}"], hora)
        else:
            nuevo_cliente = Cliente(
                self._estados_cliente[f"A {cod_masajista}"], hora)

        self._clientes[cod_masajista].append(nuevo_cliente)

    # Aca voy a tener el estado literal del cliente
    def cobrar_cliente(self, codigo_masajista):
        acc_gasto = 0
        for c in self._clientes[codigo_masajista]:
            if (not c.esta_blanqueado()) and c.estas(self._estados_cliente[f"A {codigo_masajista}"]):
                if c.tiempo_espera_mayor_treinta():
                    acc_gasto += 1500

                acc_gasto += self._precio_masajistas[codigo_masajista]
                self._acc_recaudacion_diaria += acc_gasto
                c.blanquear()
                break

    def llamar_sig_cliente(self, codigo_masajista):
        for c in self._clientes[codigo_masajista]:
            if (not c.esta_blanqueado()) and c.estas(self._estados_cliente[f"E {codigo_masajista}"]):
                c.setEstado(
                    self._estados_cliente[f"A {codigo_masajista}"], self._reloj)
                return True
        return False

    def es_prox_ev_none(self, nombre_ev):
        for clave in self._eventos:
            if self._eventos[clave].es_tu_nombre(nombre_ev):
                return self._eventos[clave].es_prox_ev_none()

    def guardar(self, j):
        if self._reloj >= j:
            return True
        return False

    def determinar_prox_ev(self):
        prox_ev = None
        c_e = None
        for clave in self._eventos:
            if self._eventos[clave].get_prox_ev() is None:
                continue
            if prox_ev is None:
                prox_ev = self._eventos[clave].get_prox_ev()
                c_e = clave
            if self._eventos[clave].get_prox_ev() < prox_ev:
                prox_ev = self._eventos[clave].get_prox_ev()
                c_e = clave
        return self._eventos[c_e]

    def determinar_cant_cola(self):
        cant_cola = 0
        for clave in self._clientes:
            for c in self._clientes[clave]:
                if (not c.esta_blanqueado()) and c.haciendo_cola():
                    cant_cola += 1
        return cant_cola

    def crear_vector(self):
        vec = [str(self._reloj), self._evento_actual]
        for clave in self._eventos:
            vec.extend(self._eventos[clave].crear_vector())

        for clave in self._masajistas:
            vec.append(self._masajistas[clave].get_nombre_estado())

        vec.extend([str(self._cant_max_cola), str(self._acc_recaudacion_diaria), str(
            self._acc_recaudacion_total), str(self._cant_dias_simulados)])

        for clave in self._clientes:
            for c in self._clientes[clave]:
                vec.extend(c.crear_vector())
        return vec

    def finalizo(self):
        if self._cant_dias_simulados == self._dias_a_simular:
            return True
        return False

    def crear_reporte(self):
        if self._cant_dias_simulados > 0:
            recaudacion_promedio = self._acc_recaudacion_total / self._cant_dias_simulados
            reporte_recaudacion = f"La recaudación promedio daria del centro es de ${
                recaudacion_promedio} en {self._cant_dias_simulados} días simulados."
        else:
            recaudacion_promedio = self._acc_recaudacion_diaria
            reporte_recaudacion = f"La recaudación producida en menos de un dia es de ${
                recaudacion_promedio}."

        reporte = f"""
            <h3>Reporte</h3>
            <p>La cantidad mínima de sillas que debe haber para que ningún cliente esté de pie es de {self._cant_max_cola}.</p>
            <p>{reporte_recaudacion}</p>
            """
        return reporte
