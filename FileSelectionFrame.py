import customtkinter as ctk
from tkinter import filedialog
import tkinter as tk
from PIL import Image
from dictionary import micro_enum


# Classe: FileSelectionFrame
# Descrição: Cria um novo frame com widgets para seleção de arquivos.
class FileSelectionFrame(ctk.CTkFrame):
    # Método: __init__
    # Parâmetros de Entrada: master (janela principal), repository (repositório de frames), index (índice do frame)
    # Operação: Inicializa os atributos do frame.
    def __init__(self, master, repository, index, **kwargs):
        super().__init__(master, **kwargs)
        
        # guarda a lista de frames do app
        self.repository = repository
        self.index = index
        self.name = "FW " + str(self.index + 1)
        self.filename = ''
        self.binary_length = 0
        self.offset = 0
        self.code1 = 0
        self.code2 = 0
        
        #label para identificar o código na tela de seleção
        self.label = ctk.CTkLabel(self, text = self.name, font=("",14, "bold"))
        self.label.pack(padx=10, pady=15, side=ctk.LEFT, anchor=ctk.N)
        
        # checkbox
        self.checkbox = ctk.CTkCheckBox(
            self, text='', height=35, width=25, command=self.toggleCheckbox)
        self.checkbox.pack(padx=10, pady=10, side=ctk.LEFT, anchor=ctk.N)

        # botão para abrir a seleção de arquivos
        img_file = repository.master.get_image_path('pathicon.png')
        fileicon = ctk.CTkImage(Image.open(img_file), size=(25, 25))
        self.btn = ctk.CTkButton(self, state=ctk.DISABLED, text="", image=fileicon, height=35, width=50, font=('', 14, 'bold'), command=self.chooseFile)
        self.btn.pack(pady=10, padx=5, side=ctk.LEFT, anchor=ctk.N)

        # campo de texto que exibe o path do arquivo selecionado
        self.file = ctk.CTkEntry(self, placeholder_text="Local do arquivo", height=35, width=300)
        self.file.pack(expand=False, fill=ctk.X, pady=10, anchor=ctk.N, side=ctk.LEFT)

        # entrada para o version_high
        self.label_VersionH = ctk.CTkLabel(self, text="V. High:", font=("", 12, "bold"), height=35, anchor=ctk.E)
        self.label_VersionH.pack(fill=ctk.X, expand=True, side=ctk.LEFT, padx=5, pady=10, anchor=ctk.N)

        self.version_h = ctk.CTkEntry(self, placeholder_text="Ex: 0000", height=35, width=90)
        self.version_h.pack(fill=ctk.X, expand=True, pady=10, side=ctk.LEFT, anchor=ctk.N)

        # entrada para o version_lower
        self.label_VersionL = ctk.CTkLabel(self, text="V. Low:", font=("", 12, "bold"), height=35, anchor=ctk.E)
        self.label_VersionL.pack(fill=ctk.X, expand=True, side=ctk.LEFT, padx=5, pady=10, anchor=ctk.N)

        self.version_l = ctk.CTkEntry(self, placeholder_text="Ex: FFFF", height=35, width=90)
        self.version_l.pack(fill=ctk.X, expand=True, pady=10, side=ctk.LEFT, anchor=ctk.N)
        
        self.micro_var = ctk.StringVar(value="RX/RL")
        self.micro_fam = ctk.CTkOptionMenu(self, state=ctk.DISABLED, dynamic_resizing=False, height=35, width=125, values=["RX", "RL"], command=self.micro_callback, variable=self.micro_var)
        self.micro_fam.pack(expand=True, padx=10, pady=10,
                       side=ctk.LEFT, anchor=ctk.N)

        # botão para apagar o frame
        img_excluir = repository.master.get_image_path('excluir.png')
        img = ctk.CTkImage(Image.open(img_excluir), size=(20, 20))
        self.bin = ctk.CTkButton(
            self, text='', image=img, width=35, height=35, command=lambda: self.delFrame(self.repository))
        self.bin.pack(pady=10, padx=10, side=ctk.RIGHT, anchor=ctk.E)


        #tirar esse frame do bootloader daqui e colocá-lo na tab de configurações
        # if self.index == 0:
        #     self.micro_fam.configure(variable=ctk.StringVar(value="Bootloader"), dynamic_resizing=True, values=["Bootloader RX", "Bootloader RL"])
        #     self.micro_fam.pack(anchor=ctk.W, padx=155, pady=10)
        #     self.bin.pack_forget()
        #     self.label_VersionH.pack_forget()
        #     self.label_VersionL.pack_forget()
        #     self.version_h.pack_forget()
        #     self.version_l.pack_forget()
        
        #Desativação dos campos que foram alterados(placeholders)
        self.file.configure(state=ctk.DISABLED)
        self.version_h.configure(state=ctk.DISABLED)
        self.version_l.configure(state=ctk.DISABLED)
        self.micro_fam.configure(state=ctk.DISABLED)

    # Método: toggleCheckbox
    # Parâmetros de Entrada: Nenhum
    # Operação: Controla a ativação dos widgets de acordo com a marcação na checkbox.
    def toggleCheckbox(self):
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

    # Método: chooseFile
    # Parâmetros de Entrada: Nenhum
    # Operação: Permite a seleção de arquivos .txt e .hex.
    def chooseFile(self):
        '''
        Permite a seleção de arquivos .txt e .hex 
        '''
        # self.length.configure(state=ctk.NORMAL)
        self.file.configure(state=ctk.NORMAL)
        self.filename = filedialog.askopenfilename(title="Selecione o arquivo do seu firmware", filetypes=[
            ("Arquivos .mot", "*.mot")])
        print(self.filename)
        if self.filename != "":
            self.master.master.master.previous_path = self.filename
        if self.filename=='':
            self.file.configure(state=ctk.DISABLED)
            return
        self.file.delete(0, tk.END)
        self.file.insert(0, self.filename)
        self.file.configure(state=ctk.DISABLED)

    # Método: delFrame
    # Parâmetros de Entrada: repository (repositório de frames)
    # Operação: Retira o respectivo frame seletor da janela.
    def delFrame(self, repository):
        self.pack_forget()
        repository.removeFrame(self)

    # Método: validate_input
    # Parâmetros de Entrada: input (entrada a ser validada)
    # Operação: Retorna True se a entrada tiver comprimento menor ou igual a 8, False caso contrário.
    def validate_input(self, input):
        if len(input) <= 8:
            return True
        else:
            return False

    # Método: micro_callback
    # Parâmetros de Entrada: choice (opção escolhida)
    # Operação: Atualiza os campos de acordo com a escolha do usuário.
    def micro_callback(self, choice):
        # if choice == "RX":
        #     self.initadd.delete(0, tk.END)
        #     self.finaladd.delete(0, tk.END)
        #     self.initadd.configure(state=ctk.DISABLED)
        #     self.finaladd.configure(state=ctk.DISABLED)
        # elif choice == "RL":
        #     self.initadd.configure(state=ctk.NORMAL)
        #     self.finaladd.configure(state=ctk.NORMAL)
            
        self.micro_var = micro_enum[choice]
        print("Microcontrolador: ", choice)
