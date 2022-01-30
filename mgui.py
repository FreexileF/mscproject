from tkinter import *
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import messagebox
from tkinter.font import Font
from tkinter.ttk import *
import os
from tokenize import String

from more_itertools import value_chain
class editorTab(Frame):
    def __init__(self, root, name) -> None:
        Frame.__init__(self,root)

        self.root = root
        self.name = StringVar(value=name)

        self.fontfamily = StringVar()
        self.fontfamily.set("Courier New")
        self.fontsize = 14
        self.textfont = Font(family=self.fontfamily, size=self.fontsize)
        
        self.bgcolour = StringVar(value= "white")
        self.line_number_bar = Text(self, width=4, padx=3, takefocus=0, border=0,
                            background='#F0E68C', state='disabled')

        self.line_number_bar.pack(side='left', fill='y')    

        self.textarea = scrolledtext.ScrolledText(self, wrap=WORD, undo=True, font=self.textfont)
        self.textarea.pack(expand="yes", fill="both")
    

    def update_linenum(self, show=True):
        if show:
            row, _ = self.textarea.index("end").split('.')
            print("row = %s" % row)
            line_num_content = "\n".join([str(i) for i in range(1, int(row))])
            self.line_number_bar.config(state='normal')
            self.line_number_bar.delete('1.0', 'end')
            self.line_number_bar.insert('1.0', line_num_content)
            self.line_number_bar.config(state='disabled')
        else:
            self.line_number_bar.config(state='normal')
            self.line_number_bar.delete('1.0', 'end')
            self.line_number_bar.config(state='disabled')    
    
class editor(Tk):
    def __init__(self) -> None:
        super().__init__()
        self.set_window()
        self.set_tabs()
        #add a tab
        self.add_tab()
        self.create_menu_bar()
        

    def open_file(self, event="None"):
        print("open_file() is called.")
        input_file = filedialog.askopenfilename()
        fbasename = os.path.basename(input_file)
        if input_file:
            self.cur_tab().textarea.delete(1.0, END)
            self.notebook.tab(self.cur_tab(), text= fbasename)
            with open(input_file, 'r') as f:
                self.cur_tab().textarea.insert(1.0, f.read())
        self.cur_tab().update_linenum()

    def cur_textarea(self):
        return self.cur_tab().textarea

    def save(self, event=None):
        print("Tab's name=" + self.cur_tab().name)
        if not self.cur_tab().name:
            self.save_as()
        else:
            self.write_file(self.cur_tab().name)
    
    def save_as(self, event=None):
        input_file = filedialog.asksaveasfilename(
            filetypes=[("All Files", "*.*"), ("Text files", "*.txt")])
        if input_file:
            self.cur_tab().name = input_file
            self.write_file(self.cur_tab().name)

    def write_file(self, file_name):
        try:
            fname = self.cur_tab().name
            content = self.cur_tab().textarea.get(1.0, 'end')
            with open(fname, 'w') as f:
                f.write(content)
        except IOError:
            messagebox.showwarning("Save", "File saving failed")  

    def exit_editor(self):
        if messagebox.askokcancel("D"):
            self.destroy()

    def set_window(self):
        self.title("Notepad--")
        scn_width, scn_height = self.maxsize()
        wm_val = '800x600+%d+%d' % ((scn_width - 750) / 2, (scn_height - 450) / 2)
        self.geometry(wm_val)
        self.protocol('WM_DELETE_WINDOW', self.exit_editor)


    def create_menu_bar(self):
        #Useful variables for view menu
        self.is_show_line_num = IntVar()
        self.is_show_line_num.set(1)
        self.enable_word_wrap = BooleanVar()
        self.enable_word_wrap.set(False)

        menu_bar = Menu(self)
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label='New', command=self.add_tab)
        file_menu.add_command(label='Open...', accelerator='Ctrl+O', command=self.open_file)
        file_menu.add_command(label='Save', accelerator='Ctrl+S', command=self.save)
        file_menu.add_command(label='Save as...', accelerator='Shift+Ctrl+S', command=self.save_as)

        menu_bar.add_cascade(label='File', menu=file_menu)

        edit_menu = Menu(menu_bar, tearoff=0)



        edit_menu.add_command(label='undo', command=self.handle_menu_action('undo'), accelerator='Ctrl+Z')
        edit_menu.add_command(label='redo', accelerator='Ctrl+Y')
        edit_menu.add_separator()
        edit_menu.add_command(label='cut', accelerator='Ctrl+X')
        edit_menu.add_command(label='copy', accelerator='Ctrl+C')
        edit_menu.add_command(label='paste', accelerator='Ctrl+V')
        edit_menu.add_separator()
        edit_menu.add_command(label='find', accelerator='Ctrl+F')
        edit_menu.add_separator()
        edit_menu.add_command(label='select all', accelerator='Ctrl+A')
        menu_bar.add_cascade(label='Edit', menu=edit_menu)

        view_menu = Menu(menu_bar, tearoff=0)


        view_menu.add_checkbutton(label='line number', variable=self.is_show_line_num,
                                  )
        view_menu.add_checkbutton(label="word wrap", variable=self.enable_word_wrap)
        view_menu.add_command(label="bigger font", accelerator="Ctrl+=")
        view_menu.add_command(label="smaller font", accelerator="Ctrl+-")
        
        #font selection menu
        font_select = Menu(view_menu, tearoff=0)
        for ff in ("Source Code Pro", "Courier New","Hack", "Fira Code", "Menlo"):
            font_select.add_radiobutton(label=ff)
        
        #colour selection menu
        colour_select= Menu(view_menu, tearoff=0)
        for clr in ("black", "green", "yellow", "blue", "white"):
            colour_select.add_radiobutton(label=clr)
        
        view_menu.add_cascade(label="font..", menu=font_select)
        view_menu.add_cascade(label="background", menu=colour_select)

        menu_bar.add_cascade(label='View', menu=view_menu)


        self["menu"] = menu_bar

    def set_tabs(self):
        self.tabs = {'ky': 0}
        #Keep a record of the open tabs in a list.
        self.tab_list = []
        self.notebook = Notebook(self)
        self.notebook.pack(expand = True, fill= 'both')


    
    def cur_tab(self) -> None| editorTab:
        return self.tab_list[self.notebook.index('current')]

    def add_tab(self, name="scratch"):
        tab = editorTab(self.notebook, name)
        self.notebook.add(tab, text=name)
        self.tab_list.append(tab)
        tab.textarea.bind("<Control-o>", self.open_file)
        tab.textarea.bind("<Any-KeyPress>", self.cur_tab().update_linenum)
    def generate_tab(self):
        if self.tabs['ky'] < 20:
            self.tabs['ky'] += 1
            self.add_tab('Document ' + str(self.tabs['ky']))
    
    def handle_menu_action(self, action_type):
        {
        "undo": self.cur_tab().textarea.event_generate("<<Undo>>"),
        "redo": self.cur_tab().textarea.event_generate("<<Redo>>"),
        "copy": self.cur_tab().textarea.event_generate("<<Copy>>"),
        "cut":  self.cur_tab().textarea.event_generate("<<Cut>>"),
        "paste": self.cur_tab().textarea.event_generate("<<Paste>>")
        }[action_type]

        # self.cur_tab().textarea.config()

        if action_type != "copy":
            self.cur_tab().update_linenum()

        return "break"

editor().mainloop()