import numpy as np
import time
import threading
from Controlador_Cache import *
from memoria_L1 import *
from Control_Inst import *
from memoria_L2 import *
from memoria_m import *

'''
instr1 = Control_Inst("P0", "read", 0, 0)
instr2 = Control_Inst("P1", "write", 0, 2)
instr3 = Control_Inst("P0", "read", 1, 0)
'''



p00_l1 = memoria_L1()
p01_l1 = memoria_L1()

p10_l1 = memoria_L1()
p11_l1 = memoria_L1()

p0_l2 = memoria_L2()

p1_l2 = memoria_L2()

memoriaP = memoria_m()



cont_cache = Controlador_Cache(p00_l1, p01_l1, p0_l2, p10_l1, p11_l1, p1_l2, memoriaP)

file = open("logFile.txt", "w")
file.close()

'''

cont_cache.add_instr(instr1)
cont_cache.add_instr(instr2)
cont_cache.add_instr(instr3)
'''

def gen_instr(proc_ident, l1_cache):
    s = np.random.poisson(2,6)

    ins_array = []

    instr = None

    hit = False

    for num in s:
        aux_num = num

        if(num == 0):
            aux_num = 1

        while(aux_num > 3):
            aux_num = aux_num - 3
        ins_array.append(aux_num)
    
    while(ins_array):
        mem_val = 0
        if(ins_array[0] == 1 or ins_array[0] == 3):
            s2 = np.random.poisson(16,1)
            while(s2[0] > 16):
                s2[0] = s2[0] - 16

            mem_val = s2[0]

        
        if(ins_array[0] == 1):
            instr = Control_Inst(proc_ident, "read", mem_val, 1)
        if(ins_array[0] == 2):
            instr = Control_Inst(proc_ident, "calc", mem_val, 0)
        if(ins_array[0] == 3):
            data = random.randint(0, 65535)
            instr = Control_Inst(proc_ident, "write", mem_val, data)
       
        cont_cache.add_instr(instr)
        ins_array.pop(0)

        time.sleep(1)

x1 = threading.Thread(target=gen_instr, args=("P0:0", p00_l1), daemon=True)

x2 = threading.Thread(target=gen_instr, args=("P0:1", p01_l1), daemon=True)

x3 = threading.Thread(target=gen_instr, args=("P1:0", p10_l1), daemon=True)

x4 = threading.Thread(target=gen_instr, args=("P1:1", p11_l1), daemon=True)

x1.start()

x2.start()

x3.start()

x4.start()


'''

instr1 = Control_Inst("P0:0", "read", 1, 99)
instr2 = Control_Inst("P0:0", "read", 2, 1)
instr3 = Control_Inst("P0:1", "read", 3, 99)
instr4 = Control_Inst("P0:1", "read", 4, 69)
instr5 = Control_Inst("P1:0", "read", 5, 69)
instr6 = Control_Inst("P1:0", "read", 6, 69)
instr7 = Control_Inst("P1:1", "read", 7, 42)
instr8 = Control_Inst("P1:1", "read", 8, 24)
cont_cache.add_instr(instr1)
cont_cache.add_instr(instr2)
cont_cache.add_instr(instr3)
cont_cache.add_instr(instr4)
cont_cache.add_instr(instr5)
cont_cache.add_instr(instr6)
cont_cache.add_instr(instr7)
cont_cache.add_instr(instr8)

'''

while(True):
    if(not cont_cache.state_instr):
        pass
    else:
        print(cont_cache.state_instr[0])
        file = open("logFile.txt", "a+")
        file.write("Ins: " + str(cont_cache.state_instr[0]) + "\n")
        file.close()
        if(cont_cache.state_instr[0].instr_type == "read"):
            cont_cache.read_mem(cont_cache.state_instr[0].mem_addr, cont_cache.state_instr[0].proc_orig)
        elif(cont_cache.state_instr[0].instr_type == "write"):
            cont_cache.write_mem(cont_cache.state_instr[0].mem_addr, cont_cache.state_instr[0].proc_orig, cont_cache.state_instr[0].data)
        cont_cache.state_instr.pop(0)
        print("P0:0")
        p00_l1.print_mem()
        print("P0:1")
        p01_l1.print_mem()
        print("P0:L2")
        p0_l2.print_mem()
        print("P1:0")
        p10_l1.print_mem()
        print("P1:1")
        p11_l1.print_mem()
        print("P1:L2")
        p1_l2.print_mem()
        print("Mem")
        memoriaP.print_mem()