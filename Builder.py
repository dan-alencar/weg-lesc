from tkinter import filedialog, messagebox
from binary import *
from BinaryToMot import mot_to_binary_rl, mot_to_binary_rx, ascii_to_mot


# Classe: Builder
# Descrição: Responsável por gerar o arquivo binário com base nas configurações fornecidas.
class Builder:
    # Construtor da classe Builder
    # Parâmetros de Entrada: master (objeto que representa o aplicativo principal)
    def __init__(self, master):
        self.master = master

    # Método: gerarbinario
    # Parâmetros de Entrada: Nenhum
    # Operação: Gera o arquivo binário com base nas configurações fornecidas no aplicativo.
    def geradorMot(self):
        version = bytearray()
        binary_data = bytearray()
        mot_list = []
        firmware_list = []
        app_list = []
        offset = 0
        i = 0
        aux = 0
        try:
            for controller_frame in self.master.controllerframe_list.controllerframes:
                option_selected = controller_frame.optionmenu.get()
                if controller_frame.checkbox.get() == 1:
                    i = i + 1
                    # self.fieldCheck(controller_frame, 'controller')
                    firmware_frame = self.master.codeframe_list.searchFrameFile(option_selected)
                    firmware_file = firmware_frame.file.get()
                    # self.fieldCheck(firmware_frame, 'firmware')
                    if firmware_frame in firmware_list:
                        code1_size = firmware_frame.code1
                        code2_size = firmware_frame.code2
                        offset = firmware_frame.offset
                    else:
                        file, code1_size, code2_size = mot_to_binary(firmware_file, firmware_frame.micro_var)
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
                    if (firmware_file, firmware_frame.micro_var) not in mot_list:
                        mot_list.append((firmware_file, firmware_frame.micro_var))
                    version_h = int(firmware_frame.version_h.get(), 16)
                    version_l = int(firmware_frame.version_l.get(), 16)
                    optional = controller_frame.optional_box.get()
                    interface = controller_frame.interface_var
                    comm_address = int(controller_frame.comm_address.get(), 16)
                    code_id = int(controller_frame.code_id.get(), 16)
                    version.extend(
                        build_version_header(version_h, version_l, offset, firmware_frame.binary_length, interface,
                                             comm_address, code_id, optional, code1_size, code2_size))

            print("Version: ", version)

            for file_path in mot_list:
                print(file_path)
                file, family = file_path
                if family == 1:
                    app, vector_table = mot_to_binary_rx(file)
                    rx_address = app['address']
                    vt_data = vector_table['data']
                    vt_address = vector_table['address']
                    app_list.append(app['data'])
                elif family == 2:
                    app, vector_table = mot_to_binary_rl(file)
                    app_list.append(vector_table['data'])
                    app_list.append(app['data'])
            mot_vector = ascii_to_mot(vt_data, vt_address)
            #Alterar para a aplicação do bootloader RL
            bootloader_app, bootloader_vector = mot_to_binary_rx(self.master.tab_view.configframe.file_entry.get())
            bootloader_app_data = ascii_to_mot(bootloader_app['data'], bootloader_app['address'])
            bootloader_vt_data = ascii_to_mot(bootloader_vector['data'], bootloader_vector['address'])


            # for mot in app_list:
            #     print(mot)
            # for mot in vectortable_list:
            #     print(mot)

            # static = {
            #     "exch_mode": self.master.tab_view.configframe.exch_mode_entry.get(),
            #     "fw_rev": self.master.tab_view.configframe.fw_rev_entry.get(),
            #     "vecstart": self.master.tab_view.configframe.vecstart_entry.get(),
            #     "vecend": self.master.tab_view.configframe.vecend_entry.get(),
            #     "addstart": self.master.tab_view.configframe.addstart_entry.get(),
            #     "addend": self.master.tab_view.configframe.addend_entry.get(),
            #     "addcrc": self.master.tab_view.configframe.addcrc_entry.get(),
            #     "numslaves": self.master.tab_view.configframe.numslaves_entry.get(),
            #     "exch_mode_slaves": self.master.tab_view.configframe.exch_mode_slaves_entry.get(),
            #     "zeroblock": self.master.tab_view.configframe.zeroblock_entry.get(),
            #     "first_update": "AAAAAAAA",
            #     "prod_ver": self.master.tab_view.configframe.prodver_entry.get(),
            # }
            #
            # data = [('Arquivo .bin', '*.bin')]
            # file = filedialog.asksaveasfilename(
            #     initialdir="/", title="Salvar como", filetypes=data, defaultextension=data)
            #
            # #alterações nessa função para a aplicação de Bin2Mot
            # binary_gen(file, static, version, binary_data)
            #
            # messagebox.showinfo(title="Concluído", message="O arquivo foi gerado com sucesso!")
        except ValueError as e:
            messagebox.showerror("Erro", str(e))
        except Exception:
            messagebox.showerror("Erro", "Erro na geração do binário.")
        # log_file = file[:-4] + ".txt"
        # self.log_builder(log_file, static, version)

    # Método: fieldCheck
    # Parâmetros de Entrada: frame (objeto representando o frame a ser verificado),
    # type (tipo de verificação - 'firmware', 'controller' ou 'header')
    # Operação: Verifica se todos os campos obrigatórios foram preenchidos
    # nos frames de firmware, controlador ou cabeçalho.
    def fieldCheck(self, frame, type):
        if type == 'firmware':
            if '' in {frame.version_h.get(), frame.version_l.get(),
                      frame.file.get()} or frame.micro_fam.get() == "Selecione uma aplicação":
                raise ValueError('Configure todos os campos dos firmwares selecionados')
            # cuidado com esse parenteses
            else:
                return

        elif type == 'controller':
            if '' in {frame.comm_address.get(),
                      frame.code_id.get()} or frame.interface.get() == "Selecione uma interface" or frame.optionmenu.get() == "Selecione uma opção":
                raise ValueError('Configure todos os campos dos controladores selecionados')
            else:
                return

        elif type == 'header':
            if '' in {self.master.tab_view.configframe.exch_mode_entry.get(), self.master.tab_view.configframe.fw_rev_entry.get(), self.master.tab_view.configframe.vecstart_entry.get(), self.master.tab_view.configframe.vecend_entry.get(), self.master.tab_view.configframe.addstart_entry.get(), self.master.tab_view.configframe.addend_entry.get(), self.master.tab_view.configframe.addcrc_entry.get(), self.master.tab_view.configframe.numslaves_entry.get(), self.master.tab_view.configframe.exch_mode_slaves_entry.get()}:
                raise ValueError('Preencha todos os campos do cabeçalho')
            else:
                return

    # Método: log_builder
    # Parâmetros de Entrada: destination_path (caminho do arquivo de log), header
    # Operação: Verifica se todos os campos obrigatórios foram preenchidos
    # nos frames de firmware, controlador ou cabeçalho.
    def log_builder(self, destination_path, header, version):
        with open(destination_path, "w") as destination:
            destination.write("Firmwares carregados:\n")
            for firmware in self.master.codeframe_list.valid_firmware:
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
                destination.write("Code 1 Size: ")
                destination.write(str(firmware.code1))
                destination.write('\n')
                destination.write("Code 2 Size: ")
                destination.write(str(firmware.code2))
                destination.write('\n')
                destination.write("Família de controlador compatível: ")
                destination.write(firmware.micro_fam.get())
                destination.write('\n')
                destination.write('\n')
            destination.write("Controladores selecionados:\n")
            for controller in self.master.controllerframe_list.controllerframes:
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
