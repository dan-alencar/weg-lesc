import customtkinter as ctk
from PIL import Image
from FileSelectionFrame import FileSelectionFrame
from ControllerSelectionFrame import ControllerSelectionFrame


# Classe: BodyFrame
# Descrição: Frame inicial que contém o primeiro seletor de arquivos e pode adicionar novos frames seletores.
class BodyFrame(ctk.CTkScrollableFrame):

    # Método: __init__
    # Parâmetros de Entrada: master (janela principal), repository (repositório de frames),
    # type (tipo de frame: 'code' ou 'controller'), **kwargs (parâmetros adicionais)
    # Operação: Inicializa o frame, cria o primeiro seletor de arquivos e adiciona um botão para adicionar novos frames.
    def __init__(self, master, repository, type, **kwargs):
        super().__init__(master, **kwargs)
        
        # cria o primeiro seletor de arquivos
        if type == "code":
            self.first_frame = FileSelectionFrame(self, repository, 0)
            self.first_frame.micro_fam.configure(values=["Bootloader RX", "Bootloader RL"])
            self.first_frame.bin.configure(state="disabled", fg_color="transparent", image=None)
            self.index = 1
        if type == "controller":
            self.first_frame = ControllerSelectionFrame(self, repository)
        self.first_frame.pack(fill=ctk.BOTH, expand=ctk.TRUE)
        repository.addFrame(self.first_frame)

        # botão para adicionar novo frame
        img_mais = repository.master.get_image_path('mais.png')
        img = ctk.CTkImage(Image.open(img_mais), size=(20, 20))
        self.add_frame = ctk.CTkButton(self, text="", image=img, width=45, height=35, command=lambda: self.newFrame(repository, type))
        self.add_frame.pack(side=ctk.BOTTOM, pady=5)

    # Método: newFrame
    # Parâmetros de Entrada: repository (repositório de frames), type (tipo de frame: 'code' ou 'controller')
    # Operação: Adiciona um novo frame seletor de arquivos no frame inicial.
    def newFrame(self,repository, type):
        if type == "code":
            new_frame = FileSelectionFrame(self, repository, self.index)
            new_frame.pack(fill=ctk.BOTH, expand=ctk.TRUE)
            repository.addFrame(new_frame)
            self.index += 1
        if type == "controller":
            new_frame = ControllerSelectionFrame(self, repository)
            new_frame.pack(fill=ctk.BOTH, expand=ctk.TRUE)
            repository.addFrame(new_frame)
