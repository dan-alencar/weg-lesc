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
                    new_frame.file.configure(state=ctk.NORMAL)
                    micro_option = frame.get('micro')
                    if micro_option == 'RL':
                        new_frame.initadd.configure(state=ctk.NORMAL)
                        new_frame.finaladd.configure(state=ctk.NORMAL)
                        new_frame.initadd.insert('1', frame.get('initadd'))
                        new_frame.finaladd.insert('1', frame.get('finaladd'))
                    # new_frame.length.insert('1',  frame.get('length'))
                    new_frame.filename = frame.get('filepath')
                    new_frame.file.insert('1', frame.get('filepath'))
                    new_frame.version_h.insert('1',  frame.get('version_h'))
                    new_frame.version_l.insert('1', frame.get('version_l'))
                    new_frame.offset.insert('1', frame.get('offset'))
                    if micro_option != 'Selecione uma aplicação':
                        new_frame.micro_fam.set(micro_option)
                        new_frame.micro_callback(micro_option)
                    else:
                        new_frame.micro_fam.set('Selecione uma aplicação')
                        new_frame.micro_var = -1
                    new_frame.file.configure(state=ctk.DISABLED)
                if (frame.tag=='controllerframe'):
                    new_frame = ControllerSelectionFrame(self.master.tab_view.controllerframe, self.master.controllerframe_list)
                    self.master.controllerframe_list.addFrame(new_frame)
                    new_frame.pack(side=ctk.TOP, fill=ctk.BOTH, expand=ctk.TRUE)
                    new_frame.checkbox.toggle()
                    # new_frame.offset.insert('1', frame.get('offset'))
                    interface_option = frame.get('interface')
                    if interface_option != 'Selecione uma interface':
                        new_frame.interface.set(interface_option)
                        new_frame.interface_callback(interface_option)
                    else:
                        new_frame.interface.set('Selecione uma interface')
                        new_frame.interface_var = -1
                    new_frame.comm_address.insert('1', frame.get('comm_address'))
                    fw_option = frame.get('option')
                    if fw_option[:2] == 'FW':
                        new_frame.optionmenu.set(fw_option)
                    else:
                        new_frame.optionmenu.set('Selecione uma opção')
                if (frame.tag=='configurations'):  
                    self.master.tab_view.configframe.header_version.insert('1', frame.get('header_ver'))
                    self.master.tab_view.configframe.header_valid.insert('1', frame.get('header_val'))
                    self.master.tab_view.configframe.prod_id.insert('1', frame.get('prod_id'))
                    self.master.tab_view.configframe.prod_ver.insert('1', frame.get('prod_ver'))
        
        if len(self.master.codeframe_list.codeframes) == 0:
            new_codeframe = FileSelectionFrame(self.master.tab_view.codeframe, self.master.codeframe_list, self.master.tab_view.codeframe.index)
            self.master.tab_view.codeframe.index += 1
            self.master.codeframe_list.addFrame(new_codeframe)  # adiciona no repositório
            new_codeframe.pack(side=ctk.TOP, fill=ctk.BOTH, expand=ctk.TRUE)
            
        if len(self.master.controllerframe_list.controllerframes) == 0:
            new_controllerframe = ControllerSelectionFrame(self.master.tab_view.controllerframe, self.master.controllerframe_list)
            self.master.controllerframe_list.addFrame(new_controllerframe)
            new_controllerframe.pack(side=ctk.TOP, fill=ctk.BOTH, expand=ctk.TRUE)

    def onSave(self, master):
        '''
        Salva um arquivo .lesc
        '''

        # abre o gerenciador de arquivos para salvar arquivo .lesc

        data = [('Arquivos .lesc', '*.lesc')]
        file = filedialog.asksaveasfilename(
            initialdir="/", title="Salvar como", filetypes=data, defaultextension=data)

        # chama a função que cria o arquivo XML

        file = self.toXML(master.codeframe_list, master.controllerframe_list, master.tab_view.configframe, file)

    def toXML(self, codeframe_list, controllerframe_list, configurations, file):
        '''
        Cria um arquivo xml
        '''

        xml_doc = ET.Element('App')
        codeframes = ET.SubElement(xml_doc, 'codeframes')
        controllerframes = ET.SubElement(xml_doc, 'controllerframes')
        configs = ET.SubElement(xml_doc, 'configs')
        for frame in codeframe_list.valid_firmware:
            if frame.checkbox.get() == 1:
                if (isinstance(frame, FileSelectionFrame)):
                    ET.SubElement(codeframes, 'codeframe', filepath=frame.file.get(), version_h=frame.version_h.get(), version_l=frame.version_l.get(), offset=frame.offset.get(), micro=frame.micro_fam.get(), initadd=frame.initadd.get(), finaladd=frame.finaladd.get())
        
        for frame in controllerframe_list.controllerframes:
            if frame.checkbox.get() == 1:
                if (isinstance(frame, ControllerSelectionFrame)):
                    optionSelected = frame.optionmenu.get()
                    if optionSelected[:2] == 'FW':
                        optionIndex = codeframe_list.searchbyName(codeframe_list.valid_firmware_index, optionSelected)
                        if optionIndex != -1:
                            optionSelected = 'FW ' + str(optionIndex+1)
                        else:
                            optionSelected = "Selecione uma opção"
                    ET.SubElement(controllerframes, 'controllerframe', interface=frame.interface.get(), comm_address=frame.comm_address.get(),  option=optionSelected)
        ET.SubElement(configs, 'configurations', header_ver=configurations.header_version.get(), header_val=configurations.header_valid.get(), prod_id=configurations.prod_id.get(), prod_ver=configurations.prod_ver.get())

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
        self.master.tab_view.configframe.clearFields()
        self.master.tab_view.codeframe.index = 0
        

    def about(self):
        messagebox.showinfo("Help", "Custom Menu Example")
