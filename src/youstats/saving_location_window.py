import os
from pathlib import Path

import customtkinter as ctk

class SavingLocationWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title(' Select saving location')
        self.geometry('300x185')
        self.resizable(False, False)
        self.configure(bg='#222629')
        self.after(250, lambda: self.iconbitmap(os.path.join(Path(__file__).resolve().parent.parent.parent,
                                                             'resources', 'Save.ico')))


