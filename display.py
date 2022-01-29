import curses
import editor_shared as e
import mylog as lg
msgline  = None



def init():
    global msgline
    curses.initscr()
    curses.raw()
    curses.nonl()
    curses.noecho()

    
    e.scrheight, e.scrwidth = curses.LINES, curses.COLS
    
    msgline = curses.newwin(1, e.scrwidth, e.scrheight-1, 0)    

    firstwnd = CursesWindow(e.scrheight - 1, e.scrwidth,
                            0, 0, e.curb, None)
    e.headw = firstwnd
    e.curw = firstwnd

    ml_print("Welcome to %s." % e.PROGRAM_NAME)
    e.curw.update()
    hw_update()


def cleanup():
    lg.warn("Clean up().")
    # lg.warn("On exit: %d-%d" % curses.getsyx())
    curses.noraw()
    curses.nl()
    curses.echo()
    curses.endwin()

def ml_print(s):
    msgline.erase()
    msgline.addstr(s)
    msgline.refresh()

def showversion(_):
    ml_print(e.PROGRAM_NAME + " " + e.PROGRAM_VERSION)

def upd_allw():
    wp = e.headw
    while wp != None:

        wp.update()
        wp = wp.wnext

def hw_update():
    e.curw.mvcursor(e.curw.cy - e.curw.yof, e.curw.cx - e.curw.xof)
    curses.doupdate()

def splitw(_):
    w: CursesWindow = e.curw
    if w.nrow < 3:
        return
    uppernrow = w.nrow // 2
    lowerrow = w.nrow - uppernrow
    w.resize(uppernrow, w.ncol)
    newwnd = CursesWindow(lowerrow, w.ncol, w.bgny +
                          uppernrow, w.bgnx, w.usebuf, w.wnext)
    newwnd.yof, newwnd.xof = w.yof, w.xof
    w.wnext = newwnd

def rightchar(n):
    for _ in range(n):
        e.curw.cursorforw()

def leftchar(n):
    for _ in range(n):
        e.curw.cursorback()

def nextline(n):
    for _ in range(n):
        e.curw.cursordown()

def prevline(n):
    for _ in range(n):
        e.curw.cursorup()

class CursesWindow:
    def __init__(self, nrow, ncol, bgny, bgnx, usebuf, wnext) -> None:
        #Postion and size
        self.nrow = nrow
        self.ncol = ncol
        self.bgny = bgny
        self.bgnx = bgnx

        self.textnrow = self.nrow-1
        # cursor's position
        self.cy, self.cx = 0, 0

        self.usebuf = usebuf
        self.wnext = wnext

        self.yof, self.xof = 0, 0

        self.curseswnd: curses._CursesWindow = curses.newwin(nrow, ncol, bgny, bgnx)

        self.view: list[str] = []
        self.modestr: str = ""
        
    def upd_mode(self):
        stat = "Modified" if self.usebuf.chgdflag else " "
        self.modestr = "%s : %s (%s)" % (e.PROGRAM_NAME, self.usebuf.bname, stat)

    def upd_view(self):
        #Depending on the size of window, extact text from buffer
        viewnrow, viewncol = self.textnrow, self.ncol
        newview = []
        for i in range(viewnrow):
            try:
                wln = self.usebuf.getline(i + self.yof)
                if len(wln) > viewncol:
                    wln = wln[:viewncol]
                newview.append(wln)
            except IndexError:
                #There might be not enough lines ,if so, we simply ignore it
                #because we just print whatever we got, not need to full fill the screen,
                #the screen itself keeps as empty as it originally is
                pass

        self.view = newview

    def writeln(self, i, ln, atrr = curses.A_NORMAL):
        self.curseswnd.addstr(i, 0, ln, atrr)

    def mvcursor(self, y, x):

        lg.warn("(%d,  %d)" % (y, x))
        self.curseswnd.move(y, x)
        self.curseswnd.noutrefresh()

    def cursorforw(self):
        if self.cx == self.usebuf.linelen(self.cy) - 1:
            if self.cy <  self.usebuf.buflen() - 1:
                self.cy += 1
                self.cx = 0
        else:
            self.cx += 1

    def cursorback(self):
        if self.cx == 0:
            if self.cy > 0:
                self.cy -= 1
                self.cx = self.usebuf.linelen(self.cy) - 1
        else:
            self.cx -= 1


    def cursordown(self):
        if self.cy < self.usebuf.buflen() - 1:
            self.cy += 1
        # if self.cx >= (mx:=self.usebuf.linelen(self.cy) - 1):
        #     self.cx = max(0, mx-1)

    def cursorup(self):
        if self.cy > 0:
            self.cy -= 1
        # if self.cx >= (mx:=self.usebuf.linelen(self.cy) - 1):
        #     self.cx = max(0, mx-1)

    def absyx(self):
        return (self.cy, self.cx)

    def wndyx(self):
        lg.warn("Cy = %d,Cx = %d" % self.absyx())

        return (self.cy - self.yof, self.cx - self.xof)

    def update(self):
        #clear the entire window
        self.curseswnd.erase()
        
        self.reframe()

        self.upd_view()
        
        self.upd_mode()

        # To update the window, first redraw view, then modestring
        for i, ln in enumerate(self.view):
            self.writeln(i, ln)

        self.writeln(self.nrow-1, self.modestr, curses.A_STANDOUT)

        # Restore cursor's position
        self.mvcursor(*self.wndyx())

        self.curseswnd.noutrefresh()

    def resize(self, newnrow, newncol):
        self.nrow, self.ncol = newnrow, newncol
        self.curseswnd.resize(newnrow, newncol)

    def reframe(self):
        lg.warn("yof = %d, Bottom of window: %d" %(self.yof, self.yof + self.textnrow))
        if self.cy >= (mxwy:=self.yof + self.textnrow - 1):
           
            self.vert_scroll(1 * (self.cy - mxwy))

        elif self.cy < self.yof:
            self.vert_scroll(-1 * (self.yof - self.cy))

        elif True:
            pass
        elif True: 
            pass

    def vert_scroll(self, d):
        # lg.warn("Scroll: %d" % d)
        self.yof += d
        
    def hori_scroll(self, d):
        self.xof += d



    def splitw(self):
        pass
