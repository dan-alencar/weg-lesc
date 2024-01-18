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

        # Configuração do grid
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=3)


        # Campo de texto que exibe o path do arquivo selecionado
        self.exch_mode_label = ctk.CTkLabel(self, height=30, width=100, text="Exchange mode:", font=("", 12, "bold"))
        self.exch_mode_label.grid(column=1, row=0, sticky=tk.S, padx=5, pady=5)

        self.exch_mode_entry = ctk.CTkEntry(self, placeholder_text="Ex: 02", width=160)
        self.exch_mode_entry.grid(column=1, row=1, sticky=tk.N, padx=5, pady=5)

        self.fw_rev_label = ctk.CTkLabel(self, height=30, width=100, text="UPS Firmware Revision:", font=("", 12, "bold"))
        self.fw_rev_label.grid(column=2, row=0, sticky=tk.S, padx=5, pady=5)

        self.fw_rev_entry = ctk.CTkEntry(self, placeholder_text="Ex: 00", width=160)
        self.fw_rev_entry.grid(column=2, row=1, sticky=tk.N, padx=5, pady=5)

        self.vecstart_add_label = ctk.CTkLabel(self, height=30, width=100, text="End. inicial Vector:", font=("", 12, "bold"))
        self.vecstart_add_label.grid(column=1, row=2, sticky=tk.S, padx=5, pady=5)

        self.vecstart_entry = ctk.CTkEntry(self, placeholder_text="Ex: WECC300", width=160)
        self.vecstart_entry.grid(column=1, row=3, sticky=tk.N, padx=5, pady=5)

        self.vecend_label = ctk.CTkLabel(self, height=30, width=100, text="End. final Vector:", font=("", 12, "bold"))
        self.vecend_label.grid(column=2, row=2, sticky=tk.S, padx=5, pady=5)

        self.vecend_entry = ctk.CTkEntry(self, placeholder_text="Ex: V2.01", width=160)
        self.vecend_entry.grid(column=2, row=3, sticky=tk.N, padx=5, pady=5)

        self.addstart_label = ctk.CTkLabel(self, height=30, width=100, text="Endereço inicial:", font=("", 12, "bold"))
        self.addstart_label.grid(column=1, row=4, sticky=tk.S, padx=5, pady=5)

        self.addstart_entry = ctk.CTkEntry(self, placeholder_text="Ex: 02", width=160)
        self.addstart_entry.grid(column=1, row=5, sticky=tk.N, padx=5, pady=5)

        self.addend_label = ctk.CTkLabel(self, height=30, width=100, text="Endereço final:", font=("", 12, "bold"))
        self.addend_label.grid(column=2, row=4, sticky=tk.S, padx=5, pady=5)

        self.addend_entry = ctk.CTkEntry(self, placeholder_text="Ex: 00", width=160)
        self.addend_entry.grid(column=2, row=5, sticky=tk.N, padx=5, pady=5)

        self.addcrc_label = ctk.CTkLabel(self, height=30, width=100, text="Endereço do CRC:", font=("", 12, "bold"))
        self.addcrc_label.grid(column=1, row=6, sticky=tk.S, padx=5, pady=5)

        self.addcrc_entry = ctk.CTkEntry(self, placeholder_text="Ex: WECC300", width=160)
        self.addcrc_entry.grid(column=1, row=7, sticky=tk.N, padx=5, pady=5)

        self.numslaves_label = ctk.CTkLabel(self, height=30, width=100, text="Num. de servos:", font=("", 12, "bold"))
        self.numslaves_label.grid(column=2, row=6, sticky=tk.S, padx=5, pady=5)

        self.numslaves_entry = ctk.CTkEntry(self, placeholder_text="Ex: V2.01", width=160)
        self.numslaves_entry.grid(column=2, row=7, sticky=tk.N, padx=5, pady=5)

        self.exch_mode_slaves_label = ctk.CTkLabel(self, height=30, width=100, text="Exch. mode dos servos:", font=("", 12, "bold"))
        self.exch_mode_slaves_label.grid(column=1, row=8, sticky=tk.S, padx=5, pady=5)

        self.exch_mode_slaves_entry = ctk.CTkEntry(self, placeholder_text="Ex: 02", width=160)
        self.exch_mode_slaves_entry.grid(column=1, row=9, sticky=tk.N, padx=5, pady=5)

        self.prodver_label = ctk.CTkLabel(self, height=30, width=100, text="Versão:", font=("", 12, "bold"))
        self.prodver_label.grid(column=2, row=8, sticky=tk.S, padx=5, pady=5)

        self.prodver_entry = ctk.CTkEntry(self, placeholder_text="Ex: V2.01", width=160)
        self.prodver_entry.grid(column=2, row=9, sticky=tk.N, padx=5, pady=5)

        self.zeroblock_label = ctk.CTkLabel(self, height=30, width=100, text="Endereço da Static:", font=("", 12, "bold"))
        self.zeroblock_label.grid(column=1, row=10, sticky=tk.S, padx=5, pady=5)

        self.zeroblock_entry = ctk.CTkEntry(self, placeholder_text="Ex: 02", width=160)
        self.zeroblock_entry.grid(column=1, row=11, sticky=tk.N, padx=5, pady=5)

        self.file_label = ctk.CTkLabel(self, height=30, width=100, text="Arquivo do Bootloader:",
                                            font=("", 12, "bold"))
        self.file_label.grid(column=2, row=10, sticky=tk.S, padx=5, pady=5)

        # botão para abrir a seleção de arquivos
        img_file = master.master.master.get_image_path('pathicon.png')
        fileicon = ctk.CTkImage(Image.open(img_file), size=(25, 25))
        self.btn = ctk.CTkButton(self, text="", image=fileicon, height=35, width=50,
                                 font=('', 14, 'bold'), command=self.chooseFile)
        self.btn.grid(column=3, row=11, pady=5, padx=5, sticky=tk.W)

        # campo de texto que exibe o path do arquivo selecionado
        self.file_entry = ctk.CTkEntry(self, state=ctk.DISABLED, placeholder_text="Local do arquivo", width=160)
        self.file_entry.grid(column=2, row=11, pady=5, padx=5)

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
        if self.filename=='':
            self.file_entry.configure(state=ctk.DISABLED)
            return
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(0, self.filename)
        self.file_entry.configure(state=ctk.DISABLED)


    # Método: clearFields
    # Parâmetros de Entrada: Nenhum
    # Operação: Limpa os campos de entrada do frame.
    def clearFields(self):
        self.exch_mode_entry.delete('0', ctk.END)
        self.fw_rev_entry.delete('0', ctk.END)
        self.vecstart_entry.delete('0', ctk.END)
        self.vecend_entry.delete('0', ctk.END)
        self.addstart_entry.delete('0', ctk.END)
        self.addend_entry.delete('0', ctk.END)
        self.addcrc_entry.delete('0', ctk.END)
        self.numslaves_entry.delete('0', ctk.END)
        self.exch_mode_slaves_entry.delete('0', ctk.END)
        self.prodver_entry.delete('0', ctk.END)
