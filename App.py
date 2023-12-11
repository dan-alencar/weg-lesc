import sys
import os
import customtkinter as ctk
from binary import *
from TabbedPanel import TabbedPanel
from FileSelectionFrameList import FileSelectionFrameList
from ControllerSelectionFrameList import ControllerSelectionFrameList
from MenuFrame import MenuFrame
from PIL import Image
from tkinter import filedialog
from tkinter import messagebox


class App(ctk.CTk):
    """
    Janela principal da aplicação
    """

    def __init__(self):
        super().__init__()

        # configuração inicial da janela

        self.geometry("1400x800")
        self.resizable('true', 'true')
        self.title("Seleção de Arquivos")

        weg_ico = 'weg-logo-5.ico'
        weg_logo = 'logo-weg.png'
        self.iconbitmap(self.get_image_path(weg_ico))
        ctk.set_appearance_mode('light')

        # frame de menu
        self.menu_frame = MenuFrame(
            self, fg_color='transparent', corner_radius=0)
        self.menu_frame.pack(fill=ctk.BOTH)

        self.logo = ctk.CTkImage(
            light_image=Image.open(self.get_image_path(weg_logo)), size=(1000, 90))
        self.logo_label = ctk.CTkLabel(self, image=self.logo, text='')
        self.logo_label.pack()

        # Menu de abas
        self.codeframe_list = FileSelectionFrameList(
            self)  # cria lista de frames de seleção
        self.controllerframe_list = ControllerSelectionFrameList(
            self)  # cria lista de frames de seleção
        self.tab_view = TabbedPanel(self)
        self.tab_view.pack(fill=ctk.BOTH, expand=ctk.TRUE)

        # Gerador do arquivo binário
        self.generate_binary = ctk.CTkButton(
            self, text="Gerar Binário", command=self.gerarbinario)
        self.generate_binary.pack(pady=10, padx=10)

    def gerarbinario(self):
        '''
        Função chamada pelo botão gerar binário
        '''
        version = bytearray()
        binary_data = bytearray()
        header_len = 0
        mot_list = []
        firmware_list = []
        offset = 0
        i = 0
        aux = 0
        try:
            self.fieldCheck(self.tab_view.configframe, 'header')

            for controller_frame in self.controllerframe_list.controllerframes:
                option_selected = controller_frame.optionmenu.get()
                # if option_selected[:2] == 'FW' and controller_frame.checkbox.get() == 1:
                if controller_frame.checkbox.get() == 1:
                    i = i + 1
                    self.fieldCheck(controller_frame, 'controller')
                    firmware_frame = self.codeframe_list.searchFrameFile(option_selected)
                    firmware_file = firmware_frame.file.get()
                    self.fieldCheck(firmware_frame, 'firmware')
                    if firmware_frame in firmware_list:
                        code1_size = firmware_frame.code1
                        code2_size = firmware_frame.code2
                        offset = firmware_frame.offset
                    else:
                        if firmware_frame.micro_var == 1:
                            init_add = final_add = 0
                        elif firmware_frame.micro_var == 2:
                            init_add = int(firmware_frame.initadd.get(), 16)
                            final_add = int(firmware_frame.finaladd.get(), 16)
                        file, code1_size, code2_size = mot_to_binary(firmware_file, firmware_frame.micro_var, init_add, final_add)
                        firmware_frame.binary_length = len(file)
                        firmware_frame.code1 = code1_size
                        firmware_frame.code2 = code2_size
                        if i == 1:
                            offset = 0
                            aux = code1_size
                        elif i == 2:
                            offset = aux
                            aux = code1_size + code2_size
                        elif i > 2:
                            offset = offset + aux
                            aux = code1_size + code2_size
                        firmware_frame.offset = offset
                        firmware_list.append(firmware_frame)
                    # adiciona a tupla à lista de .mot
                    if (firmware_file, firmware_frame.micro_var, init_add, final_add) not in mot_list:
                        mot_list.append((firmware_file, firmware_frame.micro_var, init_add, final_add))
                    version_h = int(firmware_frame.version_h.get(), 16)
                    version_l = int(firmware_frame.version_l.get(), 16)
                    optional = controller_frame.optional_box.get()
                    interface = controller_frame.interface_var
                    comm_address = int(controller_frame.comm_address.get(), 16)
                    code_id = int(controller_frame.code_id.get(), 16)
                    version.extend(build_version_header(version_h, version_l, offset, firmware_frame.binary_length, interface, comm_address, code_id, code1_size, code2_size, optional))

            print("Version: ", version)

            for file_path in mot_list:
                print(file_path)
                # mudar nome da variável depois
                holder, _, _ = mot_to_binary(*file_path)
                # total_l += len(holder)
                binary_data.extend(holder)
            if self.tab_view.configframe.header_version.get() == '01':
                header_len = 28
            elif self.tab_view.configframe.header_version.get() == '02':
                header_len = 32

            header = {
                "header_ver": int(self.tab_view.configframe.header_version.get(), 16),
                "header_valid": int(self.tab_view.configframe.header_valid.get(), 16),
                "prod_id": self.tab_view.configframe.prod_id.get(),
                "prod_ver": self.tab_view.configframe.prod_ver.get(),
                # tamanho dos dados + cabeçalho wps + cabeçalho versionamento + crc
                "length": len(binary_data) + header_len + len(version) + 4
            }
            data = [('Arquivo .bin', '*.bin')]
            file = filedialog.asksaveasfilename(
                initialdir="/", title="Salvar como", filetypes=data, defaultextension=data)

            binary_gen(file, header, version, binary_data)
            messagebox.showinfo(title="Concluído", message="O arquivo foi gerado com sucesso!")
        except ValueError as e:
            messagebox.showerror("Erro", str(e))
        except Exception:
            messagebox.showerror("Erro", "Erro na geração do binário.")
        log_type = [('Arquivo .txt', '*.txt')]
        log_file = filedialog.asksaveasfilename(
            initialdir="/", title="Salvar como", filetypes=log_type, defaultextension=log_type)
        self.log_builder(log_file, header, version)

    def fieldCheck(self, frame, type):
        if type == 'firmware':
            if '' in {frame.version_h.get(), frame.version_l.get(), frame.file.get()} or frame.micro_fam.get() == "Selecione uma aplicação":
                raise ValueError('Configure todos os campos dos firmwares selecionados')
            #cuidado com esse parenteses
            if frame.micro_fam.get() == "RL" and ('' in {frame.initadd.get(), frame.finaladd.get()}):
                raise ValueError('Configure todos os campos dos firmwares selecionados')
            else:
                return
        
        elif type == 'controller':
            if '' in {frame.comm_address.get(), frame.code_id.get()} or frame.interface.get() == "Selecione uma interface" or frame.optionmenu.get() == "Selecione uma opção":
                raise ValueError('Configure todos os campos dos controladores selecionados')
            else:
                return
        
        elif type == 'header':
            if '' in {frame.header_version.get(), frame.header_valid.get(), frame.prod_id.get(), frame.prod_ver.get()}:
                raise ValueError('Preencha todos os campos do cabeçalho')
            else:
                return

    def get_image_path(self, image_filename):
        if hasattr(sys, '_MEIPASS'):
            # Running as a PyInstaller executable
            return os.path.join(sys._MEIPASS, 'img', image_filename)
        else:
            # Running as a script
            return os.path.join('img', image_filename)

    def log_builder(self, destination_path, header, version):
        with open(destination_path, "w") as destination:
            destination.write("Firmwares carregados:\n")
            for firmware in self.codeframe_list.valid_firmware:
                destination.write(firmware.name)
                destination.write('\n')
                destination.write("Path do arquivo: ")
                destination.write(firmware.file.get())
                destination.write('\n')
                destination.write("Tamanho do arquivo: ")
                destination.write(str(firmware.binary_length))
                destination.write('\n')
                destination.write("Offset do arquivo: ")
                destination.write(str(firmware.offset))
                destination.write('\n')
                destination.write("Version High: ")
                destination.write(firmware.version_h.get())
                destination.write('\n')
                destination.write("Version Low: ")
                destination.write(firmware.version_l.get())
                destination.write('\n')
                destination.write("Init. Add.: ")
                destination.write(firmware.initadd.get())
                destination.write('\n')
                destination.write("Final Add.: ")
                destination.write(firmware.finaladd.get())
                destination.write('\n')
                destination.write("Família de controlador compatível: ")
                destination.write(firmware.micro_fam.get())
                destination.write('\n')
                destination.write('\n')
            destination.write("Controladores selecionados:\n")
            for controller in self.controllerframe_list.controllerframes:
                if controller.checkbox.get() == 1:
                    destination.write("Firmware selecionado: ")
                    destination.write(controller.optionmenu.get())
                    destination.write('\n')
                    destination.write("Endereço de comunicação: ")
                    destination.write(controller.comm_address.get())
                    destination.write('\n')
                    destination.write("Code ID: ")
                    destination.write(controller.code_id.get())
                    destination.write('\n')
                    destination.write("Interface: ")
                    destination.write(controller.interface.get())
                    destination.write('\n')
                    destination.write("Controlador opcional: ")
                    destination.write(str(controller.optional_box.get()))
                    destination.write('\n')
                    destination.write('\n')
            destination.write("Cabeçalho WPS:\n")
            for key in header:
                destination.write(key)
                destination.write(': ')
                destination.write(str(header[key]))
                destination.write('\n')
            destination.write('\n')
            destination.write("Cabeçalho de versionamento:\n")
            destination.write('\n')
            destination.write(str(version))


app = App()
app.mainloop()
