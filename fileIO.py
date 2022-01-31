import editor_shared as e
import display as dspl
from input import ml_prompt
import mylog as ml

#
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
    numCharsWrited = fwrite(e.curw.usebuf.fname, e.curw.usebuf.to_str())
    e.curw.usebuf.chgdflag = False
    dspl.ml_print(str(numCharsWrited) + " characters wrote.")

def save_as(_):
    fname = ml_prompt("Save as:")
    with open(fname, 'w') as f :
        dspl.ml_print("%d characters wrote." % f.write(e.curw.usebuf.to_str()))

def cb_openfile(filename):
    f = fallines(filename)
    e.curw.usebuf.blines = [ln.rstrip() for ln in f]


# def cb_appendfile(filename):
#     newlines = fallines(filename)
#     e.curb.blines += [ln.rstrip() for ln in newlines]


