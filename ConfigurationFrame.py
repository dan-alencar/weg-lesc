import customtkinter as ctk
import tkinter as tk

class ConfigurationFrame(ctk.CTkFrame):
    '''
    Cria novo frame com widgets para seleção de arquivos 
    '''

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # validate_length = self.register((self.validate_input), "%P")
        
        #configuração do grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=2)
        self.columnconfigure(3, weight=1)
        
        # campo de texto que exibe o path do arquivo selecionado        
        self.headver_label = ctk.CTkLabel(self, height=100, width=100, text="Cabeçalho:")
        self.headver_label.grid(column = 1, row = 0, sticky = tk.E, padx = 5, pady = 5)
        
        self.header_version = ctk.CTkEntry(self)
        self.header_version.grid(column = 2, row = 0, sticky = tk.W, padx = 5, pady = 5)
        
        self.headval_label = ctk.CTkLabel(self, height=100, width=100, text="Validação:")
        self.headval_label.grid(column = 1, row = 1, sticky = tk.E, padx = 5, pady = 5)
        
        self.header_valid = ctk.CTkEntry(self)
        self.header_valid.grid(column = 2, row = 1, sticky = tk.W, padx = 5, pady = 5)
        
        self.prodID_label = ctk.CTkLabel(self, height=100, width=100, text="Produto:")
        self.prodID_label.grid(column = 1, row = 2, sticky = tk.E, padx = 5, pady = 5)
        
        self.prod_id = ctk.CTkEntry(self)
        self.prod_id.grid(column = 2, row = 2, sticky = tk.W, padx = 5, pady = 5)
        
        self.prodVer_label = ctk.CTkLabel(self, height=100, width=100, text="Versão:")
        self.prodVer_label.grid(column = 1, row = 3, sticky = tk.E, padx = 5, pady = 5)
        
        self.prod_ver = ctk.CTkEntry(self)
        self.prod_ver.grid(column = 2, row = 3, sticky = tk.W, padx = 5, pady = 5)
        
    def clearFields(self):
        self.header_version.delete('0', ctk.END)
        self.header_valid.delete('0', ctk.END)
        self.prod_id.delete('0', ctk.END)
        self.prod_ver.delete('0', ctk.END)