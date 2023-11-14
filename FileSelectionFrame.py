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
        self.filename = ''
        self.binary_length = 0
        
        #label para identificar o código na tela de seleção
        self.label = ctk.CTkLabel(self, text = self.name, font=("",14, "bold"))
        self.label.pack(padx=10, pady=15, side=ctk.LEFT, anchor=ctk.N)
        
        # checkbox
        self.checkbox = ctk.CTkCheckBox(
            self, text='', height=35, width=25, command=self.toggleCheckbox)
        self.checkbox.pack(padx=10, pady=10, side=ctk.LEFT, anchor=ctk.N)

        # primeira entrada de texto (endereço)
        # self.length = ctk.CTkEntry(self, placeholder_text="Tamanho", height=35, width=75)
        # self.length.pack(expand=True, padx=10, pady=10,
        #                   side=ctk.LEFT, anchor=ctk.N)

        # botão para abrir a seleção de arquivos
        self.btn = ctk.CTkButton(
            self, state=ctk.DISABLED, text="Escolher Arquivo", height=35, font=('', 15, 'bold'), command=self.chooseFile)
        self.btn.pack(pady=10, padx=10, side=ctk.LEFT, anchor=ctk.N)

        # campo de texto que exibe o path do arquivo selecionado
        self.file = ctk.CTkEntry(self, placeholder_text="Local do arquivo", height=35, width=160)
        self.file.pack(expand=True, fill=ctk.X, pady=10, anchor=ctk.N, side=ctk.LEFT)

        # entrada para o version_high
        self.label_VersionH = ctk.CTkLabel(self, text="Version High:", font=("", 12, "bold"), height=35, anchor=ctk.E)
        self.label_VersionH.pack(fill=ctk.X, expand=True, side=ctk.LEFT, padx=5, pady=10, anchor=ctk.N)

        self.version_h = ctk.CTkEntry(self, placeholder_text="Ex: 0000", height=35, width=75)
        self.version_h.pack(fill=ctk.X, expand=True, pady=10, side=ctk.LEFT, anchor=ctk.N)

        # entrada para o version_lower
        self.label_VersionL = ctk.CTkLabel(self, text="Version Low:", font=("", 12, "bold"), height=35, anchor=ctk.E)
        self.label_VersionL.pack(fill=ctk.X, expand=True, side=ctk.LEFT, padx=5, pady=10, anchor=ctk.N)

        self.version_l = ctk.CTkEntry(self, placeholder_text="Version_l", height=35, width=75)
        self.version_l.pack(fill=ctk.X, expand=True, pady=10, side=ctk.LEFT, anchor=ctk.N)
        
        #entrada para o endereço inicial
        self.label_offset = ctk.CTkLabel(self, text="End. Inicial:", font=("", 12, "bold"), height=35, anchor=ctk.E)
        self.label_offset.pack(fill=ctk.X, expand=True, side=ctk.LEFT, padx=5, pady=10, anchor=ctk.N)

        self.init_offset = ctk.CTkEntry(self, placeholder_text="Endereço inicial", height=35, width=75)
        self.init_offset.pack(fill=ctk.X, expand=True, pady=10, side=ctk.LEFT, anchor=ctk.N)
        
        #entrada para o endereço final
        self.label_final_add = ctk.CTkLabel(self, text="End. Final:", font=("", 12, "bold"), height=35, anchor=ctk.E)
        self.label_final_add.pack(fill=ctk.X, expand=True, side=ctk.LEFT, padx=5, pady=10, anchor=ctk.N)

        self.final_add = ctk.CTkEntry(self, placeholder_text="Endereço final", height=35, width=75)
        self.final_add.pack(fill=ctk.X, expand=True, pady=10, side=ctk.LEFT, anchor=ctk.N)
        
        self.micro_var = ctk.StringVar(value="Selecione uma aplicação")
        self.micro_fam = ctk.CTkOptionMenu(self, state=ctk.DISABLED, dynamic_resizing=False, height=35, width=200, values=["RX", "RL"], command=self.micro_callback, variable=self.micro_var)
        self.micro_fam.pack(expand=True, padx=10, pady=10,
                       side=ctk.LEFT, anchor=ctk.N)

        # botão para apagar o frame
        img = ctk.CTkImage(Image.open('img\excluir.png'), size=(20, 20))
        self.bin = ctk.CTkButton(
            self, text='', image=img, width=35, height=35, command=lambda: self.delFrame(self.repository))
        self.bin.pack(pady=10, padx=10, side=ctk.RIGHT, anchor=ctk.E)
        
        #Desativação dos campos que foram alterados(placeholders)
        # self.length.configure(state=ctk.DISABLED)
        self.file.configure(state=ctk.DISABLED)
        self.version_h.configure(state=ctk.DISABLED)
        self.version_l.configure(state=ctk.DISABLED)
        self.micro_fam.configure(state=ctk.DISABLED)
        self.init_offset.configure(state=ctk.DISABLED)
        self.final_add.configure(state=ctk.DISABLED)

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
        # self.length.configure(state=ctk.NORMAL)
        self.file.configure(state=ctk.NORMAL)
        self.filename = filedialog.askopenfilename(title="Selecione o arquivo do seu firmware", filetypes=[
            ("Arquivos .mot", "*.mot")])
        print(self.filename)
        if self.filename=='':
            # self.length.configure(state=ctk.DISABLED)
            self.file.configure(state=ctk.DISABLED)
            return
        self.file.delete(0, tk.END)
        # self.length.delete(0, tk.END)
        # if self.micro_fam.get() == "RX":
        #     self.binary_length = len(mot_to_binary(self.filename, self.micro_var, 0, 0))
            # self.length.insert(0, self.binary_length)
        # if self.micro_fam.get() == "RL":
        #     self.binary_length = len(mot_to_binary(self.filename, self.micro_var, int(self.init_offset.get(), 16), int(self.final_add.get(), 16)))
            # self.length.insert(0, self.binary_length)
        self.file.insert(0, self.filename)
        # self.length.configure(state=ctk.DISABLED)
        self.file.configure(state=ctk.DISABLED)
        # print(self.binary_length)
        

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
        if choice == "RX":
            self.init_offset.delete(0,tk.END)
            self.final_add.delete(0,tk.END)
            self.init_offset.configure(state=ctk.DISABLED)
            self.final_add.configure(state=ctk.DISABLED)
        elif choice == "RL":
            self.init_offset.configure(state=ctk.NORMAL)
            self.final_add.configure(state=ctk.NORMAL)
            
        self.micro_var = micro_enum[choice]
        print("Microcontrolador: ", choice)
        
        # if self.filename != '':
            # self.length.configure(state=ctk.NORMAL)
            # self.length.delete(0, tk.END)
            # if self.micro_fam.get() == "RX":
            #     self.binary_length = len(mot_to_binary(self.filename, self.micro_var, 0, 0))
            # if self.micro_fam.get() == "RL":
            #     self.binary_length = len(mot_to_binary(self.filename, self.micro_var, int(self.init_offset.get(), 16), int(self.final_add.get(), 16)))
            #self.binary_length = len(mot_to_binary(self.filename, self.micro_var))
            # self.length.insert(0, self.binary_length)
            # self.length.configure(state=ctk.DISABLED)