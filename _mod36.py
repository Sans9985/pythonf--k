from time import time

class mv:
    ind: int = 0

def write(breakby: int, contents: bytearray) -> None:
    if breakby < 1:
        print("Parameter for operand '.' must be more than 1!")
        return

    with open("output", "wb") as f:
        if breakby == 1:
            f.write(contents)

        else:
            for i in range(len(contents) // (2 ** breakby)):
                f.write(contents[i:i+2**breakby] + b"\n")

class Instruction:
    def __init__(self, line: str) -> None:
        self.instruction = line[0]

        if len(line) == 1:
            self.param = 1
        else:
            self.param = line[1:]

            if self.param.isnumeric():
                self.param = int(self.param)

            if self.instruction != "^":
                ...
            else:
                self.param = ord(self.param) if type(self.param) != int else self.param

    def __py__(self) -> str:
        """Return the Python replica of the instruction."""
        out: str = ""

        if self.instruction == ">": out += "v.pointer += " + str(self.param)
        elif self.instruction == "<": out += "v.pointer -= " + str(self.param)
        elif self.instruction == ";": out += "print '" + str(self.param) + "'"
        elif self.instruction == "!": out += "v.arr = bytearray(v.size)"
        elif self.instruction == "^": out += "v.arr[v.pointer] = " + str(self.param)
        elif self.instruction == ".": out += "write(" + str(self.param) + ", v.arr)"
        elif self.instruction == ",": out += "v.pointer = " + str(self.param)

        elif self.instruction == "/": out += \
            "with open('./input', 'r') as f: data = f.read()\n" + ' ' * mv.ind + \
            "if len(data) != 0:\n" + ' ' * mv.ind + \
            "    for byte in data:\n" + ' ' * mv.ind + \
            "        v.arr[v.pointer] = byte\n" + ' ' * mv.ind + \
            "        v.pointer += 1"
            
        elif self.instruction == "\\": out += \
            "_ = v.pointer\nv.pointer = 0\nwith open('./output', 'rb') as f: data = f.read()\n" + ' ' * mv.ind + \
            "for byte in data:\n" + ' ' * mv.ind + \
            "    v.arr[v.pointer] = byte\n" + ' ' * mv.ind + \
            "    v.pointer += 1\nv.pointer = _"

        elif self.instruction == "~":
            mv.ind = 4

            m = self.param.split(":")
            out += "for i in range(" + m[1] + "):\n" + " " * mv.ind

            self.param = m[0]
            b = self.param.split("(")[1].strip(")").split(";")

            if b[-1] == '':
                del b[-1]

            for inst in b:
                inst = Instruction(inst)
                out += inst.__py__() + "\n" + ' ' * mv.ind

                if inst.param == "$":
                    out = out.replace("'$'", "i")

            mv.ind = 0

        return out