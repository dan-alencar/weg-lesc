import customtkinter as ctk
from tkinter import filedialog
import tkinter as tk
from PIL import Image
from FileSelectionFrameList import FileSelectionFrameList
from binary import mot_to_binary
from dictionary import micro_enum

class FileSelectionFrame(ctk.CTkFrame):
    '''
    Cria novo frame com widgets para seleção de arquivos 
    '''

    def __init__(self, master, repository, index, **kwargs):
        super().__init__(master, **kwargs)
        
        # guarda a lista de frames do app
        validate_length = self.register((self.validate_input), "%P")
        self.repository = repository
        self.index = index
        self.name = "FW " + str(self.index + 1)
        
        #label para identificar o código na tela de seleção
        self.label = ctk.CTkLabel(self, text = self.name)
        self.label.pack(padx=10, pady=15, side=ctk.LEFT, anchor=ctk.N)
        
        # checkbox
        self.checkbox = ctk.CTkCheckBox(
            self, text='', height=35, width=25, command=self.toggleCheckbox)
        self.checkbox.pack(padx=10, pady=10, side=ctk.LEFT, anchor=ctk.N)

        # primeira entrada de texto (endereço)
        self.length = ctk.CTkEntry(
            self, state=ctk.DISABLED, height=35, width=70)
        self.length.pack(expand=True, padx=10, pady=10,
                          side=ctk.LEFT, anchor=ctk.N)

        # botão para abrir a seleção de arquivos
        self.btn = ctk.CTkButton(
            self, text="Escolher Arquivo", state=ctk.DISABLED, height=35, font=('', 15, 'bold'), command=self.chooseFile)
        self.btn.pack(pady=10, padx=10, side=ctk.LEFT, anchor=ctk.N)

        # campo de texto que exibe o path do arquivo selecionado
        self.file = ctk.CTkEntry(self, state=ctk.DISABLED, height=35)
        self.file.pack(expand=True, padx=10, pady=10,
                       side=ctk.LEFT, anchor=ctk.N)

        # entrada para o version_high
        self.version_h = ctk.CTkEntry(self, state=ctk.DISABLED, height=35, width=70)
        self.version_h.pack(expand=True, padx=10, pady=10,
                          side=ctk.LEFT, anchor=ctk.N)

        # entrada para o version_lower
        self.version_l = ctk.CTkEntry(self, state=ctk.DISABLED, height=35, width=70)
        self.version_l.pack(expand=True, padx=10, pady=10,
                       side=ctk.LEFT, anchor=ctk.N)
        
        self.micro_var = ctk.StringVar(value="Selecione uma aplicação")
        self.micro_fam = ctk.CTkOptionMenu(self,state=ctk.DISABLED, height=35, width=70, values=["RX", "RL"], command=self.app_callback, variable=self.app_var)
        self.micro_fam.pack(expand=True, padx=10, pady=10,
                       side=ctk.LEFT, anchor=ctk.N)

        # botão para apagar o frame
        img = ctk.CTkImage(Image.open('img\excluir.png'), size=(20, 20))
        self.bin = ctk.CTkButton(
            self, text='', image=img, width=35, height=35, command=lambda: self.delFrame(self.repository))
        self.bin.pack(pady=10, padx=10, side=ctk.LEFT, anchor=ctk.N)

    def toggleCheckbox(self):
        '''
        Controla a ativação dos widgets de acordo com a marcação na 
        checkbox
        '''

        # ativa os widgets quando a checkbox é marcada e desativa quando desmarcada
        if (self.checkbox.get()==1):
            self.btn.configure(state=ctk.NORMAL)
            self.version_h.configure(state=ctk.NORMAL)
            self.version_l.configure(state=ctk.NORMAL)
            self.micro_fam.configure(state=ctk.NORMAL)
            self.repository.fwValidation(self)
        else:
            self.btn.configure(state=ctk.DISABLED)
            self.version_h.configure(state=ctk.DISABLED)
            self.version_l.configure(state=ctk.DISABLED)
            self.micro_fam.configure(state=ctk.DISABLED)
            self.repository.fwRemove(self)

    def chooseFile(self):
        '''
        Permite a seleção de arquivos .txt e .hex 
        '''
        self.length.configure(state=ctk.NORMAL)
        self.file.configure(state=ctk.NORMAL)
        self.filename = filedialog.askopenfilename(title="Selecione o arquivo do seu firmware", filetypes=[
            ("Arquivos .mot", "*.mot")])
        binary_string = mot_to_binary(self.filename)
        self.binary_length = len(binary_string)
        self.file.delete(0, tk.END)
        self.length.delete(0, tk.END)
        self.file.insert(0, self.filename)
        self.length.insert(0, self.binary_length)
        self.length.configure(state=ctk.DISABLED)
        self.file.configure(state=ctk.DISABLED)
        # print(self.binary_string)
        print(self.binary_length)
        

    def delFrame(self, repository):
        '''
        Retira o respectivo frame seletor da janela 
        '''
        self.pack_forget()
        repository.removeFrame(self)
    
    def validate_input(self, input):
        if len(input) <= 8:
            return True
        else:
            return False
        
    def micro_callback(self, choice):
        self.micro_var = micro_enum[choice]
        print(self.micro_var)