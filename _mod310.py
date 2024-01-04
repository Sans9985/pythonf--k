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

        match self.instruction:
            case ">": out += f"v.pointer += {self.param}"
            case "<": out += f"v.pointer -= {self.param}"
            case "_": out += f"print('{self.param}')"
            case "^": out += f"v.arr[v.pointer] = {self.param}"
            case ".": out += f"write({self.param}, v.arr)"
            case ",": out += f"v.pointer = {self.param}"

            case "/": out += f"""with open('input', 'rb') as f: data = f.read()
{" " * mv.ind}if len(data) != 0:
{" " * mv.ind}    for byte in data:
{" " * mv.ind}        v.arr[v.pointer] = byte
{" " * mv.ind}        v.pointer += 1"""

            case "\\": out += f"""with open('output', 'rb') as f: data = f.read()
{" " * mv.ind}for byte in data:
{" " * mv.ind}    v.arr[v.pointer] = byte
{" " * mv.ind}    v.pointer += 1"""

            case "~":
                mv.ind = 4

                m = self.param.split(":")
                out += f"""for i in range({m[1]}): 
{" " * mv.ind}"""

                self.param = m[0]
                b = self.param.split("(")[1].strip(")").split(";")

                if b[-1] == '':
                    del b[-1]

                for inst in b:
                    inst = Instruction(inst)
                    out += f"{inst.__py__()}\n{' ' * mv.ind}"

                    if inst.param == "$":
                        out = out.replace("'$'", "i")

                mv.ind = 0

        return out