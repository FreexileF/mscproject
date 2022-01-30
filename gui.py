from tkinter import *
from tkinter import font
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import *
import os, re
import idlelib.colorizer as ic
import idlelib.percolator  as ip

class editorTab(Frame):
    

    def __init__(self) -> None:
        #editing area
        self.fontfamily = StringVar()
        self.fontfamily.set("Courier New")
        self.fontsize = 14
        self.textfont = font.Font(family=self.fontfamily, size=self.fontsize)
        self.bgcolour = StringVar(value= "white")
        self.filename = None


        self.textarea = scrolledtext.ScrolledText(self, wrap=WORD, undo=True, font=self.textfont)
        self.textarea.pack(expand='yes', fill='both')
        self.textarea.bind('<Control-n>', self.new_file)
        self.textarea.bind('<Control-o>', self.open_file)
        self.textarea.bind('<Control-s>', self.save)
        self.textarea.bind('<Control-a>', self.select_all)
        self.textarea.bind('<Control-f>', self.find_text)
        self.textarea.bind('<Any-KeyPress>', lambda e: self._update_line_num())
        self.textarea.bind('<Control-equal>', self.bigger_text)
        self.textarea.bind('<Control-minus>', self.smaller_text)

        #syntax hightlighting, thanks to library function.
        cdg = ic.ColorDelegator()
        ip.Percolator(self.textarea).insertfilter(cdg)

    def toggle_word_wrap(self):
        self.enable_word_wrap= not self.enable_word_wrap
        self.textarea.config(wrap= 'word' if self.enable_word_wrap else 'none')


    def set_fontface(self):
        self.textfont.config(family=self.fontfamily.get())

    def set_bgcolour(self):
        self.textarea.config(background=self.bgcolour.get())

    def smaller_text(self, event=None):
        self.fontsize -= 2
        self.textfont.config(size = self.fontsize)

    def bigger_text(self, event=None):
        self.fontsize += 2
        self.textfont.config(size = self.fontsize)




    def select_all(self, event=None):
        self.textarea.tag_add('sel', '1.0', 'end')
        return "break"

    def new_file(self, event=None):
        # self.title("scratch")
        self.textarea.delete(1.0, END)
        self.file_name = None




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
        ignore_case_value = IntVar()
        Checkbutton(search_toplevel, 
                    text='case insensitive',
                    variable=ignore_case_value).grid(
                    row=1, column=1, sticky='e', padx=2, pady=2)

        Button(search_toplevel, text="Search", command=lambda: self.search_result(
            search_entry_widget.get(), ignore_case_value.get(), search_toplevel, search_entry_widget)
               ).grid(row=0, column=2, sticky='e' + 'w', padx=2, pady=2)


        def destroy_serch():
            self.textarea.tag_remove('match', '1.0', "end"); search_toplevel.destroy()

        search_toplevel.protocol('WM_DELETE_WINDOW', destroy_serch)
        return "break"

    def search_result(self, key, ignore_case, search_toplevel, search_box):
        self.textarea.tag_remove('match', '1.0', "end")
        matches_found = 0
        if key:
            start_pos = '1.0'
            while True:
                start_pos = self.textarea.search(key, start_pos, nocase=ignore_case, stopindex="end")
                if not start_pos:
                    break
                end_pos = '{}+{}c'.format(start_pos, len(key))
                self.textarea.tag_add('match', start_pos, end_pos)
                matches_found += 1
                start_pos = end_pos
            self.textarea.tag_config('match', foreground='red', background='yellow')
        search_box.focus_set()
        search_toplevel.title('Found %d matched result.' % matches_found)



