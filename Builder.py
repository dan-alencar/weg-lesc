from tkinter import filedialog, messagebox
from binary import *
from binascii import hexlify
from crc import crc16_encode, hex_string_to_bytearray
from BinaryToMot import mot_to_binary_rl, mot_to_binary_rx, ascii_to_mot, build_static_rx, mot_gen, fill_data


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
        binary_data = ''
        file_list = []
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
                    if (firmware_file, firmware_frame.micro_var) not in file_list:
                        file_list.append((firmware_file, firmware_frame.micro_var))
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

            for file_path in file_list:
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
            for binary in app_list:
                binary_data += binary
            data_complete = fill_data(binary_data, rx_address)
            print("Data complete: ", data_complete)
            data = hex_string_to_bytearray(data_complete)
            print("data: ", data)
            crc_complete = crc16_encode(data)
            crc_str = (hexlify(int.to_bytes(crc_complete, length=(crc_complete.bit_length() + 7) // 8, byteorder='big')).decode('utf-8'))
            crc_h = crc_str[:2]
            crc_l = crc_str[2:4]
            crc_complete = crc_l + crc_h + '0000'
            print("CRC do arquivo: ", crc_complete)
            mot_app = ascii_to_mot(binary_data, rx_address)
            mot_vector = ascii_to_mot(vt_data, vt_address)
            # Alterar para a aplicação do bootloader RL
            bootloader_app, bootloader_vector = mot_to_binary_rx(self.master.tab_view.configframe.file_entry.get())
            mot_bootloader_app = ascii_to_mot(bootloader_app['data'], bootloader_app['address'])
            mot_bootloader_vt = ascii_to_mot(bootloader_vector['data'], bootloader_vector['address'])

            static = {
                "exch_mode": 0x00000000,
                "fw_rev": 0xFFFFFFFF,
                "vecstart": 0xFFFFFF70,
                "vecend": 0xFFFFFEF4,
                "addstart": rx_address,
                #atualmente está errado, mas pode ser padronizado
                "addend": 0xFFFFE000,
                "addcrc": 0xFFFFFF7C,
                "numslaves": 0xFFFFFFFF,
                "exch_mode_slaves": 0x00000000,
                "first_update": 0xAAAAAAAA,
                "prod_ver": self.master.tab_view.configframe.prodver_entry.get(),
            }

            static_data = build_static_rx(static, version)
            mot_static = ascii_to_mot(static_data, 0xFFFFE000)

            mot_crc = ascii_to_mot(crc_complete, static['addcrc'])
            mot_list = [mot_bootloader_app, mot_app, mot_static, mot_vector, mot_crc, mot_bootloader_vt]

            data = [('Arquivo .mot', '*.mot')]
            file = filedialog.asksaveasfilename(
                initialdir="/", title="Salvar como", filetypes=data, defaultextension=data)

            mot_gen(file, mot_list)

            messagebox.showinfo(title="Concluído", message="O arquivo foi gerado com sucesso!")
        except ValueError as e:
            messagebox.showerror("Erro", str(e))
        except FileNotFoundError:
            pass
        except Exception:
            messagebox.showerror("Erro", "Erro na geração do arquivo.")
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
                      frame.file.get()} or frame.micro_fam.get() == "RX/RL":
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
