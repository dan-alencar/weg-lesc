from tkinter import filedialog, messagebox
from binary import *


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
    def gerarbinario(self):
        version = bytearray()
        binary_data = bytearray()
        header_len = 0
        mot_list = []
        firmware_list = []
        offset = 0
        i = 0
        aux = 0
        try:
            self.fieldCheck(self.master.tab_view.configframe, 'header')

            for controller_frame in self.master.controllerframe_list.controllerframes:
                option_selected = controller_frame.optionmenu.get()
                # if option_selected[:2] == 'FW' and controller_frame.checkbox.get() == 1:
                if controller_frame.checkbox.get() == 1:
                    i = i + 1
                    self.fieldCheck(controller_frame, 'controller')
                    firmware_frame = self.master.codeframe_list.searchFrameFile(option_selected)
                    firmware_file = firmware_frame.file.get()
                    self.fieldCheck(firmware_frame, 'firmware')
                    if firmware_frame in firmware_list:
                        code1_size = firmware_frame.code1
                        code2_size = firmware_frame.code2
                        offset = firmware_frame.offset
                    else:
                        # if firmware_frame.micro_var == 1:
                        #     init_add = final_add = 0
                        # elif firmware_frame.micro_var == 2:
                        #     init_add = int(firmware_frame.initadd.get(), 16)
                        #     final_add = int(firmware_frame.finaladd.get(), 16)
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
                # mudar nome da variável depois
                holder, _, _ = mot_to_binary(*file_path)
                # total_l += len(holder)
                binary_data.extend(holder)
            if self.master.tab_view.configframe.header_version.get() == '01':
                header_len = 28
            elif self.master.tab_view.configframe.header_version.get() == '02':
                header_len = 32

            header = {
                "header_ver": int(self.master.tab_view.configframe.header_version.get(), 16),
                "header_valid": int(self.master.tab_view.configframe.header_valid.get(), 16),
                "prod_id": self.master.tab_view.configframe.prod_id.get(),
                "prod_ver": self.master.tab_view.configframe.prod_ver.get(),
                # tamanho dos dados + cabeçalho wps + cabeçalho versionamento + crc
                "length": len(binary_data) + header_len + len(version) + 4
            }
            data = [('Arquivo .bin', '*.bin')]
            file = filedialog.asksaveasfilename(
                initialdir=self.master.previous_path, title="Salvar como", filetypes=data, defaultextension=data)
            if file != '':
                self.master.previous_path = file
            binary_gen(file, header, version, binary_data)
            messagebox.showinfo(title="Concluído", message="O arquivo foi gerado com sucesso!")
        except ValueError as e:
            messagebox.showerror("Erro", str(e))
        except FileNotFoundError:
            pass
        except Exception:
            messagebox.showerror("Erro", "Erro na geração do binário.")
        log_file = file[:-4] + ".txt"
        self.log_builder(log_file, header, version)

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
            if '' in {frame.header_version.get(), frame.header_valid.get(), frame.prod_id.get(), frame.prod_ver.get()}:
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
