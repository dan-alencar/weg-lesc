import customtkinter as ctk
from BodyFrame import BodyFrame
from SelectionFrameList import SelectionFrameList
from MenuFrame import MenuFrame
from PIL import Image
from tkinter import messagebox


class App(ctk.CTk):
    """
    Janela principal da aplicação
    """

    def __init__(self):
        super().__init__()

        # configuração inicial da janela

        self.geometry("1000x800")
        self.resizable('false', 'false')
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

        # frame de seleção de arquivos

        self.frame_list = SelectionFrameList()  # cria lista de frames de seleção
        self.body_frame = BodyFrame(
            master=self, corner_radius=0, fg_color='transparent')
        self.body_frame.pack(fill=ctk.BOTH, expand=ctk.TRUE, padx=30, pady=30)

        # botão para gerar aquivo binário

        self.generate_binary = ctk.CTkButton(
            self, text="Gerar Binário", command=self.listWatch)
        self.generate_binary.pack(pady=10, padx=10)

    def gerarbinario(self):
        '''
        Função chamada pelo botão gerar binário
        '''
        for frame in self.frame_list.all_frames:
            if frame.file.get() != "":
                response = messagebox.showinfo(
                    title="Mensagem", message="Seu arquivo binário foi gerado com sucesso")
                return

        response = messagebox.showerror(
            title="Mensagem", message="Selecione pelo menos um arquivo")

    def listWatch(self):
        print(*self.frame_list.all_frames)


# janela funcionando
app = App()
app.mainloop()