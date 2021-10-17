from aoc23 import run

def main():
    cups = [5, 9, 8, 1, 6, 2, 7, 3, 4]

    in2 = list(range(1, 1_000_001))
    in2[0:9] = cups
    res2 = run(10_000_000, in2)
    m1 = res2[1]
    m2 = res2[m1]
    print(m1*m2)

main()
