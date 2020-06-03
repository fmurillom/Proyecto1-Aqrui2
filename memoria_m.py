from Bloque_mem import *
from prettytable import PrettyTable

class memoria_m:
    mem_blocks = None
   
    def __init__(self):
       self.mem_blocks = []

       for i in range(0, 17):
           block = Bloque_mem()
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
        return self.mem_blocks[direc_mem]
    def set_dueno(self, direc_mem, dueno):
        block = self.search_block(direc_mem)
        if(block != None):
            block.dueno.append(dueno)
    def elim_dueno(self, direc_mem, dueno):
        block = self.search_block(direc_mem)
        if(block != None):
            block.dueno.remove(dueno)

    def print_mem(self):
        t = PrettyTable(['Estado de Coherencia', 'Dueno', 'Dato'])
        for i in self.mem_blocks:
            duenos = ""
            for j in i.dueno:
                duenos += j + " "
            t.add_row([i.estado_coherencia, duenos, i.dato])
        print(t)



    
