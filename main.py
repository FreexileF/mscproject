
import display as dspl
import sys, buffer, input,fileIO
from input import is_ascii, is_control
import keybinding as kbd
import editor_shared as e
import mylog as ml


def fetch_exec(c: int):
    
    #printable character inserting
    
    if is_ascii(c):
        for _ in range(e.uni_arg):
            e.curb.insstr(*e.curw.absyx(), chr(c))
            dspl.rightchar(1)
        e.uni_arg = 1

    #Enter
    elif c == input.C_("M"):
        e.curb.insnl(*e.curw.absyx())
        dspl.rightchar(1)
    elif c == input.C_("U"):
        e.uni_arg = int(sys.stdin.read(1))
        dspl.ml_print("Arg = %d" % e.uni_arg)
    #Backspace
    elif c == 0x7f:
        for _ in range(e.uni_arg):
            e.curb.delchar(*e.curw.absyx())
            dspl.leftchar(1)
        e.uni_arg = 1
    elif kbd.is_bound(c):
        cmd = kbd.binding_table[c]
        ml.warn(cmd)

        f = cmd_func_table[cmd]

        f(e.uni_arg)
        e.uni_arg = 1
    else:
        dspl.ml_print("Key not bound.")
    
    

def editor_init():
    if len(sys.argv) >= 2:
        buffer.init(sys.argv[1])

    else:
        buffer.init()

    dspl.init()


def editor_main():
    editor_init()
    while True:
        c = input.get_command()
        fetch_exec(c)
        dspl.upd_allw()
        dspl.hw_update()


def editor_exit(_ = None):
    dspl.cleanup()
    sys.exit()


cmd_func_table = {
  "show-version":   dspl.showversion,
  "split-window":   dspl.splitw,
  "editor-exit":    editor_exit,
  "save-buffer":    fileIO.cb_save,
  "next-line":      dspl.nextline,
  "previous-line":  dspl.prevline,
  "right-char":     dspl.rightchar,
  "left-char":      dspl.leftchar,
#   "other-window":   dspl.otherwindow,
#   "open-line":      buffer.insnl
}

if __name__ == "__main__":
    try:
        editor_main()
    except Exception:
        #do neccessary clean up
        editor_exit()
