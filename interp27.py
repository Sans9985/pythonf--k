# NOTE: only use this with python 2.7!

from sys import version_info, argv

if version_info >= (2, 7):
    from _mod27 import Instruction, write
else:
    print "Version " + ".".join(map(str, version_info[:3])) + " is not compatible with this script. Use version 2.7 or later."
    exit()

class v:
    arr = bytearray(32768)
    pointer = 0

def load(name, debug = False):
    x = []
    
    with open(name) as f:
        file = f.read()
    
    file = file.split("\n")

    i = 0
    while i < len(file):
        line = file[i]
        if debug:
            s = str(i+1).format(">3") + " " + line
            print s

        if line.startswith("*") or line == "":
            del file[i]
            continue

        if line.startswith("$"):
            try:
                y = load("./" + line[1:] + ".pf")

                for l in y:
                    x.append(l)

            except FileNotFoundError:
                print("Script '" + line[1:] + ".pf' not found; the instruction on line " + str(i + 1) + " is skipped.")

            i += 1
            continue

        x.append(Instruction(line))
        i += 1

    return x

def do(lines):
    string = []

    for l in lines:
        string.append(l.__py__())

    for inst in string:
        print inst

        exec(inst)

        if v.pointer < 0:
            v.pointer += len(v.arr)

        if v.pointer > len(v.arr) - 1:
            v.pointer -= len(v.arr)

def main(file, debug):
    if debug in ("-1", "1", "true", "True", "yes", "Yes", "y", "Y", "t", "T"): debug = True
    else: debug = False

    x = load("./" + file, debug)

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
            "Too many arguments. (expected at most 2, got " + str(len(argv) - 1)
        )
else:
    raise NameError("Cannot import file. Launch file directly.")