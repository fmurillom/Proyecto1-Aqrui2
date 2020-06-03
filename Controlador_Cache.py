from memoria_L1 import *
import random

class Controlador_Cache:
    cache_P0 = None
    cache_P1 = None
    cache_L2 = None
    cache_P10 = None
    cache_P11 = None
    cache_L2P1 = None
    state_instr = []
    mem_p = None

    def __init__(self, cache_P0, cache_P1, cache_L2, cache_P10, cache_P11, cache_L2P1, mem_p):
        self.cache_P0 = cache_P0
        self.cache_P1 = cache_P1
        self.cache_L2 = cache_L2
        self.cache_P10 = cache_P10
        self.cache_P11 = cache_P11
        self.cache_L2P1 = cache_L2P1
        
        self.mem_p = mem_p

    def add_instr(self, instr):
        self.state_instr.append(instr)
    
    def read_mem(self, direc_mem, proc_orig):
        file = open("logFile.txt", "a+")
        if(proc_orig == "P0:0"):
            if(self.cache_P0.mem_blocks[0].get_coherencia() != "I" and self.cache_P0.mem_blocks[1].get_coherencia() != "I"):
                swap_block = random.randint(0,1)

                self.mem_p.search_block(self.cache_P0.mem_blocks[swap_block].get_direcc_memoria()).set_dato(self.cache_P0.mem_blocks[swap_block].get_dato())

                self.cache_P0.mem_blocks[swap_block].set_direcMem(direc_mem)

                file.write("Swapping block %d of P0:0 L1, writing value %d into memory block %d\n" % (swap_block, self.cache_P0.mem_blocks[swap_block].get_dato(), self.cache_P0.mem_blocks[swap_block].get_direcc_memoria()))

                self.cache_P0.mem_blocks[swap_block].set_dato(self.mem_p.mem_blocks[direc_mem].dato)
                self.cache_P0.mem_blocks[swap_block].set_coherencia("M")

                block_shared = self.cache_P1.search_block(direc_mem)

                if(block_shared != None):
                    self.cache_P0.mem_blocks[swap_block].set_dato(block_shared.get_dato())
                    file.write("Reading shared block %d from P0:1 with data %d\n" % (direc_mem, block_shared.get_dato()))
                elif(self.cache_P10.search_block(direc_mem) != None):
                    block_shared = self.cache_P10.search_block(direc_mem)
                    self.cache_P0.mem_blocks[swap_block].set_dato(block_shared.get_dato())
                    file.write("Reading shared block %d from P1:0 with data %d\n" % (direc_mem, block_shared.get_dato()))
                elif(self.cache_P11.search_block(direc_mem) != None):
                    block_shared = self.cache_P11.search_block(direc_mem)
                    self.cache_P0.mem_blocks[swap_block].set_dato(block_shared.get_dato())
                    file.write("Reading shared block %d from P1:1 with data %d\n" % (direc_mem, block_shared.get_dato()))
                else:
                    file.write("Reading block %d from Memory with data %d\n" % (direc_mem, self.mem_p.mem_blocks[direc_mem].dato))

                self.copyBLock(self.cache_P0.mem_blocks[swap_block], self.cache_L2.mem_blocks[swap_block])


            else:
                block_invalid = None
                for block in self.cache_P0.mem_blocks:
                    if(block.get_coherencia() == "I"):
                        block_invalid = block
                        break
                block_invalid.set_dato(self.mem_p.mem_blocks[direc_mem].dato)
                block_invalid.set_direcMem(direc_mem)
                block_invalid.set_coherencia("M")

                block_index = self.cache_P0.mem_blocks.index(block_invalid)

                block_shared = self.cache_P1.search_block(direc_mem)

                if(block_shared != None):
                    self.cache_P0.mem_blocks[block_index].set_dato(block_shared.get_dato())
                    file.write("Reading shared block %d from P0:1 with data %d\n" % (direc_mem, block_shared.get_dato()))
                elif(self.cache_P10.search_block(direc_mem) != None):
                    block_shared = self.cache_P10.search_block(direc_mem)
                    self.cache_P0.mem_blocks[block_index].set_dato(block_shared.get_dato())
                    file.write("Reading shared block %d from P1:0 with data %d\n" % (direc_mem, block_shared.get_dato()))
                elif(self.cache_P11.search_block(direc_mem) != None):
                    block_shared = self.cache_P11.search_block(direc_mem)
                    self.cache_P0.mem_blocks[block_index].set_dato(block_shared.get_dato())
                    file.write("Reading shared block %d from P1:1 with data %d\n" % (direc_mem, block_shared.get_dato()))
                else:
                    file.write("Reading block %d from Memory with data %d\n" % (direc_mem, self.mem_p.mem_blocks[direc_mem].dato))

                self.copyBLock(block_invalid, self.cache_L2.mem_blocks[block_index])


        elif(proc_orig == "P0:1"):
            if(self.cache_P1.mem_blocks[0].get_coherencia() != "I" and self.cache_P1.mem_blocks[1].get_coherencia() != "I"):
                swap_block = random.randint(0,1)

                self.mem_p.search_block(self.cache_P1.mem_blocks[swap_block].get_direcc_memoria()).set_dato(self.cache_P1.mem_blocks[swap_block].get_dato())

                file.write("Swapping block %d of P0:1 L1, writing value %d into memory block %d\n" % (swap_block, self.cache_P1.mem_blocks[swap_block].get_dato(), self.cache_P1.mem_blocks[swap_block].get_direcc_memoria()))

                self.cache_P1.mem_blocks[swap_block].set_direcMem(direc_mem)
                self.cache_P1.mem_blocks[swap_block].set_dato(self.mem_p.mem_blocks[direc_mem].dato)
                self.cache_P1.mem_blocks[swap_block].set_coherencia("M")

                block_shared = self.cache_P0.search_block(direc_mem)

                if(block_shared != None):
                    self.cache_P1.mem_blocks[swap_block].set_dato(block_shared.get_dato())
                    file.write("Reading shared block %d from P0:0 with data %d\n" % (direc_mem, block_shared.get_dato()))
                elif(self.cache_P10.search_block(direc_mem) != None):
                    block_shared = self.cache_P10.search_block(direc_mem)
                    self.cache_P1.mem_blocks[swap_block].set_dato(block_shared.get_dato())
                    file.write("Reading shared block %d from P1:0 with data %d\n" % (direc_mem, block_shared.get_dato()))
                elif(self.cache_P11.search_block(direc_mem) != None):
                    block_shared = self.cache_P11.search_block(direc_mem)
                    self.cache_P1.mem_blocks[swap_block].set_dato(block_shared.get_dato())
                    file.write("Reading shared block %d from P1:1 with data %d\n" % (direc_mem, block_shared.get_dato()))
                else:
                    file.write("Reading block %d from Memory with data %d\n" % (direc_mem, self.mem_p.mem_blocks[direc_mem].dato))

                self.copyBLock(self.cache_P1.mem_blocks[swap_block], self.cache_L2.mem_blocks[swap_block + 2])

            else:
                block_invalid = None
                for block in self.cache_P1.mem_blocks:
                    if(block.get_coherencia() == "I"):
                        block_invalid = block
                        break
                block_invalid.set_dato(self.mem_p.mem_blocks[direc_mem].dato)
                block_invalid.set_direcMem(direc_mem)
                block_invalid.set_coherencia("M")
                block_index = self.cache_P1.mem_blocks.index(block_invalid)

                block_shared = self.cache_P0.search_block(direc_mem)

                if(block_shared != None):
                    self.cache_P1.mem_blocks[block_index].set_dato(block_shared.get_dato())
                    file.write("Reading shared block %d from P0:0 with data %d\n" % (direc_mem, block_shared.get_dato()))
                elif(self.cache_P10.search_block(direc_mem) != None):
                    block_shared = self.cache_P10.search_block(direc_mem)
                    self.cache_P1.mem_blocks[block_index].set_dato(block_shared.get_dato())
                    file.write("Reading shared block %d from P1:0 with data %d\n" % (direc_mem, block_shared.get_dato()))
                elif(self.cache_P11.search_block(direc_mem) != None):
                    block_shared = self.cache_P11.search_block(direc_mem)
                    self.cache_P1.mem_blocks[block_index].set_dato(block_shared.get_dato())
                    file.write("Reading shared block %d from P1:1 with data %d\n" % (direc_mem, block_shared.get_dato()))
                else:
                    file.write("Reading block %d from Memory with data %d\n" % (direc_mem, self.mem_p.mem_blocks[direc_mem].dato))
                self.copyBLock(block_invalid, self.cache_L2.mem_blocks[block_index + 2])

        elif(proc_orig == "P1:0"):
            if(self.cache_P10.mem_blocks[0].get_coherencia() != "I" and self.cache_P10.mem_blocks[1].get_coherencia() != "I"):
                swap_block = random.randint(0,1)

                self.mem_p.search_block(self.cache_P10.mem_blocks[swap_block].get_direcc_memoria()).set_dato(self.cache_P10.mem_blocks[swap_block].get_dato())

                self.cache_P10.mem_blocks[swap_block].set_direcMem(direc_mem)

                file.write("Swapping block %d of P1:0 L1, writing value %d into memory block %d\n" % (swap_block, self.cache_P10.mem_blocks[swap_block].get_dato(), self.cache_P10.mem_blocks[swap_block].get_direcc_memoria()))

                self.cache_P10.mem_blocks[swap_block].set_dato(self.mem_p.mem_blocks[direc_mem].dato)
                self.cache_P10.mem_blocks[swap_block].set_coherencia("M")

                block_shared = self.cache_P0.search_block(direc_mem)

                if(block_shared != None):
                    self.cache_P10.mem_blocks[swap_block].set_dato(block_shared.get_dato())
                    file.write("Reading shared block %d from P0:0 with data %d\n" % (direc_mem, block_shared.get_dato()))
                elif(self.cache_P1.search_block(direc_mem) != None):
                    block_shared = self.cache_P1.search_block(direc_mem)
                    self.cache_P10.mem_blocks[swap_block].set_dato(block_shared.get_dato())
                    file.write("Reading shared block %d from P0:1 with data %d\n" % (direc_mem, block_shared.get_dato()))
                elif(self.cache_P11.search_block(direc_mem) != None):
                    block_shared = self.cache_P11.search_block(direc_mem)
                    self.cache_P10.mem_blocks[swap_block].set_dato(block_shared.get_dato())
                    file.write("Reading shared block %d from P1:1 with data %d\n" % (direc_mem, block_shared.get_dato()))
                else:
                    file.write("Reading block %d from Memory with data %d\n" % (direc_mem, self.mem_p.mem_blocks[direc_mem].dato))

                self.copyBLock(self.cache_P10.mem_blocks[swap_block], self.cache_L2P1.mem_blocks[swap_block])


            else:
                block_invalid = None
                for block in self.cache_P10.mem_blocks:
                    if(block.get_coherencia() == "I"):
                        block_invalid = block
                        break
                block_invalid.set_dato(self.mem_p.mem_blocks[direc_mem].dato)
                block_invalid.set_direcMem(direc_mem)
                block_invalid.set_coherencia("M")

                block_index = self.cache_P10.mem_blocks.index(block_invalid)

                block_shared = self.cache_P0.search_block(direc_mem)

                if(block_shared != None):
                    self.cache_P10.mem_blocks[block_index].set_dato(block_shared.get_dato())
                    file.write("Reading shared block %d from P0:0 with data %d\n" % (direc_mem, block_shared.get_dato()))
                elif(self.cache_P1.search_block(direc_mem) != None):
                    block_shared = self.cache_P1.search_block(direc_mem)
                    self.cache_P10.mem_blocks[block_index].set_dato(block_shared.get_dato())
                    file.write("Reading shared block %d from P0:1 with data %d\n" % (direc_mem, block_shared.get_dato()))
                elif(self.cache_P11.search_block(direc_mem) != None):
                    block_shared = self.cache_P11.search_block(direc_mem)
                    self.cache_P10.mem_blocks[block_index].set_dato(block_shared.get_dato())
                    file.write("Reading shared block %d from P1:1 with data %d\n" % (direc_mem, block_shared.get_dato()))
                else:
                    file.write("Reading block %d from Memory with data %d\n" % (direc_mem, self.mem_p.mem_blocks[direc_mem].dato))

                self.copyBLock(block_invalid, self.cache_L2P1.mem_blocks[block_index])

        elif(proc_orig == "P1:1"):
            if(self.cache_P11.mem_blocks[0].get_coherencia() != "I" and self.cache_P11.mem_blocks[1].get_coherencia() != "I"):
                swap_block = random.randint(0,1)

                self.mem_p.search_block(self.cache_P11.mem_blocks[swap_block].get_direcc_memoria()).set_dato(self.cache_P11.mem_blocks[swap_block].get_dato())

                self.cache_P11.mem_blocks[swap_block].set_direcMem(direc_mem)

                file.write("Swapping block %d of P1:1 L1, writing value %d into memory block %d\n" % (swap_block, self.cache_P11.mem_blocks[swap_block].get_dato(), self.cache_P11.mem_blocks[swap_block].get_direcc_memoria()))

                self.cache_P11.mem_blocks[swap_block].set_dato(self.mem_p.mem_blocks[direc_mem].dato)
                self.cache_P11.mem_blocks[swap_block].set_coherencia("M")

                block_shared = self.cache_P0.search_block(direc_mem)

                if(block_shared != None):
                    self.cache_P11.mem_blocks[swap_block].set_dato(block_shared.get_dato())
                    file.write("Reading shared block %d from P0:0 with data %d\n" % (direc_mem, block_shared.get_dato()))
                elif(self.cache_P1.search_block(direc_mem) != None):
                    block_shared = self.cache_P1.search_block(direc_mem)
                    self.cache_P11.mem_blocks[swap_block].set_dato(block_shared.get_dato())
                    file.write("Reading shared block %d from P0:1 with data %d\n" % (direc_mem, block_shared.get_dato()))
                elif(self.cache_P10.search_block(direc_mem) != None):
                    block_shared = self.cache_P10.search_block(direc_mem)
                    self.cache_P10.mem_blocks[swap_block].set_dato(block_shared.get_dato())
                    file.write("Reading shared block %d from P1:0 with data %d\n" % (direc_mem, block_shared.get_dato()))
                else:
                    file.write("Reading block %d from Memory with data %d\n" % (direc_mem, self.mem_p.mem_blocks[direc_mem].dato))

                self.copyBLock(self.cache_P11.mem_blocks[swap_block], self.cache_L2P1.mem_blocks[swap_block + 2])


            else:
                block_invalid = None
                for block in self.cache_P11.mem_blocks:
                    if(block.get_coherencia() == "I"):
                        block_invalid = block
                        break
                block_invalid.set_dato(self.mem_p.mem_blocks[direc_mem].dato)
                block_invalid.set_direcMem(direc_mem)
                block_invalid.set_coherencia("M")

                block_index = self.cache_P11.mem_blocks.index(block_invalid)

                block_shared = self.cache_P0.search_block(direc_mem)

                if(block_shared != None):
                    self.cache_P11.mem_blocks[block_index].set_dato(block_shared.get_dato())
                    file.write("Reading shared block %d from P0:0 with data %d\n" % (direc_mem, block_shared.get_dato()))
                elif(self.cache_P1.search_block(direc_mem) != None):
                    block_shared = self.cache_P1.search_block(direc_mem)
                    self.cache_P11.mem_blocks[block_index].set_dato(block_shared.get_dato())
                    file.write("Reading shared block %d from P0:1 with data %d\n" % (direc_mem, block_shared.get_dato()))
                elif(self.cache_P10.search_block(direc_mem) != None):
                    block_shared = self.cache_P10.search_block(direc_mem)
                    self.cache_P11.mem_blocks[block_index].set_dato(block_shared.get_dato())
                    file.write("Reading shared block %d from P1:0 with data %d\n" % (direc_mem, block_shared.get_dato()))
                else:
                    file.write("Reading block %d from Memory with data %d\n" % (direc_mem, self.mem_p.mem_blocks[direc_mem].dato))

                self.copyBLock(block_invalid, self.cache_L2P1.mem_blocks[block_index + 2])


        file.close()
        self.checkL2()
        self.checkL2P1()
        self.check_Mem()

    def write_mem(self, direc_mem, proc_orig, data):
        if(proc_orig == "P0:0" or proc_orig == "P0:1"):
            self.write_memP0(direc_mem, proc_orig, data)
        else:
            self.write_memP1(direc_mem, proc_orig, data)
    
    def write_memP0(self, direc_mem, proc_orig, data):
        file = open("logFile.txt", "a+")
        block_L2 = self.cache_L2.search_block(direc_mem)
        if(block_L2 != None and block_L2.get_coherencia() != "I"):
            if(block_L2.get_coherencia() == "S"):
                if(proc_orig == "P0:0"):

                    if(self.cache_P0.search_block(direc_mem) == None):
                        self.read_mem(direc_mem, proc_orig)

                    self.cache_P0.search_block(direc_mem).set_dato(data)
                    self.cache_P0.search_block(direc_mem).set_coherencia("M")
                    file.write("Writing %d value into shared block %d on P0:0 L1\n" % (data, direc_mem))
                    shared = self.cache_P1.search_block(direc_mem)
                    if(shared != None):
                        shared.set_coherencia("I")
                        file.write("Invalidating shared block %d on P0:1 L1\n" % (direc_mem))
                    shared = self.cache_P10.search_block(direc_mem)
                    if(shared != None):
                        shared.set_coherencia("I")
                        file.write("Invalidating shared block %d on P1:0 L1\n" % (direc_mem))
                    shared = self.cache_P11.search_block(direc_mem)
                    if(shared != None):
                        shared.set_coherencia("I")
                        file.write("Invalidating shared block %d on P1:1 L1\n" % (direc_mem))
                    self.cache_L2.search_block(direc_mem).set_dato(data)
                    file.write("Updating %d on P0 L2\n" % (direc_mem))
                if(proc_orig == "P0:1"):


                    if(self.cache_P1.search_block(direc_mem) == None):
                        self.read_mem(direc_mem, proc_orig)

                    self.cache_P1.search_block(direc_mem).set_dato(data)
                    self.cache_P1.search_block(direc_mem).set_coherencia("M")
                    file.write("Writing %d value into shared block %d on P0:1 L1\n" % (data, direc_mem))
                    shared = self.cache_P0.search_block(direc_mem)
                    if(shared != None):
                        shared.set_coherencia("I")
                        file.write("Invalidating shared block %d on P0:0 L1\n" % (direc_mem))
                    shared = self.cache_P10.search_block(direc_mem)
                    if(shared != None):
                        shared.set_coherencia("I")
                        file.write("Invalidating shared block %d on P1:0 L1\n" % (direc_mem))
                    shared = self.cache_P11.search_block(direc_mem)
                    if(shared != None):
                        shared.set_coherencia("I")
                        file.write("Invalidating shared block %d on P1:1 L1\n" % (direc_mem))
                    self.cache_L2.search_block(direc_mem).set_dato(data)
                    file.write("Updating %d on P0 L2\n" % (direc_mem))
            else:
                if(proc_orig == "P0:0"):

                    if(self.cache_P0.search_block(direc_mem) == None):
                        self.read_mem(direc_mem, proc_orig)

                    self.cache_P0.search_block(direc_mem).set_dato(data)
                    self.cache_P0.search_block(direc_mem).set_coherencia("M")
                    file.write("Writing %d value into block %d on P0:0 L1\n" % (data, direc_mem))
                    self.cache_L2.search_block(direc_mem).set_dato(data)
                    file.write("Updating %d on P0 L2\n" % (direc_mem))
                if(proc_orig == "P0:1"):

                    if(self.cache_P1.search_block(direc_mem) == None):
                        self.read_mem(direc_mem, proc_orig)

                    self.cache_P1.search_block(direc_mem).set_dato(data)
                    self.cache_P1.search_block(direc_mem).set_coherencia("M")
                    file.write("Writing %d value into block %d on P0:1 L1\n" % (data, direc_mem))
                    self.cache_L2.search_block(direc_mem).set_dato(data)
                    file.write("Updating %d on P0 L2\n" % (direc_mem))
        else:
            file.close()
            self.read_mem(direc_mem, proc_orig)
            file = open("logFile.txt", "a+")
            file.write("Write Miss detected for %d address in %s\n" % (direc_mem, proc_orig))
            file.close()
            self.write_memP0(direc_mem, proc_orig, data)

        self.checkL2()
        self.checkL2P1()
        self.check_Mem()
        file.close()
    
    def write_memP1(self, direc_mem, proc_orig, data):
        file = open("logFile.txt", "a+")
        block_L2 = self.cache_L2P1.search_block(direc_mem)

        if(block_L2 != None and block_L2.get_coherencia() != "I"):
            if(block_L2.get_coherencia() == "S"):
                if(proc_orig == "P1:0"):


                    if(self.cache_P10.search_block(direc_mem) == None):
                        self.read_mem(direc_mem, proc_orig)

                    self.cache_P10.search_block(direc_mem).set_dato(data)
                    self.cache_P10.search_block(direc_mem).set_coherencia("M")
                    file.write("Writing %d value into shared block %d on P1:0 L1\n" % (data, direc_mem))
                    shared = self.cache_P0.search_block(direc_mem)
                    if(shared != None):
                        shared.set_coherencia("I")
                        file.write("Invalidating shared block %d on P0:0 L1\n" % (direc_mem))
                    shared = self.cache_P1.search_block(direc_mem)
                    if(shared != None):
                        shared.set_coherencia("I")
                        file.write("Invalidating shared block %d on P1:1 L1\n" % (direc_mem))
                    shared = self.cache_P11.search_block(direc_mem)
                    if(shared != None):
                        shared.set_coherencia("I")
                        file.write("Invalidating shared block %d on P1:1 L1\n" % (direc_mem))
                    self.cache_L2P1.search_block(direc_mem).set_dato(data)
                    file.write("Updating %d on P1 L2\n" % (direc_mem))
                if(proc_orig == "P1:1"):

                    if(self.cache_P11.search_block(direc_mem) == None):
                        self.read_mem(direc_mem, proc_orig)

                    self.cache_P11.search_block(direc_mem).set_dato(data)
                    self.cache_P11.search_block(direc_mem).set_coherencia("M")
                    file.write("Writing %d value into shared block %d on P1:1 L1\n" % (data, direc_mem))
                    shared = self.cache_P0.search_block(direc_mem)
                    if(shared != None):
                        shared.set_coherencia("I")
                        file.write("Invalidating shared block %d on P0:0 L1\n" % (direc_mem))
                    shared = self.cache_P1.search_block(direc_mem)
                    if(shared != None):
                        shared.set_coherencia("I")
                        file.write("Invalidating shared block %d on P0:1 L1\n" % (direc_mem))
                    shared = self.cache_P10.search_block(direc_mem)
                    if(shared != None):
                        shared.set_coherencia("I")
                        file.write("Invalidating shared block %d on P1:0 L1\n" % (direc_mem))
                    self.cache_L2P1.search_block(direc_mem).set_dato(data)
                    file.write("Updating %d on P1 L2\n" % (direc_mem))
            else:
                if(proc_orig == "P1:0"):

                    if(self.cache_P10.search_block(direc_mem) == None):
                        self.read_mem(direc_mem, proc_orig)

                    self.cache_P10.search_block(direc_mem).set_dato(data)
                    self.cache_P10.search_block(direc_mem).set_coherencia("M")
                    file.write("Writing %d value into block %d on P1:0 L1\n" % (data, direc_mem))
                    self.cache_L2P1.search_block(direc_mem).set_dato(data)
                    file.write("Updating %d on P1 L2\n" % (direc_mem))
                if(proc_orig == "P1:1"):

                    if(self.cache_P11.search_block(direc_mem) == None):
                        self.read_mem(direc_mem, proc_orig)

                    self.cache_P11.search_block(direc_mem).set_dato(data)
                    self.cache_P11.search_block(direc_mem).set_coherencia("M")
                    file.write("Writing %d value into block %d on P1:1 L1\n" % (data, direc_mem))
                    self.cache_L2P1.search_block(direc_mem).set_dato(data)
                    file.write("Updating %d on P1 L2\n" % (direc_mem))
        else:
            file.close()
            self.read_mem(direc_mem, proc_orig)
            file = open("logFile.txt", "a+")
            file.write("Write Miss detected for %d address in %s\n" % (direc_mem, proc_orig))
            file.close()
            self.write_memP1(direc_mem, proc_orig, data)

        self.checkL2()
        self.checkL2P1()
        self.check_Mem()
        file.close()


    def copyBLock(self, block1, block2):
        block2.set_direcMem(block1.get_direcc_memoria())
        block2.set_dato(block1.get_dato())
        block2.set_coherencia(block1.get_coherencia())

    def checkL2(self):
        file = open("logFile.txt", "a+")
        shared_blocks = []
        checked_blocks = []

        for block_L2 in self.cache_L2.mem_blocks:
            block_L2.set_coherencia("I")


        for block_L2 in self.cache_L2.mem_blocks:
            block_aux0 = self.cache_P0.search_block(block_L2.direcc_memoria)
            block_aux1 = self.cache_P1.search_block(block_L2.direcc_memoria)
            block_aux10 = self.cache_P10.search_block(block_L2.direcc_memoria)
            block_aux11 = self.cache_P11.search_block(block_L2.direcc_memoria)

            if(block_aux0 != None and block_aux1 != None and block_aux10 != None and block_aux11 != None and shared_blocks.count(block_L2.direcc_memoria) == 0):
                block_L2.set_coherencia("S")
                block_L2.dueno.clear()
                block_L2.dueno.append("P0:0")
                block_L2.dueno.append("P0:1")
                block_L2.dueno.append("P1:0")
                block_L2.dueno.append("P1:1")
                shared_blocks.append(block_L2.direcc_memoria)
                checked_blocks.append(block_L2.direcc_memoria)
                block_aux0.set_coherencia("S")
                block_aux1.set_coherencia("S")
                block_aux10.set_coherencia("S")
                block_aux11.set_coherencia("S")
                file.write("Setting %d adress as shared on P0:0, P0:1, P1:0, P1:1\n" % (block_L2.direcc_memoria))

            elif(block_aux0 != None and block_aux10 != None and block_aux11 != None and shared_blocks.count(block_L2.direcc_memoria) == 0):
                block_L2.set_coherencia("S")
                block_L2.dueno.clear()
                block_L2.dueno.append("P0:0")
                block_L2.dueno.append("P1:0")
                block_L2.dueno.append("P1:1")
                shared_blocks.append(block_L2.direcc_memoria)
                checked_blocks.append(block_L2.direcc_memoria)
                block_aux0.set_coherencia("S")
                block_aux10.set_coherencia("S")
                block_aux11.set_coherencia("S")
                file.write("Setting %d adress as shared on P0:0, P1:0, P1:1\n" % (block_L2.direcc_memoria))

            elif(block_aux0 != None and block_aux10 != None and shared_blocks.count(block_L2.direcc_memoria) == 0):
                block_L2.set_coherencia("S")
                block_L2.dueno.clear()
                block_L2.dueno.append("P0:0")
                block_L2.dueno.append("P1:0")
                shared_blocks.append(block_L2.direcc_memoria)
                checked_blocks.append(block_L2.direcc_memoria)
                block_aux0.set_coherencia("S")
                block_aux10.set_coherencia("S")
                file.write("Setting %d adress as shared on P0:0, and P1:0\n" % (block_L2.direcc_memoria))

            elif(block_aux0 != None and block_aux11 != None and shared_blocks.count(block_L2.direcc_memoria) == 0):
                block_L2.set_coherencia("S")
                block_L2.dueno.clear()
                block_L2.dueno.append("P0:0")
                block_L2.dueno.append("P1:1")
                shared_blocks.append(block_L2.direcc_memoria)
                checked_blocks.append(block_L2.direcc_memoria)
                block_aux0.set_coherencia("S")
                block_aux11.set_coherencia("S")
                file.write("Setting %d adress as shared on P0:0 and P1:1\n" % (block_L2.direcc_memoria))


            elif(block_aux0 != None and block_aux1 != None and shared_blocks.count(block_L2.direcc_memoria) == 0):
                block_L2.set_coherencia("S")
                block_L2.dueno.clear()
                block_L2.dueno.append("P0:0")
                block_L2.dueno.append("P0:1")
                shared_blocks.append(block_L2.direcc_memoria)
                checked_blocks.append(block_L2.direcc_memoria)
                block_aux0.set_coherencia("S")
                block_aux1.set_coherencia("S")
                file.write("Setting %d adress as shared on P0:0 and P0:1\n" % (block_L2.direcc_memoria))
            
            elif(block_aux1 != None and block_aux10 != None and block_aux11 != None and shared_blocks.count(block_L2.direcc_memoria) == 0):
                block_L2.set_coherencia("S")
                block_L2.dueno.clear()
                block_L2.dueno.append("P0:1")
                block_L2.dueno.append("P1:0")
                block_L2.dueno.append("P1:1")
                shared_blocks.append(block_L2.direcc_memoria)
                checked_blocks.append(block_L2.direcc_memoria)
                block_aux1.set_coherencia("S")
                block_aux10.set_coherencia("S")
                block_aux11.set_coherencia("S")
                file.write("Setting %d adress as shared on P0:1, P1:0, P1:1\n" % (block_L2.direcc_memoria))

            elif(block_aux1 != None and block_aux10 != None and shared_blocks.count(block_L2.direcc_memoria) == 0):
                block_L2.set_coherencia("S")
                block_L2.dueno.clear()
                block_L2.dueno.append("P0:1")
                block_L2.dueno.append("P1:0")
                shared_blocks.append(block_L2.direcc_memoria)
                checked_blocks.append(block_L2.direcc_memoria)
                block_aux1.set_coherencia("S")
                block_aux10.set_coherencia("S")
                file.write("Setting %d adress as shared on P0:1, and P1:0\n" % (block_L2.direcc_memoria))

            elif(block_aux1 != None and block_aux11 != None and shared_blocks.count(block_L2.direcc_memoria) == 0):
                block_L2.set_coherencia("S")
                block_L2.dueno.clear()
                block_L2.dueno.append("P0:1")
                block_L2.dueno.append("P1:1")
                shared_blocks.append(block_L2.direcc_memoria)
                checked_blocks.append(block_L2.direcc_memoria)
                block_aux1.set_coherencia("S")
                block_aux11.set_coherencia("S")
                file.write("Setting %d adress as shared on P0:1 and P1:1\n" % (block_L2.direcc_memoria))
            else:
                if(shared_blocks.count(block_L2.direcc_memoria) == 0 and block_L2.direcc_memoria != -1 and checked_blocks.count(block_L2.direcc_memoria) == 0):
                    block_L2.set_coherencia("M")
                    checked_blocks.append(block_L2.direcc_memoria)
                    block_L2.dueno.clear()
                    if(block_aux0 != None):
                        block_L2.dueno.append("P0:0")
                        self.cache_P0.search_block(block_L2.get_direcc_memoria()).set_coherencia("M")
                    if(block_aux1 != None):
                        block_L2.dueno.append("P0:1")
                        self.cache_P1.search_block(block_L2.get_direcc_memoria()).set_coherencia("M")
                    if(block_L2.dueno == []):
                        block_L2.set_coherencia("I")
                else:
                    block_L2.set_coherencia("I")
                    block_L2.dueno.clear()
        file.close()

    def checkL2P1(self):
        file = open("logFile.txt", "a+")
        shared_blocks = []
        checked_blocks = []

        for block_L2 in self.cache_L2P1.mem_blocks:
            block_L2.set_coherencia("I")


        for block_L2 in self.cache_L2P1.mem_blocks:
            block_aux0 = self.cache_P0.search_block(block_L2.direcc_memoria)
            block_aux1 = self.cache_P1.search_block(block_L2.direcc_memoria)
            block_aux10 = self.cache_P10.search_block(block_L2.direcc_memoria)
            block_aux11 = self.cache_P11.search_block(block_L2.direcc_memoria)

            if(block_aux0 != None and block_aux1 != None and block_aux10 != None and block_aux11 != None and shared_blocks.count(block_L2.direcc_memoria) == 0):
                block_L2.set_coherencia("S")
                block_L2.dueno.clear()
                block_L2.dueno.append("P0:0")
                block_L2.dueno.append("P0:1")
                block_L2.dueno.append("P1:0")
                block_L2.dueno.append("P1:1")
                shared_blocks.append(block_L2.direcc_memoria)
                checked_blocks.append(block_L2.direcc_memoria)
                block_aux0.set_coherencia("S")
                block_aux1.set_coherencia("S")
                block_aux10.set_coherencia("S")
                block_aux11.set_coherencia("S")
                file.write("Setting %d adress as shared on P0:0, P0:1, P1:0, P1:1\n" % (block_L2.direcc_memoria))

            elif(block_aux0 != None and block_aux10 != None and block_aux11 != None and shared_blocks.count(block_L2.direcc_memoria) == 0):
                block_L2.set_coherencia("S")
                block_L2.dueno.clear()
                block_L2.dueno.append("P0:0")
                block_L2.dueno.append("P1:0")
                block_L2.dueno.append("P1:1")
                shared_blocks.append(block_L2.direcc_memoria)
                checked_blocks.append(block_L2.direcc_memoria)
                block_aux0.set_coherencia("S")
                block_aux10.set_coherencia("S")
                block_aux11.set_coherencia("S")
                file.write("Setting %d adress as shared on P0:0, P1:0, P1:1\n" % (block_L2.direcc_memoria))

            elif(block_aux0 != None and block_aux10 != None and shared_blocks.count(block_L2.direcc_memoria) == 0):
                block_L2.set_coherencia("S")
                block_L2.dueno.clear()
                block_L2.dueno.append("P0:0")
                block_L2.dueno.append("P1:0")
                shared_blocks.append(block_L2.direcc_memoria)
                checked_blocks.append(block_L2.direcc_memoria)
                block_aux0.set_coherencia("S")
                block_aux10.set_coherencia("S")
                file.write("Setting %d adress as shared on P0:0, and P1:0\n" % (block_L2.direcc_memoria))

            elif(block_aux0 != None and block_aux11 != None and shared_blocks.count(block_L2.direcc_memoria) == 0):
                block_L2.set_coherencia("S")
                block_L2.dueno.clear()
                block_L2.dueno.append("P0:0")
                block_L2.dueno.append("P1:1")
                shared_blocks.append(block_L2.direcc_memoria)
                checked_blocks.append(block_L2.direcc_memoria)
                block_aux0.set_coherencia("S")
                block_aux11.set_coherencia("S")
                file.write("Setting %d adress as shared on P0:0 and P1:1\n" % (block_L2.direcc_memoria))


            elif(block_aux0 != None and block_aux1 != None and shared_blocks.count(block_L2.direcc_memoria) == 0):
                block_L2.set_coherencia("S")
                block_L2.dueno.clear()
                block_L2.dueno.append("P0:0")
                block_L2.dueno.append("P0:1")
                shared_blocks.append(block_L2.direcc_memoria)
                checked_blocks.append(block_L2.direcc_memoria)
                block_aux0.set_coherencia("S")
                block_aux1.set_coherencia("S")
                file.write("Setting %d adress as shared on P0:0 and P0:1\n" % (block_L2.direcc_memoria))
            
            elif(block_aux1 != None and block_aux10 != None and block_aux11 != None and shared_blocks.count(block_L2.direcc_memoria) == 0):
                block_L2.set_coherencia("S")
                block_L2.dueno.clear()
                block_L2.dueno.append("P0:1")
                block_L2.dueno.append("P1:0")
                block_L2.dueno.append("P1:1")
                shared_blocks.append(block_L2.direcc_memoria)
                checked_blocks.append(block_L2.direcc_memoria)
                block_aux1.set_coherencia("S")
                block_aux10.set_coherencia("S")
                block_aux11.set_coherencia("S")
                file.write("Setting %d adress as shared on P0:1, P1:0, P1:1\n" % (block_L2.direcc_memoria))

            elif(block_aux1 != None and block_aux10 != None and shared_blocks.count(block_L2.direcc_memoria) == 0):
                block_L2.set_coherencia("S")
                block_L2.dueno.clear()
                block_L2.dueno.append("P0:1")
                block_L2.dueno.append("P1:0")
                shared_blocks.append(block_L2.direcc_memoria)
                checked_blocks.append(block_L2.direcc_memoria)
                block_aux1.set_coherencia("S")
                block_aux10.set_coherencia("S")
                file.write("Setting %d adress as shared on P0:1, and P1:0\n" % (block_L2.direcc_memoria))

            elif(block_aux1 != None and block_aux11 != None and shared_blocks.count(block_L2.direcc_memoria) == 0):
                block_L2.set_coherencia("S")
                block_L2.dueno.clear()
                block_L2.dueno.append("P0:1")
                block_L2.dueno.append("P1:1")
                shared_blocks.append(block_L2.direcc_memoria)
                checked_blocks.append(block_L2.direcc_memoria)
                block_aux1.set_coherencia("S")
                block_aux11.set_coherencia("S")
                file.write("Setting %d adress as shared on P0:1 and P1:1\n" % (block_L2.direcc_memoria))
            
            elif(block_aux10 != None and block_aux11 != None and shared_blocks.count(block_L2.direcc_memoria) == 0):
                block_L2.set_coherencia("S")
                block_L2.dueno.clear()
                block_L2.dueno.append("P1:0")
                block_L2.dueno.append("P1:1")
                shared_blocks.append(block_L2.direcc_memoria)
                checked_blocks.append(block_L2.direcc_memoria)
                block_aux10.set_coherencia("S")
                block_aux11.set_coherencia("S")
                file.write("Setting %d adress as shared on P0:1 and P1:1\n" % (block_L2.direcc_memoria))
            else:
                if(shared_blocks.count(block_L2.direcc_memoria) == 0 and block_L2.direcc_memoria != -1 and checked_blocks.count(block_L2.direcc_memoria) == 0):
                    block_L2.set_coherencia("M")
                    checked_blocks.append(block_L2.direcc_memoria)
                    block_L2.dueno.clear()
                    if(block_aux10 != None):
                        block_L2.dueno.append("P1:0")
                        self.cache_P10.search_block(block_L2.get_direcc_memoria()).set_coherencia("M")
                    if(block_aux11 != None):
                        block_L2.dueno.append("P1:1")
                        self.cache_P11.search_block(block_L2.get_direcc_memoria()).set_coherencia("M")
                    if(block_L2.dueno == []):
                        block_L2.set_coherencia("I")
                else:
                    block_L2.set_coherencia("I")
                    block_L2.dueno.clear()
        file.close()
    
    def check_Mem(self):

        for block_mem in self.mem_p.mem_blocks:
            block_mem.set_coherencia("I")
            block_mem.dueno.clear()

        for block_L2 in self.cache_L2.mem_blocks:
            if(block_L2.direcc_memoria != -1):
                self.mem_p.mem_blocks[block_L2.direcc_memoria].set_coherencia("M")
                if(block_L2.dueno.count("P0:0") > 0 or block_L2.dueno.count("P0:1") > 0):
                    self.mem_p.mem_blocks[block_L2.direcc_memoria].dueno.append("C0")
        for block_L2 in self.cache_L2P1.mem_blocks:
            if(block_L2.direcc_memoria != -1):
                self.mem_p.mem_blocks[block_L2.direcc_memoria].set_coherencia("M")
                if(block_L2.dueno.count("P1:0") > 0 or block_L2.dueno.count("P1:1") > 0):
                    self.mem_p.mem_blocks[block_L2.direcc_memoria].dueno.append("C1")

        for block_mem in self.mem_p.mem_blocks:
            if(len(block_mem.dueno) > 1):
                block_mem.set_coherencia("S")



