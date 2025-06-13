
class Id():
    _instancia = None
    _nro = 1

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(Id, cls).__new__(cls)
        return cls._instancia

    def get_nro(self):
        nro = self.__class__._nro
        self.__class__._nro += 1
        return nro

    def reset(self):
        self.__class__._nro = 1
