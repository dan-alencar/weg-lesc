from tkinter import filedialog
from dictionary import rlmomery_enum
import customtkinter as ctk
import tkinter as tk
from PIL import Image


# Classe: ConfigurationFrame
# Descrição: Cria um novo frame com widgets para seleção de arquivos.
class ConfigurationFrame(ctk.CTkFrame):
    # Método: __init__
    # Parâmetros de Entrada: master (janela principal), **kwargs (parâmetros adicionais)
    # Operação: Inicializa o frame e configura widgets para seleção de arquivos.
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Campo de texto que exibe o path do arquivo selecionado
        self.endadd_label = ctk.CTkLabel(self, height=30, width=100, text="RL78 Part Memory Size:", font=("", 12, "bold"))
        self.endadd_label.pack(padx=5, pady=5)

        self.endadd_var = ctk.StringVar(value="Part Number")
        self.endadd_fam = ctk.CTkOptionMenu(self, dynamic_resizing=False, height=35, width=125,
                                           values=["A", "C", "D", "E", "F", "G", "H", "J", "K", "L"], command=self.dropdown_callback, variable=self.endadd_var)
        self.endadd_fam.pack(padx=5, pady=5)
        self.file_label = ctk.CTkLabel(self, height=30, width=100, text="Arquivo do Bootloader:",
                                            font=("", 12, "bold"))
        self.file_label.pack(padx=5, pady=5)

        # botão para abrir a seleção de arquivos
        img_file = master.master.master.get_image_path('pathicon.png')
        fileicon = ctk.CTkImage(Image.open(img_file), size=(25, 25))
        self.btn = ctk.CTkButton(self, text="", image=fileicon, height=35, width=50,
                                 font=('', 14, 'bold'), command=self.chooseFile)

        # campo de texto que exibe o path do arquivo selecionado
        self.file_entry = ctk.CTkEntry(self, state=ctk.DISABLED, placeholder_text="Local do arquivo", width=300)
        self.file_entry.pack(pady=5, padx=5)
        self.btn.pack(pady=5, padx=5)

    # Método: chooseFile
    # Parâmetros de Entrada: Nenhum
    # Operação: Permite a seleção de arquivos .txt e .hex.
    def chooseFile(self):
        '''
        Permite a seleção de arquivos .txt e .hex
        '''
        # self.length.configure(state=ctk.NORMAL)
        self.file_entry.configure(state=ctk.NORMAL)
        self.filename = filedialog.askopenfilename(initialdir=self.master.master.master.previous_path, title="Selecione o arquivo do seu firmware", filetypes=[
            ("Arquivos .mot", "*.mot")])
        if self.filename != '':
            self.master.master.master.previous_path = self.filename
        print(self.filename)
        if self.filename == '':
            self.file_entry.configure(state=ctk.DISABLED)
            return
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(0, self.filename)
        self.file_entry.configure(state=ctk.DISABLED)


    # Método: clearFields
    # Parâmetros de Entrada: Nenhum
    # Operação: Limpa os campos de entrada do frame.
    def clearFields(self):
        self.file_entry.delete('0', ctk.END)

    def dropdown_callback(self, choice):
        self.endadd_var = rlmomery_enum[choice]
        print(self.endadd_var)