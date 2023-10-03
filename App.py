import customtkinter as ctk
from binary import binary_gen
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
        ctk.set_appearance_mode('light')
        
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
        for mot_file in self.codeframe_list.valid_firmware:
            mot_file = mot_file.address
        binary_gen(file,)


# janela funcionando
app = App()
app.mainloop()
