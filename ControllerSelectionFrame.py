import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
from dictionary import interface_enum

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
        self.optionmenu = ctk.CTkOptionMenu(self,state=ctk.DISABLED, dynamic_resizing=False, height=35, width=180, variable=self.optionmenu_var)
        self.optionmenu.pack(padx=10, pady=10, side=ctk.LEFT, anchor=ctk.N)
        
        # entrada para o communication address
        self.label_commadd = ctk.CTkLabel(self, text="End. de comunicação:", font=("", 12, "bold"), height=35, anchor=ctk.E)
        self.label_commadd.pack(fill=ctk.X, expand=True, side=ctk.LEFT, padx=5, pady=10, anchor=ctk.N)

        self.comm_address = ctk.CTkEntry(self, placeholder_text="Ex: 00", height=35, width=40)
        self.comm_address.pack(fill=ctk.X, expand=True, pady=10,
                       side=ctk.LEFT, anchor=ctk.N)
        
        # entrada para a interface
        self.interface_var = ctk.StringVar(value="Selecione uma interface")
        self.interface = ctk.CTkOptionMenu(self,state=ctk.DISABLED, dynamic_resizing=False, height=35, width=200, values=["I2C", "CAN", "Serial"], command=self.interface_callback, variable=self.interface_var)
        self.interface.pack(expand=True, padx=10, pady=10,
                       side=ctk.LEFT, anchor=ctk.N)
        
        # botão para apagar o frame
        img = ctk.CTkImage(Image.open('img\excluir.png'), size=(20, 20))
        self.bin = ctk.CTkButton(
            self, text='', image=img, width=35, height=35, command=lambda: self.delFrame(self.repository))
        self.bin.pack(pady=10, padx=10, side=ctk.RIGHT, anchor=ctk.E)

        self.comm_address.configure(state=ctk.DISABLED)
        # self.offset.configure(state=ctk.DISABLED)
        # self.code_id.configure(state=ctk.DISABLED)

        # entrada para o offset address
        # self.label_offadd = ctk.CTkLabel(self, text="Offset:", font=("", 12, "bold"), height=35, anchor=ctk.E)
        # self.label_offadd.pack(fill=ctk.X, expand=True, side=ctk.LEFT, padx=5, pady=10, anchor=ctk.N)
        #
        # self.offset = ctk.CTkEntry(self, placeholder_text="Ex: 00000000", height=35, width=85)
        # self.offset.pack(fill=ctk.X, expand=True, pady=10,
        #                side=ctk.LEFT, anchor=ctk.N)

        # entrada para o code_id
        # self.label_codeid = ctk.CTkLabel(self, text="Code ID:", font=("", 12, "bold"), height=35, anchor=ctk.E)
        # self.label_codeid.pack(fill=ctk.X, expand=True, side=ctk.LEFT, padx=5, pady=10, anchor=ctk.N)
        #
        # self.code_id = ctk.CTkEntry(self, placeholder_text="Ex: FF", height=35, width=85)
        # self.code_id.pack(fill=ctk.X, expand=True, pady=10,
        #                side=ctk.LEFT, anchor=ctk.N)

    def toggleCheckbox(self):
        '''
        Controla a ativação dos widgets de acordo com a marcação na 
        checkbox
        '''

        # ativa os widgets quando a checkbox é marcada e desativa quando desmarcada
        if self.checkbox.get()==1:
            self.interface.configure(state=ctk.NORMAL)
            self.comm_address.configure(state=ctk.NORMAL)
            self.optionmenu.configure(state=ctk.NORMAL)
            self.repository.updateFrames()
            # self.code_id.configure(state=ctk.NORMAL)
            # self.offset.configure(state=ctk.NORMAL)
        else:
            self.optionmenu.configure(state=ctk.DISABLED)
            self.interface.configure(state=ctk.DISABLED)
            self.comm_address.configure(state=ctk.DISABLED)
            # self.code_id.configure(state=ctk.DISABLED)
            # self.offset.configure(state=ctk.DISABLED)


    def delFrame(self, repository):
        '''
        Retira o respectivo frame seletor da janela 
        '''
        self.pack_forget()
        repository.removeFrame(self)
    
    #debugging da opção selecionada    
    def interface_callback(self, choice):
        self.interface_var = interface_enum[choice]
        print("Interface: ", self.interface_var)