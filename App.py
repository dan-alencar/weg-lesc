import customtkinter as ctk
from BodyFrame import BodyFrame
from SelectionFrameList import SelectionFrameList


class App(ctk.CTk):
    """
    Janela principal da aplicação
    """

    def __init__(self):
        super().__init__()

        # configuração inicial da janela

        self.geometry("800x600")
        self.title("Seleção de Arquivos")
        self.iconbitmap("img\weg-logo-5.ico")
        ctk.set_appearance_mode('light')

        # frame de menu

        # frame de seleção de arquivos

        self.frame_list = SelectionFrameList()  # cria lista de frames de seleção
        self.body_frame = BodyFrame(
            master=self, corner_radius=0, fg_color='transparent')
        self.body_frame.pack(fill=ctk.BOTH, expand=ctk.TRUE, padx=30, pady=30)

        # botão para gerar aquivo binário

        self.generate_binary = ctk.CTkButton(
            self, text="Gerar Binário", command=lambda: self.listWatch())
        self.generate_binary.pack(pady=10, padx=10)

    def listWatch(self):
        print(*self.frame_list.all_frames)


# janela funcionando
app = App()
app.mainloop()
