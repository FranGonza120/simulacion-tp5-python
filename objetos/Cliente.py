from objetos.Id import Id


class Cliente():
    def __init__(self, estado, hora_llegada):
        self._id = Id().get_nro()
        self._estado = estado
        self._hora_llegada = hora_llegada
        self._tiempo_espera = 0

    def setEstado(self, estado, hora):
        self.calcular_tiempo_espera(estado, hora)
        self._estado = estado

    def asignar_id():
        return 1

    def calcular_tiempo_espera(self, estado, hora):
        if estado.sos_categoria("Atendido"):
            self._tiempo_espera = round(hora - self._hora_llegada, 4)

    def estas(self, estado):
        if self._estado.sos_este(estado):
            return True
        return False

    def tiempo_espera_mayor_treinta(self):
        if self._tiempo_espera > 30:
            return True
        return False

    def esta_fuera_del_sistema(self):
        if self._hora_llegada == None:
            return True
        return False

    def reutilizar(self, estado, hora):
        self._id = Id().get_nro()
        self._estado = estado
        self._hora_llegada = hora

    def blanquear(self):
        self._id = None
        self._hora_llegada = None
        self._tiempo_espera = 0
        self._estado = None

    def haciendo_cola(self):
        return self._estado.sos_categoria("Esperando")

    def crear_vector(self):
        if self._id is None:
            return ["", "", "", ""]
        else:
            return [str(self._id), self._estado.get_nombre(), str(self._hora_llegada), str(self._tiempo_espera)]

    def esta_blanqueado(self):
        if self._id is None:
            return True
        return False

    def get_hora_llegada(self):
        return self._hora_llegada