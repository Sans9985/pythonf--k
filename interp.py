from sys import version_info, argv

if version_info > (3, 9):
    from _mod310 import Instruction, write
else:
    print("Using pre-3.10 module")
    from _mod39 import Instruction, write

class v:
    arr: bytearray = bytearray(32768)
    pointer: int = 0

def load(name: str, debug: bool = False) -> list[Instruction]:
    x: list[Instruction] = []
    
    with open(name) as f:
        file = f.read()
    
    file = file.split("\n")

    i = 0
    while i < len(file):
        line = file[i]
        if debug: print(f"{i+1:>3} {line}")

        if line.startswith("*") or line == "":
            del file[i]
            continue

        if line.startswith("$"):
            try:
                y = load(f"./{line[1:]}.pf")

                for l in y:
                    x.append(l)

            except FileNotFoundError:
                print(f"Script '{line[1:]}.pf' not found; the instruction on line {i+1} is skipped.")

            i += 1
            continue

        x.append(Instruction(line))
        i += 1

    return x

def do(lines: list[Instruction]) -> None:
    string: list[str] = []

    for l in lines:
        string.append(l.__py__())

    for inst in string:
        exec(inst)

        if v.pointer < 0:
            v.pointer += len(v.arr)

        if v.pointer > len(v.arr) - 1:
            v.pointer -= len(v.arr)

def main(file: str, debug: bool = False):
    if debug in ("-1", "1", "true", "True", "yes", "Yes", "y", "Y", "t", "T"): debug = True
    else: debug = False

    x: list[Instruction] = load(f"./{file}", debug)

    do(x)

if __name__ == '__main__':
    l = len(argv)
    if l == 3:
        main(argv[1], argv[2])
    elif l == 2:
        main(argv[1], False)
    elif l == 1:
        main(input("Please enter your file's name: "))
    else:
        raise TypeError(
            f"Too many arguments. (expected at most 2, got {len(argv) - 1})"
        )
else:
    raise NameError("Cannot import file. Launch file directly.")