import customtkinter as ctk
from tkinter import filedialog
from PIL import Image


class ControllerSelectionFrame(ctk.CTkFrame):
    '''
    Cria novo frame com widgets para seleção de arquivos 
    '''

    def __init__(self, master, repository, **kwargs):
        super().__init__(master, **kwargs)

        # guarda a lista de frames do app
        self.repository = repository

        # checkbox
        self.checkbox = ctk.CTkCheckBox(
            self, text='', height=35, width=25, command=self.toggleCheckbox)
        self.checkbox.pack(padx=10, pady=10, side=ctk.LEFT, anchor=ctk.N)
        
        # menu de escolha de firmware
        self.optionmenu_var = ctk.StringVar(value="Selecione uma opção")
        self.optionmenu = ctk.CTkOptionMenu(self,state=ctk.DISABLED, values=["option 1 ", "option 2"],
                                         command=self.optionmenu_callback,
                                         variable=self.optionmenu_var)
        self.optionmenu.pack(padx=10, pady=10, side=ctk.LEFT, anchor=ctk.N)

        # entrada para o offset address
        self.offset = ctk.CTkEntry(self, state=ctk.DISABLED, height=35, width=60)
        self.offset.pack(expand=True, padx=10, pady=10,
                       side=ctk.LEFT, anchor=ctk.N)

        # entrada para a interface
        self.interface = ctk.CTkEntry(self, state=ctk.DISABLED, height=35, width=60)
        self.interface.pack(expand=True, padx=10, pady=10,
                       side=ctk.LEFT, anchor=ctk.N)
        
        # entrada para o communication address
        self.comm_address = ctk.CTkEntry(self, state=ctk.DISABLED, height=35, width=60)
        self.comm_address.pack(expand=True, padx=10, pady=10,
                       side=ctk.LEFT, anchor=ctk.N)
        
        # entrada para o code_id
        self.code_id = ctk.CTkEntry(self, state=ctk.DISABLED, height=35, width=60)
        self.code_id.pack(expand=True, padx=10, pady=10,
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
            self.offset.configure(state=ctk.NORMAL)
            self.interface.configure(state=ctk.NORMAL)
            self.comm_address.configure(state=ctk.NORMAL)
            self.code_id.configure(state=ctk.NORMAL)
            self.optionmenu.configure(state=ctk.NORMAL)
            self.repository.updateFrames()
        else:
            self.optionmenu.configure(state=ctk.DISABLED)
            self.offset.configure(state=ctk.DISABLED)
            self.interface.configure(state=ctk.DISABLED)
            self.comm_address.configure(state=ctk.DISABLED)
            self.code_id.configure(state=ctk.DISABLED)


    def delFrame(self, repository):
        '''
        Retira o respectivo frame seletor da janela 
        '''
        self.pack_forget()
        repository.removeFrame(self)
    
    #debugging da opção selecionada
    def optionmenu_callback(self, choice):
        print("optionmenu dropdown clicked:", choice)
