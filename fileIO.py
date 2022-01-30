import editor_shared as e
import display as dspl
import mylog as ml
import sys

def ml_prompt(s):
    dspl.ml_print(s)
    while ch := sys.stdin.read(1) != "\r":
        

def fallines(filename):
    with open(filename) as f:
        return f.readlines()


def ffirstnlines(filename, n):
    lines = []
    with open(filename, "r") as f:
        i = 0
        while i < n:
            if f.readline() != "":
                i += 1
            else:
                break

    return lines


def fwrite(filename, s):
    with open(filename, "w") as f:
        return f.write(s)


def cb_save(_):
    numCharsWrited = fwrite(e.curb.fname, e.curb.to_str())
    dspl.ml_print(str(numCharsWrited) + " characters wrote.")


def cb_openfile(filename):
    f = fallines(filename)
    e.curb.blines = [ln.rstrip() for ln in f]


def cb_appendfile(filename):
    newlines = fallines(filename)
    e.curb.blines += [ln.rstrip() for ln in newlines]
