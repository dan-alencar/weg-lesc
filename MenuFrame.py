import customtkinter as ctk
from tkinter import messagebox
import xml.etree.ElementTree as ET
from tkinter import filedialog
from FileSelectionFrame import FileSelectionFrame
from ControllerSelectionFrame import ControllerSelectionFrame


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

        self.clear()

        # carrega os frames do arquivo

        for frames in root:
            for frame in frames:
                if (frame.tag=='codeframe'):
                    new_frame = FileSelectionFrame(self.master.tab_view.codeframe, self.master.codeframe_list, self.master.tab_view.codeframe.index)
                    self.master.tab_view.codeframe.index += 1
                    self.master.codeframe_list.addFrame(new_frame)  # adiciona no repositório
                    new_frame.pack(side=ctk.TOP, fill=ctk.BOTH, expand=ctk.TRUE)
                    new_frame.checkbox.toggle()
                    new_frame.address.insert('1',  frame.get('address'))
                    new_frame.file.insert('1', frame.get('filepath'))
                    new_frame.txt1.insert('1', frame.get('bin'))
                    new_frame.txt2.insert('1', frame.get('hex'))
                if (frame.tag=='controllerframe'):
                    new_frame = ControllerSelectionFrame(self.master.tab_view.controllerframe, self.master.controllerframe_list)
                    self.master.controllerframe_list.addFrame(new_frame)
                    new_frame.pack(side=ctk.TOP, fill=ctk.BOTH, expand=ctk.TRUE)
                    new_frame.checkbox.toggle()
                    new_frame.address.insert('1',  frame.get('address'))
                    new_frame.file.insert('1', frame.get('filepath'))
                    new_frame.txt1.insert('1', frame.get('bin'))
                    new_frame.txt2.insert('1', frame.get('hex'))
                    option = frame.get('option')
                    if option[:2] == 'FW':
                        new_frame.optionmenu.set(option)
                    else:
                        new_frame.optionmenu.set('Selecione uma opção')

    def onSave(self, master):
        '''
        Salva um arquivo .lesc
        '''

        # abre o gerenciador de arquivos para salvar arquivo .lesc

        data = [('Arquivos .lesc', '*.lesc')]
        file = filedialog.asksaveasfilename(
            initialdir="/", title="Salvar como", filetypes=data, defaultextension=data)

        # chama a função que cria o arquivo XML

        file = self.toXML(master.codeframe_list, master.controllerframe_list, file)

    def toXML(self, codeframe_list, controllerframe_list, file):
        '''
        Cria um arquivo xml
        '''

        xml_doc = ET.Element('App')
        codeframes = ET.SubElement(xml_doc, 'codeframes')
        controllerframes = ET.SubElement(xml_doc, 'controllerframes')
        for frame in codeframe_list.valid_firmware:
            if frame.checkbox.get() == 1:
                if (isinstance(frame, FileSelectionFrame)):
                    ET.SubElement(codeframes, 'codeframe', address=frame.address.get(
                    ), filepath=frame.file.get(), bin=frame.txt1.get(), hex=frame.txt2.get())
        
        for frame in controllerframe_list.controllerframes:
            if frame.checkbox.get() == 1:
                if (isinstance(frame, ControllerSelectionFrame)):
                    optionSelected = frame.optionmenu.get()
                    # for firmware in codeframe_list.valid_firmware:
                    #     print("atualmente:" + firmware.name + "e procura:"+ optionSelected)
                    #     if firmware.name==optionSelected:
                    #         option = firmware.name
                    #         print("this is:" + optionSelected)
                    #         break
                    #     else:
                    #         print('Opção não encontrada')
                    #         option = '-1'
                    ET.SubElement(controllerframes, 'controllerframe', address=frame.address.get(
                    ), filepath=frame.file.get(), bin=frame.txt1.get(), hex=frame.txt2.get(), option = optionSelected)
            

        tree = ET.ElementTree(xml_doc)
        tree.write(file)
    
    def clear(self):
        '''
        Limpa todos os frames do aplicativo
        '''
        self.master.codeframe_list.unpackFrames()
        self.master.codeframe_list.clearFrames()
        self.master.controllerframe_list.unpackFrames()
        self.master.controllerframe_list.clearFrames()
        self.master.tab_view.codeframe.index = 0
        

    def about(self):
        messagebox.showinfo("Help", "Custom Menu Example")
