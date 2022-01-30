
from tkinter import *
import tkinter
from tkinter import font
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinter.ttk import *
import os
from tracemalloc import start

class editorTab(Frame):
    def __init__(self, root, name) -> None:
        Frame.__init__(self,root)

        self.root = root
        self.name = name

        self.fontfamily = StringVar()
        self.fontfamily.set("Courier New")
        self.fontsize = 14
        self.textfont = font.Font(family=self.fontfamily, size=self.fontsize)
        self.bgcolour = StringVar(value= "white")


        self.line_number_bar = Text(self, width=4, padx=3, takefocus=0, border=0,
                            background='#F0E68C', state='disabled', font=self.textfont)
        self.line_number_bar.pack(side='left', fill='y')    

        # self.textarea = scrolledtext.ScrolledText(self, wrap=WORD, undo=True, font=self.textfont)
        self.textarea = Text(self, wrap="word", undo=True, font=self.textfont)
        self.textarea.pack(expand="yes", fill="both")
        
        t_scrlbar=Scrollbar(self.textarea, orient=VERTICAL)
        t_scrlbar['command'] = self.scrollboth
        #well this seems a bit unusual, because the following statement must 
        #apper BEFORE registering the scrollbar to window manager

        self.textarea["yscrollcommand"]=t_scrlbar.set
        t_scrlbar.pack(side="right", fill='y')

    def set_bind(self):

            self.textarea.bind("<Control-a>", self.sel_all)
            # self.textarea.bind("<Control-x>", self.)

    def scrollboth(self, *args):
        self.textarea.yview(*args)
        self.line_number_bar.yview(*args)


    def update_linenum(self, show=True):
        if show:
            row, _ = self.textarea.index("end").split('.')
            line_num_content = "\n".join([str(i) for i in range(1, int(row))])
            self.line_number_bar.config(state='normal')
            self.line_number_bar.delete('1.0', 'end')
            self.line_number_bar.insert('1.0', line_num_content)
            self.line_number_bar.config(state='disabled')
        else:
            self.line_number_bar.config(state='normal')
            self.line_number_bar.delete('1.0', 'end')
            self.line_number_bar.config(state='disabled')    
        
    def find_text(self, event=None):
        search_toplevel = Toplevel(self)
        search_toplevel.title('Search')
        #On top of other windows
        search_toplevel.transient(self)
        search_toplevel.resizable(False, False)
        Label(search_toplevel, text="Search:").grid(row=0, column=0, sticky='e')
        search_entry_widget = Entry(search_toplevel, width=25)
        search_entry_widget.grid(row=0, column=1, padx=2, pady=2, sticky='we')
        search_entry_widget.focus_set()
        case_sensitive = IntVar()
        Checkbutton(search_toplevel, 
                    text='case insensitive',
                    variable=case_sensitive).grid(
                    row=1, column=1, sticky='e', padx=2, pady=2)

        Button(
            search_toplevel, 
            text="Search",
            command= lambda: self.search_result(
                search_entry_widget.get(), 
                case_sensitive.get(), 
                search_toplevel, 
                search_entry_widget)
                ).grid(row=0, column=2, sticky='e' + 'w', padx=2, pady=2)

        def close_search_window():
            self.textarea.tag_remove('match', '1.0', "end")
            search_toplevel.destroy()

        search_toplevel.protocol('WM_DELETE_WINDOW', close_search_window)

    def search_result(self, key, ignore_case, search_toplevel, search_box):
        self.textarea.tag_remove('match', '1.0', "end")
        matches_found = 0
        if key:
            start_pos = "1.0"
            while True:
                start_pos = self.textarea.search(key, start_pos, nocase=ignore_case, stopindex="end")
                print("start pos=%s" % start_pos)
                if not start_pos:
                    break
                end_pos = '{}+{}c'.format(start_pos, len(key))
                self.textarea.tag_add('match', start_pos, end_pos)
                matches_found += 1
                start_pos = end_pos
            self.textarea.tag_config('match', foreground='green', background='yellow')
        search_box.focus_set()
        search_toplevel.title('Found %d matched result.' % matches_found)
    
    def sel_all(self, event=None):
        self.textarea.tag_add('sel', '1.0', 'end')
        return "break"
class editor(Tk):
    def __init__(self) -> None:
        super().__init__()
        self.set_window()
        self.set_tabs()
        #add a tab
        self.add_tab()
        self.create_menu_bar()
        

    def open_file(self, event="None"):
        input_file = filedialog.askopenfilename()
        fname = os.path.basename(input_file)
        if input_file:
            self.cur_tab().textarea.delete(1.0, END)

            # self.cur_tab().name=fname
            self.notebook.tab(self.cur_tab(), text=fname)
            # self.add_tab(input_file)
            # self.notebook.select(END)
            # self.cur_tab().textarea.delete(1.0, END)
            with open(input_file, 'r') as f:
                self.cur_tab().textarea.insert(1.0, f.read())
                self.cur_tab().update_linenum()

    def cur_textarea(self):
        return self.cur_tab().textarea

    def save(self, event=None):
        if not self.cur_tab().name:
            self.save_as()
        else:
            self.write_file(self.cur_tab().name())
    
    def save_as(self, event=None):
        input_file = filedialog.asksaveasfilename(
            filetypes=[("All Files", "*.*"), ("Text files", "*.txt")])
        if input_file:
            self.notebook.tab(self.cur_tab(), text= input_file)
            self.write_file(self.cur_tab().name)

    def write_file(self, file_name):
        try:
            content = self.cur_tab().textarea.get(1.0, 'end')
            with open(file_name, 'w') as f:
                f.write(content)
        except IOError:
            pass

    def exit_editor(self):
        if self.cur_tab().textarea.edit_modified():
            if messagebox.askokcancel(title="Exit", message="Modified files exits, exit anyway?"):
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
        edit_menu.add_command(label='redo', command=self.handle_menu_action('redo'), accelerator='Ctrl+Y')
        edit_menu.add_separator()
        edit_menu.add_command(label='cut',command=self.handle_menu_action("cut"), accelerator='Ctrl+X')
        edit_menu.add_command(label='copy', command=self.handle_menu_action("copy"), accelerator='Ctrl+C')
        edit_menu.add_command(label='paste', command=self.handle_menu_action('paste'), accelerator='Ctrl+V')
        edit_menu.add_separator()
        edit_menu.add_command(label='find', command=self.cur_tab().find_text, accelerator='Ctrl+F')
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
        self.notebook = ttk.Notebook(self)

        self.notebook.pack(expand = True, fill= 'both')


    
    def cur_tab(self) -> None| editorTab:
        return self.tab_list[self.notebook.index('current')]

    def add_tab(self, name="scratch"):
        tab = editorTab(self.notebook, name)
        self.notebook.add(tab, text=name)
        self.tab_list.append(tab)

        # tab.textarea.bind("<Any-KeyPress>", self.cur_tab().update_linenum)
    
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