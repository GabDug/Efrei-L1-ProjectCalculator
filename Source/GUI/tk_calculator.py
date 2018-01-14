# PYTKCON by Samy (samyzaf) [https://github.com/samyzaf/pytkcon]
# The code is free to use, used to be a Python console but has been simplified

import tkinter as tk
from threading import Lock
from tkinter import TOP, BOTH, END, INSERT, SEL, SEL_FIRST, SEL_LAST
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

from eval_global import ext_eval_global

import logger_conf

logger = logger_conf.Log.logger


class TkConsole(ScrolledText):
    """Tk console widget which can be easily embedded withing tkinter widgets"""

    def __init__(self, master=None, **opt):
        opt.setdefault('width', 80)
        opt.setdefault('height', 24)
        opt.setdefault('background', 'gray92')  # 'cornsilk', 'FloralWhite'
        opt.setdefault('foreground', 'DarkGreen')
        opt.setdefault('font', ('Consolas', 9, 'normal'))
        self.initfile = opt.pop('initfile', None)
        self.history = []
        self.write_lock = Lock()

        ScrolledText.__init__(self, master, **opt)
        self.pack(side=TOP, fill=BOTH, expand=True)
        self._prompt = "? "
        self.text_init(opt)
        self.bindings()
        self.prompt()
        self.write_end("Welcome to Expression Evaluator: Cheap Edition.\nUse \"exit\" to exit console.\n",
                       ('welcome',))
        self.focus_set()

    def text_init(self, opt):
        prompt_font = opt['font'][0:2] + ('bold',)

        self.tag_config('prompt', font=prompt_font, foreground='maroon')
        self.tag_config('output', foreground='DarkGreen')
        self.tag_config('error', foreground='red')
        self.tag_config('welcome', foreground='DarkGreen')
        self.tag_config('cmd', foreground='tan4')

    def bindings(self):
        self.bind("<Return>", self.on_Return)
        # self.bind("<KeyRelease-Return>", self.on_Return)
        self.bind("<Shift-KeyRelease-Return>", self.on_Return)
        self.bind("<KeyRelease-Up>", self.on_Up)
        self.bind("<BackSpace>", self.on_BackSpace)
        self.bind("<Delete>", self.on_Delete)
        self.bind("<Key>", self.on_Key)
        self.bind("<Control-l>", self.clear)
        self.bind("<Enter>", self.focus)

    def run(self, cmd=None):
        # line,char = self.index('end').split('.')
        # last_line = self.index('end').split('.')[0]
        # print(self.index('limit'), self.index(INSERT))
        self.tag_add('cmd', 'limit', "%s-1c" % INSERT)
        if cmd is None:
            cmd = self.get('limit', END).lstrip()
            # print(cmd)
            self.history.append(cmd)
        self.eval(cmd)
        self.prompt()

    def eval(self, cmd):
        try:
            e = ext_eval_global(cmd)
            # e = eval(cmd)
            # self.write(END, '\n')
            if e is not None:
                self.write(END, e, ('output',))
        except Exception as e:
            self.write(END, "%s\n" % e, ('error',))

    def prompt(self):
        # self.tag_delete('prompt')
        # self.tag_remove('prompt', 1.0, END)
        if len(get_last_line(self)):
            self.write(END, '\n')
        self.write(END, self._prompt, ('prompt',))
        self.mark_set(INSERT, END)
        # self.mark_set('limit', INSERT)
        self.mark_set('limit', '%s-1c' % INSERT)
        self.see(END)

    def write(self, index, chars, *args):
        self.write_lock.acquire()
        self.insert(index, chars, *args)
        # self.see(index)
        self.write_lock.release()

    def write_end(self, txt, tag):
        l1, c1 = index_to_tuple(self, "%s-1c" % END)
        l2, c2 = index_to_tuple(self, 'limit')
        if l1 == l2:
            self.write('limit-3c', txt, (tag,))
        else:
            self.write('end', txt, (tag,))
        self.see('end')

    def writeline(self, txt, tag):
        txt += '\n'
        self.write_end(txt, tag)

    def on_BackSpace(self, event=None):
        # print(self.get('1.0', 'limit'))
        # print(event.keysym)
        # print(self.mark_names())
        if self.tag_nextrange(SEL, '1.0', END) and self.compare(SEL_FIRST, '>=', 'limit'):
            self.delete(SEL_FIRST, SEL_LAST)
        elif self.compare(INSERT, '!=', '1.0') and self.compare(INSERT, '>', 'limit+1c'):
            self.delete('%s-1c' % INSERT)
            self.see(INSERT)
        return "break"

    def on_Delete(self, event=None):
        # print(event.keysym)
        # print(self.mark_names())
        if self.tag_nextrange(SEL, '1.0', END) and self.compare(SEL_FIRST, '>=', 'limit'):
            self.delete(SEL_FIRST, SEL_LAST)
        elif self.compare(INSERT, '>', 'limit+1c'):
            self.delete('%s-1c' % INSERT)
            self.see(INSERT)
        return "break"

    def on_Return(self, event=None):
        modifiers = event_modifiers(event)
        # print(event.keysym, modifiers)
        if self.compare(INSERT, '<', 'limit'):
            if 'Shift' in modifiers:
                return "break"
            if 'Control' in modifiers:
                return "break"
            cmd = self.get_cur_cmd()
            # print("cmd=", cmd, "limit=", self.index('limit'))
            if cmd:
                self.insert_cmd(cmd)
                return "break"
        else:
            if 'Shift' in modifiers or 'Control' in modifiers:
                return
            self.mark_set(INSERT, END)
            self.write(END, '\n')
            self.run()
        return "break"

    def on_Key(self, event=None):
        modifiers = event_modifiers(event)
        special = ['x', 'v', 'd', 'h', 'i', 'k', 'o']
        if 'Control' in modifiers or 'Alt' in modifiers:
            if self.compare(INSERT, '<=', 'limit'):
                if event.keysym in special:
                    return "break"
                return
        elif self.compare(INSERT, '<=', 'limit'):
            if event.char:
                return "break"

    def on_Up(self, event=None):
        pos = self.tag_prevrange('cmd', INSERT, '1.0')
        if not pos:
            return
        idx1, idx2 = pos
        l1, c1 = index_to_tuple(self, idx1)
        idx = str(l1) + '.end'
        self.mark_set(INSERT, idx)
        self.see(INSERT)
        # self.prompt()
        return

    def insert_cmd(self, cmd):
        self.delete('limit+1c', END)
        self.write(END, cmd, ('cmd',))
        self.mark_set(INSERT, END)
        self.see(END)

    def get_cur_cmd(self):
        ranges = self.tag_ranges('cmd')
        ins = "%s-1c" % INSERT
        for i in range(0, len(ranges), 2):
            start = ranges[i]
            stop = ranges[i + 1]
            # print(repr(self.get(start, stop)))
            # print(index_to_tuple(self, start), index_to_tuple(self, ins), index_to_tuple(self, stop))
            if self.compare(start, '<=', ins) and self.compare(ins, '<=', stop):
                return self.get(start, stop).lstrip()
        return ""

    def _print(self, txt):
        self.tag_add('cmd', 'limit', "%s-1c" % END)
        self.write(END, '\n')
        self.write(END, txt)
        self.prompt()
        # self.insert_cmd(cmd)

    def clear(self, event=None):
        self.delete(1.0, END)
        self.prompt()

    def focus(self, event=None):
        self.focus_set()

    def none(self, event=None):
        pass