class editor(Tk):

    def __init__(self):
        super().__init__()
        self._set_window_()
        self._create_menu_bar_()



    def _set_window_(self):
        self.title("Notepad--")
        scn_width, scn_height = self.maxsize()
        wm_val = '800x600+%d+%d' % ((scn_width - 750) / 2, (scn_height - 450) / 2)
        self.geometry(wm_val)
        self.protocol('WM_DELETE_WINDOW', self.exit_editor)

        self.line_number_bar = Text(self, width=4, padx=3, takefocus=0, border=0,
                            background='#F0E68C', state='disabled')

        self.line_number_bar.pack(side='left', fill='y')

        self.tabs = {'ky': 0}
        #Keep a record of the open tabs in a list.
        self.tab_list = []
        self.notebook = Notebook(self)
        self.notebook.pack(expand = True, fill= 'both')

    def _update_line_num(self):
        if self.is_show_line_num.get():
            row, _ = self.cur_tab().textarea.index("end").split('.')
            line_num_content = "\n".join([str(i) for i in range(1, int(row))])
            self.line_number_bar.config(state='normal')
            self.line_number_bar.delete('1.0', 'end')
            self.line_number_bar.insert('1.0', line_num_content)
            self.line_number_bar.config(state='disabled')
        else:
            self.line_number_bar.config(state='normal')
            self.line_number_bar.delete('1.0', 'end')
            self.line_number_bar.config(state='disabled')

    # Return 'break' to stop event from futher spread

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
            self._update_line_num()

        return "break"
    def cur_tab(self) -> None| editorTab:
        #Get the tab object from the tab_list based on the index of the currently selected tab
        return self.tab_list[self.notebook.index('current')]

    def add_tab(self, name):
        tab = editorTab(self.notebook, name)
        self.notebook.add(tab, text=name)
        self.tab_list.append(tab)

    def generate_tab(self):
        if self.tabs['ky'] < 20:
            self.tabs['ky'] += 1
            self.add_tab('Document ' + str(self.tabs['ky']))

    def open_file(self, event=None):
        input_file = filedialog.askopenfilename()
        if input_file:
            self.title(os.path.basename(input_file))
            self.file_name = input_file
            self.cur_tab().textarea.delete(1.0, END)
            with open(input_file, 'r') as f:
                self.cur_tab().textarea.insert(1.0, f.read())

    def save(self, event=None):
        if not self.file_name:
            self.save_as()
        else:
            self.write_file(self.file_name)
    def save_as(self, event=None):
        input_file = filedialog.asksaveasfilename(
            filetypes=[("All Files", "*.*"), ("Text files", "*.txt")])
        if input_file:
            self.file_name = input_file
            self.write_file(self.file_name)

    def write_file(self, file_name):
        try:
            content = self.cur_tab().textarea.get(1.0, 'end')
            with open(file_name, 'w') as the_file:
                the_file.write(content)
            self.title("%s - Notepad--" % os.path.basename(file_name))
        except IOError:
            messagebox.showwarning("Save", "File saving failed")

    def _create_menu_bar_(self):


        #Useful variables for view menu
        self.is_show_line_num = IntVar()
        self.is_show_line_num.set(1)
        self.enable_word_wrap = BooleanVar()
        self.enable_word_wrap.set(False)

        menu_bar = Menu(self)
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label='New', command=self.new_file)
        file_menu.add_command(label='Open...', accelerator='Ctrl+O', command=self.open_file)
        file_menu.add_command(label='Save', accelerator='Ctrl+S', command=self.save)
        file_menu.add_command(label='Save as...', accelerator='Shift+Ctrl+S', command=self.save_as)

        menu_bar.add_cascade(label='File', menu=file_menu)

        edit_menu = Menu(menu_bar, tearoff=0)



        edit_menu.add_command(label='undo', accelerator='Ctrl+Z', command=self.handle_menu_action('undo'))
        edit_menu.add_command(label='redo', accelerator='Ctrl+Y', command=self.handle_menu_action('redo'))
        edit_menu.add_separator()
        edit_menu.add_command(label='cut', accelerator='Ctrl+X', command= self.handle_menu_action('cut'))
        edit_menu.add_command(label='copy', accelerator='Ctrl+C', command= self.handle_menu_action('copy'))
        edit_menu.add_command(label='paste', accelerator='Ctrl+V', command= self.handle_menu_action('paste'))
        edit_menu.add_separator()
        edit_menu.add_command(label='find', accelerator='Ctrl+F', command=self.cur_tab().find_text)
        edit_menu.add_separator()
        edit_menu.add_command(label='select all', accelerator='Ctrl+A', command=self.cur_tab().select_all)
        menu_bar.add_cascade(label='Edit', menu=edit_menu)

        view_menu = Menu(menu_bar, tearoff=0)


        view_menu.add_checkbutton(label='line number', variable=self.is_show_line_num,
                                  command=self._update_line_num)
        view_menu.add_checkbutton(label="word wrap", variable=self.enable_word_wrap, command=self.cur_tab().toggle_word_wrap)
        view_menu.add_command(label="bigger font", accelerator="Ctrl+=", command=self.cur_tab().igger_text)
        view_menu.add_command(label="smaller font", accelerator="Ctrl+-", command=self.cur_tab().smaller_text)
        
        #font selection menu
        font_select = Menu(view_menu, tearoff=0)
        for ff in ("Source Code Pro", "Courier New","Hack", "Fira Code", "Menlo"):
            font_select.add_radiobutton(label=ff, variable=self.cur_tab().fontfamily, value=ff, command= self.cur_tab().set_fontface)
        
        #colour selection menu
        colour_select= Menu(view_menu, tearoff=0)
        for clr in ("black", "green", "yellow", "blue", "white"):
            colour_select.add_radiobutton(label=clr, variable=self.cur_tab().bgcolour, value=clr, command=self.cur_tab().set_bgcolour)
        
        view_menu.add_cascade(label="font..", menu=font_select)
        view_menu.add_cascade(label="background", menu=colour_select)

        menu_bar.add_cascade(label='View', menu=view_menu)


        self["menu"] = menu_bar
    def exit_editor(self):
        if messagebox.askokcancel("D"):
            self.destroy()
editor().mainloop()