from Bloque_L2 import *
from prettytable import PrettyTable

class memoria_L2:
    mem_blocks = None
   
    def __init__(self):

       self.mem_blocks = []

       for i in range(0, 4):
           block = Bloque_L2()
           self.mem_blocks.append(block)
       
    def set_block(self, state_coher, direc_mem, data, block_num):
        if(block_num == 1):
            self.mem_blocks[0].set_coherencia(state_coher)
            self.mem_blocks[0].set_direcMem(direc_mem)
            self.mem_blocks[0].set_dato(data)

        if(block_num == 2):
            self.mem_blocks[1].set_coherencia(state_coher)
            self.mem_blocks[1].set_direcMem(direc_mem)
            self.mem_blocks[1].set_dato(data)
    
    def search_block(self, direc_mem):
        for block in self.mem_blocks:
            if(block.get_direcc_memoria() == direc_mem and block.get_coherencia() != "I"):
                return block
        return None

    def set_dueno(self, direc_mem, dueno):
        block = self.search_block(direc_mem)
        if(block != None):
            block.dueno.append(dueno)
    def elim_dueno(self, direc_mem, dueno):
        block = self.search_block(direc_mem)
        if(block != None):
            block.dueno.remove(dueno)

    def print_mem(self):
        t = PrettyTable(['Estado de Coherencia', 'Dueno', 'Direccion de Memoria', 'Dato'])
        for i in self.mem_blocks:
            duenos = ""
            for j in i.dueno:
                duenos += j + " "
            t.add_row([i.estado_coherencia, duenos, i.direcc_memoria, i.dato])
        print(t)



    