def event_modifiers(event):
    modifiers = []
    if event.state & 0x00001:
        modifiers.append('Shift')
    if event.state & 0x00004:
        modifiers.append('Control')
    if event.state & 0x20000:
        modifiers.append('Alt')
    if event.state & 0x00002:
        modifiers.append('Caps_Lock')
    if event.state & 0x00400:
        modifiers.append('Right_Down')
    if event.state & 0x00200:
        modifiers.append('Middle_Down')
    return modifiers


def index_to_tuple(text, index):
    return tuple(map(int, text.index(index).split(".")))


def tuple_to_index(t):
    l, c = t
    return str(l) + '.' + str(c)


def get_last_line(text):
    li, c = index_to_tuple(text, END)
    li -= 1
    start = tuple_to_index((li, 0))
    end = str(li) + ".end"
    return text.get(start, end)


class TkApp(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master, relief=tk.SUNKEN, bd=2)

        self.menubar = tk.Menu(self)

        menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Project Calculator", menu=menu)
        menu.add_command(label="About", command=self.about)
        menu.add_command(label="Exit", command=self.exit)

        menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Clear", menu=menu)
        menu.add_command(label="Are you sure to clear?", command=self.clear)

        self.master.config(menu=self.menubar)
        self.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.tkcon = TkConsole(self, height=12)
        self.tkcon.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.tkcon.focus_set()

    def exit(self):
        answer = messagebox.askyesno(
            "Exit?",
            "Are you sure you want to exit?"
        )
        if answer:
            self.master.destroy()

    def clear(self):
        self.tkcon.clear()


    def about(self):
        messagebox.showinfo(
            "About Project Calculator",
            "This project was created by Gabriel Dugny and Thibault Lepez.\n"
            "For the GUI we used pytkcon by samyzaf (Open source library)."
        )


def tk_app_calculator():
    root = tk.Tk()
    app = TkApp(root)
    app.pack()
    app.master.wm_title('Project Calculator')
    root.mainloop()


tk_app_calculator()
