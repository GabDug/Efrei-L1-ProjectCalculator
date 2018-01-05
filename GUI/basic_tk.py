import os
import sys
import tkinter as tk
import tkinter.ttk as ttk
from threading import Lock
from tkinter import TOP, BOTH, END, INSERT, SEL, SEL_FIRST, SEL_LAST
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

from eval_global import ext_eval_global
import logger_conf

logger = logger_conf.Log.logger


class Console(ScrolledText):
    def __init__(self, parent):
        """Initialize our console, that inherits from ScrollText
         (which is just a tk.Text and Scrollbar)."""
        self.parent = parent
        ScrolledText.__init__(self, self.parent)


class App(ttk.Frame):
    def __init__(self, parent):
        """Cadre principal. Contient les divers widgets ainsi que les attributs nécessaires à l'application.
        connexion_stream et connexion_statique permettent d'activer ou de désactiver les deux types de connexion
         pour travailler ur la mise en page sans se faire bloquer par les limitations."""
        # On définit le cadre dans l'objet App (inutile car pas kwargs**...)
        ttk.Frame.__init__(self, parent)
        self.parent = parent

        self.console = Console(self)
        self.console.pack(fill=tk.BOTH, expand=True)
        self.console.focus_set()

root = tk.Tk()
root.title('Project Calculator')

app = App(root)
app.pack()

root.mainloop()
