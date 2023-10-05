import customtkinter as ctk
from binary import *
from TabbedPanel import TabbedPanel
from FileSelectionFrameList import FileSelectionFrameList
from ControllerSelectionFrameList import ControllerSelectionFrameList
from MenuFrame import MenuFrame
from PIL import Image
from tkinter import filedialog


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
        self.controllerframe_list = ControllerSelectionFrameList()  # cria lista de frames de seleção
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
                if firmware_file not in mot_list:
                    mot_list.append(firmware_file)
                file_length = firmware_frame.binary_length
                version_h = int(firmware_frame.version_h.get())
                version_l = int(firmware_frame.version_l.get())
                offset = int(controller_frame.offset.get())
                interface = int(controller_frame.interface.get())
                comm_address = int(controller_frame.comm_address.get())
                code_id = int(controller_frame.code_id.get())
                version.extend(build_version_header(file_length, version_h, version_l, offset, interface, comm_address, code_id))
        
        for file_path in mot_list:
            total_l += len(mot_to_binary(file_path))
            binary_data.extend(mot_to_binary(file_path))
        
        header = {
            "header_ver": 0x02,
            "header_valid": 0x00,
            "prod_id": "CFW510",
            "prod_ver": "V2.01"
        }
        binary_gen(file, header, version, binary_data)
        
        print(version)
        print(binary_data)

# janela funcionando
app = App()
app.mainloop()
