from typing import List

from main.main import VirusMap


def interactive_input():
    sentinel = "#"
    input1 = input("Please key in M N value (space seperated):")
    matrix = []
    print(
        "Please key in hotel matrix (room is seperated by space, floor by new line, end matrix with # in new line):"
    )
    for line in iter(input, sentinel):
        _ = line.split(" ")
        matrix.append(_)
    m, n = [eval(i) for i in input1.split(" ")]
    print(VirusMap(m, n, matrix).solve())


def main_sample():
    m = 3
    n = 5
    matrix = [[2, 1, 0, 2, 1], [1, 1, 1, 1, 1], [1, 0, 0, 2, 1]]
    print(VirusMap(m, n, matrix).solve())


if __name__ == "__main__":
    main_sample()
    # interactive_main()
