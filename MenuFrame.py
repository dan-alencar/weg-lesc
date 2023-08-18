import customtkinter as ctk
from tkinter import messagebox
import xml.etree.ElementTree as ET
from tkinter import filedialog
from FileSelectionFrame import FileSelectionFrame


class MenuFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        '''
        cria uma menubar com opção de salvar e carregar arquivos
        '''

        # botões do menu
        self.open_button = ctk.CTkButton(
            self, text="Abrir", text_color='black', fg_color='transparent', hover_color='gray60', corner_radius=0, width=60, command=self.onOpen)
        self.save_button = ctk.CTkButton(
            self, text="Salvar", text_color='black', fg_color='transparent', hover_color='gray60', corner_radius=0, width=60, command=lambda: self.onSave(master))
        self.help_button = ctk.CTkButton(
            self, text="Ajuda", text_color='black', fg_color='transparent', hover_color='gray60', corner_radius=0, width=60, command=self.about)

        self.open_button.pack(side=ctk.LEFT)
        self.save_button.pack(side=ctk.LEFT)
        self.help_button.pack(side=ctk.LEFT)

    def onOpen(self):
        '''
        Procurar um arquivo .lesc
        '''

        # abre o seletor de arquivos para carregar o arquivo .lesc
        data = [('Arquivos .lesc', '*.lesc')]
        file = filedialog.askopenfilename(initialdir="/", title="Abrir arquivo",
                                          filetypes=data, defaultextension=data)

        # XML parser
        tree = ET.parse(file)
        root = tree.getroot()

        # apaga os frames do aplicativo e do repositório

        self.master.frame_list.unpackFrames()
        self.master.frame_list.clearFrames()

        # carrega os frames do arquivo

        for frames in root:
            for frame in frames:
                new_frame = FileSelectionFrame(
                    self.master.body_frame, self.master.frame_list)
                self.master.frame_list.addFrame(
                    new_frame)  # adiciona no repositório
                new_frame.pack(side=ctk.TOP, fill=ctk.BOTH, expand=ctk.TRUE)
                address = frame.get('address')
                filepath = frame.get('filepath')
                bin = frame.get('bin')
                hex = frame.get('hex')
                new_frame.checkbox.toggle()
                new_frame.address.insert('1',  address)
                new_frame.file.insert('1', filepath)
                new_frame.txt1.insert('1', bin)
                new_frame.txt2.insert('1', hex)

    def onSave(self, master):
        '''
        Salva um arquivo .lesc
        '''

        # abre o gerenciador de arquivos para salvar arquivo .lesc

        data = [('Arquivos .lesc', '*.lesc')]
        file = filedialog.asksaveasfilename(
            initialdir="/", title="Salvar como aaa", filetypes=data, defaultextension=data)

        # chama a função que cria o arquivo XML

        file = self.toXML(master.frame_list, file)

    def toXML(self, repository, file):
        '''
        Cria um arquivo xml
        '''

        xml_doc = ET.Element('App')
        frames = ET.SubElement(xml_doc, 'frames')
        for frame in repository.all_frames:
            ET.SubElement(frames, 'frame', address=frame.address.get(
            ), filepath=frame.file.get(), bin=frame.txt1.get(), hex=frame.txt2.get())

        tree = ET.ElementTree(xml_doc)
        tree.write(file)

    def about(self):
        messagebox.showinfo("Help", "Custom Menu Example")
