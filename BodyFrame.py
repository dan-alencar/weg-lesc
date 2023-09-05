import customtkinter as ctk
from PIL import Image
from FileSelectionFrame import FileSelectionFrame
from ControllerSelectionFrame import ControllerSelectionFrame


class BodyFrame(ctk.CTkScrollableFrame):
    '''
    Frame inicial que contém o primeiro seletor de arquivos
    e pode adicionar novos frames seletores
    '''

    def __init__(self, master, repository, type, **kwargs):
        super().__init__(master, **kwargs)
        
        # cria o primeiro seletor de arquivos
        if type == "code":
            self.first_frame = FileSelectionFrame(self, repository)
        if type == "controller":
            self.first_frame = ControllerSelectionFrame(self, repository)
        self.first_frame.pack(fill=ctk.BOTH, expand=ctk.TRUE)
        repository.addFrame(self.first_frame)

        # botão para adicionar novo frame
        img = ctk.CTkImage(Image.open('img\mais.png'), size=(20, 20))
        self.add_frame = ctk.CTkButton(
            self, text="", image=img, width=45, height=35, command=lambda: self.newFrame(repository, type))
        self.add_frame.pack(side=ctk.BOTTOM, pady=5)

    def newFrame(self,repository, type):
        '''
        Adiciona um novo frame seletor de arquivos no frame inicial
        '''
        if type == "code":
            new_frame = FileSelectionFrame(self, repository)
            new_frame.pack(fill=ctk.BOTH, expand=ctk.TRUE)
            repository.addFrame(new_frame)
        if type == "controller":
            new_frame = ControllerSelectionFrame(self, repository)
            new_frame.pack(fill=ctk.BOTH, expand=ctk.TRUE)
            repository.addFrame(new_frame)
