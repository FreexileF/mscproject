import display as dspl
import atexit
import sys
import mylog as ml

ctrl = 0x10000000
alt = 0x2000000
ctrlx = 0x40000000
CSI = 0x80000000


def ctoi(k): return ord(k) if isinstance(k, str) else k


def C_(k): return ctrl | ctoi(k)
def M_(k): return alt | ctoi(k)
def C_x_(k): return ctrlx | ctoi(k)


ARROW_UP = CSI | ctoi('A')
ARROW_DOWN = CSI | ctoi('B')
ARROW_RIGHT = CSI | ctoi('C')
ARROW_LEFT = CSI | ctoi('D')


def getc():
    return ord(sys.stdin.read(1))


def get_char():
    return chr(getc())


def is_ascii(c: int):
    return c >= 0x20 and c <= 0x7e


def is_control(c: int):
    return c >= 0x00 and c <= 0x1f


def gets():
    '''
    Input a string ending up with Enter.

    This should have been a trivial function, but the don't forget 
    console is in Raw mode which makes things a bit different.
    '''
    s = ""
    while (c := get_char() != '\r'):
        s += c
    return s


def get_onekey():
    c = getc()

    if is_control(c):
        return ctrl | (c + 64)
    else:
        return c


def get_command():
    '''
    TODO: BUG: should add timeout detecting maybe
    '''

    c = get_onekey()

    # command with C-X prefix
    if c == C_("X"):
        k = get_onekey()
        return C_x_(k)

    # process meta prefix
    if c == C_('['):
        c = get_onekey()
        if c == ord('['):
            c = get_onekey()
            return CSI | c
        # force uppercase
        if c >= ord('a') and c <= ord('z'):
            c -= 32
# ESC[
        if is_control(c):
            return M_(C_(c))

        else:
            return M_(c)

    else:
        return c


def cmd2str(command):

    cmdstr = ""
    if command & CSI != 0:
        command &= ~CSI
        cmdstr = "ESC[" + cmdstr
    if command & ctrlx != 0:
        command &= ~ctrlx
        cmdstr = "C-X " + cmdstr
    if command & alt != 0:
        command &= ~alt
        cmdstr = cmdstr + "M-"
    if command & ctrl != 0:
        command &= ~ctrl
        cmdstr = cmdstr + "C-"

    cmdstr = cmdstr + chr(command)
    return cmdstr


if __name__ == "__main__":
    # i = 1
    import curses
    curses.initscr()

    curses.cbreak()
    curses.noecho()
    while True:
        # t.enableRaw()
        c = get_command()
        # print(i, end='\r\n')
        print(cmd2str(c), end='\r\n')
        # i += 1
        if c == ord('q'):
            # t.restore()
            curses.endwin()
            exit()
