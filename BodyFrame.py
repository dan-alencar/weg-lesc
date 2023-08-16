import customtkinter as ctk
from FileSelectionFrame import FileSelectionFrame
from SelectionFrameList import SelectionFrameList


class BodyFrame(ctk.CTkScrollableFrame):
    '''
    Frame inicial que contém o primeiro seletor de arquivos
    e pode adicionar novos frames seletores
    '''

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # cria o primeiro seletor de arquivos
        self.first_frame = FileSelectionFrame(self, master.frame_list)
        self.first_frame.pack(fill=ctk.BOTH, expand=ctk.TRUE)
        master.frame_list.addFrame(self.first_frame)

        # botão para adicionar novo frame
        self.add_frame = ctk.CTkButton(
            self, text="+", width=35, command=lambda: self.newFrame(master))
        self.add_frame.pack(side=ctk.BOTTOM)

    def newFrame(self, master):
        '''
        Adiciona um novo frame seletor de arquivos no frame inicial
        '''
        new_frame = FileSelectionFrame(self, master.frame_list)
        new_frame.pack(fill=ctk.BOTH, expand=ctk.TRUE)
        master.frame_list.addFrame(new_frame)
