from pathlib import Path

def parse_input(file: Path):
    program = []
    with file.open() as f:
        for line in f:
            opcode, param = line.strip().split(" ")
            program.append( (opcode, int(param)) )
    return program


def run(program):
    pc = 0
    acc = 0
    already_run = set([])
    while pc not in already_run and pc < len(program):
        already_run.add(pc)
        opcode, param = program[pc]
        if opcode == "nop":
            pc += 1
        elif opcode == "acc":
            acc += param
            pc += 1
        elif opcode == "jmp":
            pc += param
    return (acc, pc == len(program))


def corrections(program):
    for i in range(len(program)):
        opcode, param = program[i]
        if opcode == "jmp":
            new_code = program[:]
            new_code[i] = ("nop", param)
            yield new_code
        elif opcode == "nop" and param != 0:
            new_code = program[:]
            new_code[i] = ("jmp", param)
            yield new_code

program = parse_input(Path("input8.txt"))
for new_code in corrections(program):
    acc, exited = run(new_code)
    if exited:
        print(acc)
        break

