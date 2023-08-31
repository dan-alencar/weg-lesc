import customtkinter as ctk
from tkinter import filedialog
import tkinter as tk
from PIL import Image
from FileSelectionFrameList import FileSelectionFrameList


class FileSelectionFrame(ctk.CTkFrame):
    '''
    Cria novo frame com widgets para seleção de arquivos 
    '''

    def __init__(self, master, repository, **kwargs):
        super().__init__(master, **kwargs)
        
        # guarda a lista de frames do app
        self.repository = repository
        self.index = len(repository.codeframes) + 1
        self.name = "Código " + str(self.index)
        
        #label para identificar o código na tela de seleção
        self.label = ctk.CTkLabel(self, text = self.name)
        self.label.pack(padx=10, pady=15, side=ctk.LEFT, anchor=ctk.N)
        
        # checkbox
        self.checkbox = ctk.CTkCheckBox(
            self, text='', height=35, width=25, command=self.toggleCheckbox)
        self.checkbox.pack(padx=10, pady=10, side=ctk.LEFT, anchor=ctk.N)

        # primeira entrada de texto (endereço)
        self.address = ctk.CTkEntry(
            self, state=ctk.DISABLED, height=35, width=70)
        self.address.pack(expand=True, padx=10, pady=10,
                          side=ctk.LEFT, anchor=ctk.N)

        # botão para abrir a seleção de arquivos
        self.btn = ctk.CTkButton(
            self, text="Escolher Arquivo", state=ctk.DISABLED, height=35, font=('', 15, 'bold'), command=self.chooseFile)
        self.btn.pack(pady=10, padx=10, side=ctk.LEFT, anchor=ctk.N)

        # campo de texto que exibe o path do arquivo selecionado
        self.file = ctk.CTkEntry(self, state=ctk.DISABLED, height=35)
        self.file.pack(expand=True, padx=10, pady=10,
                       side=ctk.LEFT, anchor=ctk.N)

        # segunda entrada de texto
        self.txt1 = ctk.CTkEntry(self, validate state=ctk.DISABLED, height=35, width=60)
        self.txt1.pack(expand=True, padx=10, pady=10,
                       side=ctk.LEFT, anchor=ctk.N)

        # terceira entrada de texto
        self.txt2 = ctk.CTkEntry(self, state=ctk.DISABLED, height=35, width=60)
        self.txt2.pack(expand=True, padx=10, pady=10,
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
            self.address.configure(state=ctk.NORMAL)
            self.file.configure(state=ctk.NORMAL)
            self.txt1.configure(state=ctk.NORMAL)
            self.txt2.configure(state=ctk.NORMAL)
            self.address.configure(placeholder_text="Endereço")
            self.repository.fwValidation(self)
        else:
            self.btn.configure(state=ctk.DISABLED)
            self.address.configure(placeholder_text="")
            self.address.configure(state=ctk.DISABLED)
            self.file.configure(state=ctk.DISABLED)
            self.txt1.configure(state=ctk.DISABLED)
            self.txt2.configure(state=ctk.DISABLED)
            self.repository.fwRemove(self)

    def chooseFile(self):
        '''
        Permite a seleção de arquivos .txt e .hex 
        '''
        self.filename = filedialog.askopenfilename(title="Selecione o arquivo do seu firmware", filetypes=[
            ("Arquivos .txt", ".txt"), ("Arquivos .hex", ".hex")])
        self.file.insert('end', self.filename)

    def delFrame(self, repository):
        '''
        Retira o respectivo frame seletor da janela 
        '''
        self.pack_forget()
        repository.removeFrame(self)
