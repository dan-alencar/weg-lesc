from tkinter import filedialog

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
        self.prodver_label = ctk.CTkLabel(self, height=30, width=100, text="Versão:", font=("", 12, "bold"))
        self.prodver_label.pack(padx=5, pady=5)

        self.prodver_entry = ctk.CTkEntry(self, placeholder_text="Ex: V2.01", width=160)
        self.prodver_entry.pack(padx=5, pady=5)

        self.file_label = ctk.CTkLabel(self, height=30, width=100, text="Arquivo do Bootloader:",
                                            font=("", 12, "bold"))
        self.file_label.pack(padx=5, pady=5)

        # botão para abrir a seleção de arquivos
        img_file = master.master.master.get_image_path('pathicon.png')
        fileicon = ctk.CTkImage(Image.open(img_file), size=(25, 25))
        self.btn = ctk.CTkButton(self, text="", image=fileicon, height=35, width=50,
                                 font=('', 14, 'bold'), command=self.chooseFile)
        self.btn.pack(pady=5, padx=5)

        # campo de texto que exibe o path do arquivo selecionado
        self.file_entry = ctk.CTkEntry(self, state=ctk.DISABLED, placeholder_text="Local do arquivo", width=160)
        self.file_entry.pack(pady=5, padx=5)

    # Método: chooseFile
    # Parâmetros de Entrada: Nenhum
    # Operação: Permite a seleção de arquivos .txt e .hex.
    def chooseFile(self):
        '''
        Permite a seleção de arquivos .txt e .hex
        '''
        # self.length.configure(state=ctk.NORMAL)
        self.file_entry.configure(state=ctk.NORMAL)
        self.filename = filedialog.askopenfilename(title="Selecione o arquivo do seu firmware", filetypes=[
            ("Arquivos .mot", "*.mot")])
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
        self.prodver_entry.delete('0', ctk.END)
        self.file_entry.delete('0', ctk.END)
