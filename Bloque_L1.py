class Bloque_L1:
    estado_coherencia = "I"
    direcc_memoria = 0
    dato = 0

    def __init__(self, estado_coherencia, direcc_memoria, dato):
        self.estado_coherencia = estado_coherencia
        self.direcc_memoria = direcc_memoria
        self.dato = dato

    def __init__(self):
        self.estado_coherencia = "I"
        self.direcc_memoria = 0000
        self.dato = 0000

    def set_coherencia(self, estado_c):
        self.estado_coherencia = estado_c

    def set_direcMem(self, address):
        self.direcc_memoria = address

    def set_dato(self, data):
        self.dato = data

    def get_coherencia(self):
        return self.estado_coherencia
    
    def get_direcc_memoria(self):
        return self.direcc_memoria

    def get_dato(self):
        return self.dato