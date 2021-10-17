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
    while pc not in already_run:
        already_run.add(pc)
        opcode, param = program[pc]
        if opcode == "nop":
            pc += 1
        elif opcode == "acc":
            acc += param
            pc += 1
        elif opcode == "jmp":
            pc += param
    return acc

program = parse_input(Path("input8.txt"))

acc = run(program)
