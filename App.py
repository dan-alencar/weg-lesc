import sys
import os
import customtkinter as ctk
from binary import *
from TabbedPanel import TabbedPanel
from Builder import Builder
from FileSelectionFrameList import FileSelectionFrameList
from ControllerSelectionFrameList import ControllerSelectionFrameList
from MenuFrame import MenuFrame
from PIL import Image
from tkinter import filedialog
from tkinter import messagebox


class App(ctk.CTk):
    """
    Janela principal da aplicação
    """

    def __init__(self):
        super().__init__()

        # configuração inicial da janela

        self.geometry("1400x800")
        self.resizable('true', 'true')
        self.title("Seleção de Arquivos")

        self.builder = Builder(self)

        weg_ico = 'weg-logo-5.ico'
        weg_logo = 'logo-weg.png'
        self.iconbitmap(self.get_image_path(weg_ico))
        ctk.set_appearance_mode('light')

        # frame de menu
        self.menu_frame = MenuFrame(
            self, fg_color='transparent', corner_radius=0)
        self.menu_frame.pack(fill=ctk.BOTH)

        self.logo = ctk.CTkImage(
            light_image=Image.open(self.get_image_path(weg_logo)), size=(1000, 90))
        self.logo_label = ctk.CTkLabel(self, image=self.logo, text='')
        self.logo_label.pack()

        # Menu de abas
        self.codeframe_list = FileSelectionFrameList(
            self)  # cria lista de frames de seleção
        self.controllerframe_list = ControllerSelectionFrameList(
            self)  # cria lista de frames de seleção
        self.tab_view = TabbedPanel(self)
        self.tab_view.pack(fill=ctk.BOTH, expand=ctk.TRUE)

        # Gerador do arquivo binário
        self.generate_binary = ctk.CTkButton(
            self, text="Gerar Binário", command=self.builder.gerarbinario)
        self.generate_binary.pack(pady=10, padx=10)


    def get_image_path(self, image_filename):
        if hasattr(sys, '_MEIPASS'):
            # Running as a PyInstaller executable
            return os.path.join(sys._MEIPASS, 'img', image_filename)
        else:
            # Running as a script
            return os.path.join('img', image_filename)

          
app = App()
app.mainloop()
