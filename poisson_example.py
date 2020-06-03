import numpy as np

s = np.random.poisson(2,6)

ins_array = []

for num in s:
    aux_num = num
    while(aux_num > 3):
        aux_num = aux_num - 3
    ins_array.append(aux_num)

print(ins_array)

