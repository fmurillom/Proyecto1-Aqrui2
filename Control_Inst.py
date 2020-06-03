class Control_Inst:
    proc_orig = ""
    instr_type = ""
    mem_addr = 0
    data = 0

    def __init__(self, proc_orig, instr_type, mem_addr, data):
        self.proc_orig = proc_orig
        self.instr_type = instr_type
        self.data = data
        self.mem_addr = mem_addr

    def __str__(self):
        out = self.proc_orig + " " + self.instr_type + " " + str(self.mem_addr) + " " + str(self.data)
        return out