import editor_shared as e
import input
import fileIO
import mylog as ml


class BufferInterface:
    '''
        initializer.
        args:
        bmodes  modes enable in this buffer
        blines  text, list of string
        bdotln  now which line holds the cursor(dot)?
        bdotidx postion of cursor

        bwlnkd  list of windows linke to this buffer
        bflname filname string, if the buffer is create by file, empty otherwise
    '''

    def __init__(self, bname, blines, fname):
        pass

    def getline(self, k):
        pass

    def insstr(self, k, s):
        pass

    def insnl(self, k):
        pass

    def delchar(self, k, i):
        pass

    # def delline(self):
    #     pass

    def to_str(self):
        pass


class LinkeBuffer(BufferInterface):
    pass


class ListBuffer(BufferInterface):
    '''
    since Buffer class is the actual place text data being store, its functions implement
    common text eiting features.
    '''

    def __init__(self, bname, blines, fname):

        self.bname = bname
        self.bmodes = set()
        self.chgdflag = False
        self.blines: list[str] = blines
        self.fname = fname
    
    def buflen(self):
        return len(self.blines)

    def linelen(self, k):
        return len(self.blines[k])

    def insstr(self, k, i, s):
        # if k > (n:=len(self.blines)):
        #     for _ in range(k - n + 1):
        #         self.blines.append("")
        # if i > (n:=len(self.blines[k])):
        #     self.blines[k] += (i - n + 1) * " "

        originln = self.blines[k]
        self.blines[k] = originln[:i] + s + originln[i:]
        self.chgdflag = True

    def insnl(self, k, i):
        # if point is at the end of a line:
        ml.warn("line %d = %s, Insert at %d" %(k, self.blines[k], i))

        if i == len(self.blines[k]):
            self.blines.insert(k+1, "")
        
        #if point is at the beginning of a line,
        elif i == 0:
            if k > 0:
                self.blines.insert(k-1, "")
            elif k == 0:
                self.blines.insert(k, "")
        
        #or, at the middle of a line
        else:
            originln = self.blines[k]
            self.blines.insert(k, "")
            self.blines[k] = originln[:i]
            self.blines[k+1] = originln[i:]
            # ml.warn("Buf = %s" % "\r\n".join(self.blines))
        self.chgdflag = True
        
    def delchar(self, k, i):
        if k == 0 and i == 0:
            return False
        if i == 0:
            lk = self.blines.pop(k)
            self.blines[k-1] += lk
            return True
        originln = self.blines[k] 
        ml.warn("del char in %d %d" %(k, i))
        self.blines[k] = originln[:i-1] + originln[i:]
        self.chgdflag = True
        return True
    # def delline(self, k):
    #     pass
    def deltoeol(self, k,  i):
        orig = self.blines[k]
        self.blines[k] = orig[:i]
        self.chgdflag = True

    def getline(self, k):
        if k >= len(self.blines):
            raise IndexError
        else:
            return self.blines[k]

    def to_str(self):
        return "\r\n".join(self.blines)


def init(fname=""):
    if fname != "":
        e.curb = ListBuffer(fname, None, fname)
        # e.cur = e.curw.usebuf
        e.curb.blines = [l.strip() for l in fileIO.fallines(fname)]
    else:
        e.curb = ListBuffer("scratch", ["#Here is your scratch."], "")

    e.buffer_table = {e.curb.bname: e.curb}

def kill_to_eol(_):
    b: ListBuffer  = e.curw.usebuf
    b.deltoeol(e.curw.cy, e.curw.cx)
    b.chgdflag =True
# def switchbuf(b: ListBuffer):
#     e.curb = b

def load_file(_):
    openf = input.ml_prompt("File:")
    flines = [l.strip() for l in fileIO.fallines(openf)]
    e.curw.usebuf= ListBuffer(openf, flines, openf)
    e.curw.cy, e.curw.cx = 0, 0