
import display as dspl
import sys, buffer, input,fileIO
from input import C_x_, is_ascii, is_control, ml_prompt, ml_yesorno
import keybinding as kbd
import editor_shared as e
import mylog as ml


def fetch_exec(c: int):
    
    #printable character inserting
    
    if is_ascii(c):
        for _ in range(e.uni_arg):
            e.curw.usebuf.insstr(*e.curw.absyx(), chr(c))
            dspl.rightchar(1)
        e.uni_arg = 1

    #Enter or C-O
    elif c == input.C_("M") or c == input.C_('O'):
        e.curw.usebuf.insnl(*e.curw.absyx())
        dspl.bol(1)
        dspl.nextline(1)
    elif c == input.C_("U"):
        e.uni_arg = int(input.ml_prompt("set arg to:"))
        dspl.ml_print("universal arg= %d" % e.uni_arg)
    #Backspace
    elif c == 0x7f:
        for _ in range(e.uni_arg):
            #If nothing to delete don't move the cursor
            if e.curb.delchar(*e.curw.absyx()):
                dspl.leftchar(1)
        e.uni_arg = 1
    #test ml_prompt()
    elif c == input.C_x_(input.C_("P")):
        ml.warn(input.ml_prompt("TRY:"))
    elif kbd.is_bound(c):
        cmd = kbd.binding_table[c]

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

    if e.curw.usebuf != None and e.curw.usebuf.chgdflag:
        if not ml_yesorno("Modified Buffer exist anyway?"):
            return 
    dspl.cleanup()
    sys.exit()


cmd_func_table = {
  "show-version":   dspl.showversion,
#   "split-window":   dspl.splitw,
  "editor-exit":    editor_exit,
  "save-buffer":    fileIO.cb_save,
  "next-line":      dspl.nextline,
  "previous-line":  dspl.prevline,
  "right-char":     dspl.rightchar,
  "left-char":      dspl.leftchar,
  "split-window-vt": dspl.splitw_vt,
  "other-window":   dspl.other_w,
  "load-file":        buffer.load_file,
  "begin-of-line":  dspl.bol,
  "end-of-line":    dspl.eol,
  "open-line":      None,
  "merge-window":   dspl.mergew,
  "display-help-message": dspl.show_help,
  "kill-to-eol":     buffer.kill_to_eol,
  "page-down":      dspl.page_down,
  "page-up":        dspl.page_up,
  "save-as":         fileIO.save_as
}

if __name__ == "__main__":
    try:
        editor_main()
    except Exception as e:
        #do neccessary clean up
        ml.warn("Exception in main(). %s"  % str(e))
        editor_exit()
editor_exit()