from Bloque_L1 import *
from prettytable import PrettyTable
class memoria_L1:
    mem_blocks = None
    t = None
   
    def __init__(self):
       self.mem_blocks = []
    
       block1 = Bloque_L1()

       self.mem_blocks.append(block1)

       block2 = Bloque_L1()
       self.mem_blocks.append(block2)


       
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

    def print_mem(self):
        t = PrettyTable(['Estado de Coherencia', 'Direccion de Memoria', 'Dato'])
        for i in self.mem_blocks:
            t.add_row([i.estado_coherencia, i.direcc_memoria, i.dato])
        print(t)


    
