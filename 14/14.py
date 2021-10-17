from pathlib import Path
from struct import pack, unpack

data = filter(lambda x: x != "", Path("input14.txt").read_text().split("\n"))
data = list(data)

def bitmask(instruction):
    return instruction.split(" = ")[1]
    
def execute(instruction, mask, ram):
    m, v = instruction.split(" = ")
    addr = int(m.split("[")[1].split("]")[0])
    sv = f"{int(v):036b}"
    masked_value = mask_value(mask, sv)
    ram[addr] = int(masked_value, 2)

def mask_value(mask, value):
    res = ""
    for m, v in zip(mask, value):
        if m == "X":
            res += v
        else:
            res += m
    return res

mask = ""
mem = {}
for instruction in data:
    print(mask)
    if "mask" in instruction:
        mask = bitmask(instruction)
    elif "mem" in instruction:
        execute(instruction, mask, mem)

print(sum(mem.values()))


## part2

def execute2(instruction, mask, ram):
    m, value = instruction.split(" = ")
    addr = int(m.split("[")[1].split("]")[0])
    saddr = f"{addr:036b}"
    masked_addrs = mask_addr(mask, saddr)
    for baddr in masked_addrs:
        iaddr = int(baddr, 2)
        ram[iaddr] = int(value)

def mask_addr(mask, addr):
    saddr = ""
    for m, a in zip(mask, addr):
        if m == "0":
            saddr += a
        else:
            saddr += m
    return addresses(saddr)

def addresses(addr):
    next_batch = []
    curr_batch = [addr]
    run = True
    while run:
        run = False
        for a in curr_batch:
            if "X" not in a:
                continue
            run = True
            i = a.index("X")
            next_batch.append(a[:i] + "0" + a[i+1:])
            next_batch.append(a[:i] + "1" + a[i+1:])
        if run:
            curr_batch, next_batch = next_batch, []
    return curr_batch

    

data = filter(lambda x: x != "", Path("input14.txt").read_text().split("\n"))
data = list(data)

mask = ""
mem  = {}
for instruction in data:
    if "mask" in instruction:
        mask = bitmask(instruction)
    elif "mem" in instruction:
        execute2(instruction, mask, mem)

print(sum(mem.values()))
