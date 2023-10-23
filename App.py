import customtkinter as ctk
from binary import *
from TabbedPanel import TabbedPanel
from FileSelectionFrameList import FileSelectionFrameList
from ControllerSelectionFrameList import ControllerSelectionFrameList
from MenuFrame import MenuFrame
from PIL import Image
from tkinter import filedialog
from dictionary import *


class App(ctk.CTk):
    """
    Janela principal da aplicação
    """

    def __init__(self):
        super().__init__()

        # configuração inicial da janela

        self.geometry("1000x800")
        self.resizable('true', 'true')
        self.title("Seleção de Arquivos")
        self.iconbitmap("img\weg-logo-5.ico")
        ctk.set_appearance_mode('light ')
        
        # frame de menu
        self.menu_frame = MenuFrame(
            self, fg_color='transparent', corner_radius=0)
        self.menu_frame.pack(fill=ctk.BOTH)

        self.logo = ctk.CTkImage(
            light_image=Image.open('img\logo-weg.png'), size=(1000, 90))
        self.logo_label = ctk.CTkLabel(self, image=self.logo, text='')
        self.logo_label.pack()
        
        #Menu de abas
        self.codeframe_list = FileSelectionFrameList(self)  # cria lista de frames de seleção
        self.controllerframe_list = ControllerSelectionFrameList(self)  # cria lista de frames de seleção
        self.tab_view = TabbedPanel(self)
        self.tab_view.pack(fill=ctk.BOTH,expand=ctk.TRUE)
        
        #Gerador do arquivo binário
        self.generate_binary = ctk.CTkButton(
            self, text="Gerar Binário", command=self.gerarbinario)
        self.generate_binary.pack(pady=10, padx=10)

    def gerarbinario(self):
        '''
        Função chamada pelo botão gerar binário
        '''
        data = [('Arquivo .bin', '*.bin')]
        file = filedialog.asksaveasfilename(
            initialdir="/", title="Salvar como", filetypes=data, defaultextension=data)
        
        version = bytearray()
        binary_data = bytearray()
        mot_list = []
        total_l = 0
        
        for controller_frame in self.controllerframe_list.controllerframes:
            option_selected = controller_frame.optionmenu.get()
            if option_selected[:2] == 'FW' and controller_frame.checkbox.get() == 1 :
                firmware_frame = self.codeframe_list.searchFrameFile(option_selected)
                firmware_file = firmware_frame.file.get()
                micro_fam = firmware_frame.micro_var
                if firmware_file not in mot_list:
                    mot_list.append((firmware_file, micro_fam)) #agora está passando uma tuple como parametro para a função do .mot
                file_length = firmware_frame.binary_length
                version_h = int(firmware_frame.version_h.get())
                version_l = int(firmware_frame.version_l.get())
                offset = int(controller_frame.offset.get())
                #lembrar de relacionar os tipos de aplicação do .mot (RX e RL)
                interface = controller_frame.interface_var
                comm_address = int(controller_frame.comm_address.get())
                code_id = int(controller_frame.code_id.get())
                version.extend(build_version_header(file_length, version_h, version_l, offset, interface, comm_address, code_id))
        
        for file_path in mot_list:
            holder = mot_to_binary(file_path) #mudar nome da variável depois
            total_l += len(holder)
            binary_data.extend(holder)

        header = {
            "header_ver": int(self.tab_view.configframe.header_version.get(), 16),
            "header_valid": int(self.tab_view.configframe.header_valid.get(), 16),
            "prod_id": self.tab_view.configframe.prod_id.get(),
            "prod_ver": self.tab_view.configframe.prod_ver.get()
        }
        
        binary_gen(file, header, version, binary_data)

app = App()
app.mainloop()
