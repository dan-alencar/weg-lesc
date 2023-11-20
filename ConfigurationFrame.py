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
        self.columnconfigure(2, weight=1)
        
        # campo de texto que exibe o path do arquivo selecionado        
        self.headver_label = ctk.CTkLabel(self, height=30, width=100, text="Cabeçalho:", font=("", 12, "bold"))
        self.headver_label.grid(column = 1, row = 0, sticky = tk.S, padx = 5, pady = 5)
        
        self.header_version = ctk.CTkEntry(self, placeholder_text="Ex: 02", width=160)
        self.header_version.grid(column = 1, row = 1, sticky = tk.N, padx = 5, pady = 5)
        
        self.headval_label = ctk.CTkLabel(self, height=30, width=100, text="Validação:", font=("", 12, "bold"))
        self.headval_label.grid(column = 1, row = 2, sticky = tk.S, padx = 5, pady = 5)
        
        self.header_valid = ctk.CTkEntry(self, placeholder_text="Ex: 00", width=160)
        self.header_valid.grid(column = 1, row = 3, sticky = tk.N, padx = 5, pady = 5)
        
        self.prodID_label = ctk.CTkLabel(self, height=30, width=100, text="Produto:", font=("", 12, "bold"))
        self.prodID_label.grid(column = 1, row = 4, sticky = tk.S, padx = 5, pady = 5)
        
        self.prod_id = ctk.CTkEntry(self, placeholder_text="Ex: WECC300", width=160)
        self.prod_id.grid(column = 1, row = 5, sticky = tk.N, padx = 5, pady = 5)
        
        self.prodVer_label = ctk.CTkLabel(self, height=30, width=100, text="Versão:", font=("", 12, "bold"))
        self.prodVer_label.grid(column = 1, row = 6, sticky = tk.S, padx = 5, pady = 5)
        
        self.prod_ver = ctk.CTkEntry(self, placeholder_text="Ex: V2.01", width=160)
        self.prod_ver.grid(column = 1, row = 7, sticky = tk.N, padx = 5, pady = 5)
        
    def clearFields(self):
        self.header_version.delete('0', ctk.END)
        self.header_valid.delete('0', ctk.END)
        self.prod_id.delete('0', ctk.END)
        self.prod_ver.delete('0', ctk.END)