import struct
import binascii
from binary import mul64


# Função: parse_srec_line
# Parâmetros de Entrada: line (linha do arquivo .mot), firmware (tipo de firmware)
# Saída: Dicionário contendo informações da linha
# Operação: Analisa a linha do arquivo .mot e extrai informações com base no tipo de firmware.
def parse_srec_line(line):
    record_type = line[0:2]
    data_length = 0
    address = 0
    data = ''
    checksum = ''
    if record_type == b'S1':
        data_length = int(line[2:4], 16)
        address = int(line[4:8], 16)
        data = line[8:-2].decode('utf-8')
        checksum = line[-2:]
    elif record_type == b'S2':
        data_length = int(line[2:4], 16)
        address = int(line[4:10], 16)
        data = line[10:-2].decode('utf-8')
        checksum = line[-2:]
    elif record_type == b'S3':
        data_length = int(line[2:4], 16)
        address = int(line[4:12], 16)
        data = line[12:-2].decode('utf-8')
        checksum = line[-2:]

    return {
        "record_type": record_type,
        "data_length": data_length,
        "address": address,
        "data": data,
        "checksum": checksum
    }


def fill_data(data, init_util, end_address):
    lenght = int(len(data) / 2)
    util_data_len = lenght + init_util
    final_data = data + (end_address - util_data_len) * 'FF'
    return final_data


# Função: mot_to_binary
# Parâmetros de Entrada: file_path, firmware, init_offset2, final_address
# Saída: Dados binários resultantes da conversão do arquivo .mot
# Operação: Converte o conteúdo de um arquivo .mot para dados binários, divididos em duas partes
# com base nos parâmetros fornecidos.
def mot_to_binary_rx(file_path):
    code1 = ''  # string que contém a primera parte do código
    code2 = ''  # string que contém a segunda parte do código
    previous_end_address = 0  # guarda o último endereço preenchido na iteração anterior
    lines = 0  # guarda a quantidade de linhas para determinar os endereços de inicio
    code1_address = 0  # endereço inicial do code1
    code2_address = 0  # endereço inicial do code2

    with open(file_path, 'rb') as mot:
        for line in mot:
            line = line.strip()
            record = parse_srec_line(line)

            # testa se a linha armazena dados
            if record['record_type'] != b'S3':
                pass

            else:
                # endereço inicial do dado
                init_address = record['address']
                # endereço final do dado
                end_address = record['address'] + record['data_length'] - 5

                if lines == 0:
                    # guarda o endereço da primeira linha do code1
                    previous_end_address = record['address']
                    code1_address = record['address']

                # verifica se a linha pertence à primeira parte
                if record['address'] < int(0xFFFFFEE4):

                    # preenche bytes vazios quando o endereço do início da linha é maior que o endereço do fim da linha anterior
                    if previous_end_address < init_address:
                        code1 += (init_address - previous_end_address) * 'FF'

                    # junta o dado à primeira string
                    code1 += record["data"]

                # verifica se a linha pertence à segunda parte
                elif record['address'] >= int(0xFFFFFEE4):
                    # guarda o endereço da primeira linha do code2
                    if code2 == '':
                        code2_address = record['address']

                    # se a linha for a primeira da segunda parte, altera o valor do endereço final da linha anterior
                    if record['address'] == int(0xFFFFFEE4):
                        previous_end_address = 0xFFFFFEE4

                    # junta o dado à segunda string
                    code2 += record["data"]

                # atualiza o endereço final anterior
                previous_end_address = end_address
                lines += 1  # incrementa o número de linhas

    # escrevendo o arquivo binário
    code1_size = len(bytearray.fromhex(code1))
    print('code 1: ', code1_size)
    code2_size = len(bytearray.fromhex(code2))
    print('code 2: ', code2_size)

    app = {
        'data': code1,
        'address': code1_address,
        'size': code1_size
    }

    vector_table = {
        'data': code2,
        'address': code2_address,
        'size': code2_size
    }

    return app, vector_table


# def mot_to_binary_rl(file_path):
#     code1 = ''  # string que contém a primera parte do código
#     code2 = ''  # string que contém a segunda parte do código
#     previous_end_address = 0  # guarda o último endereço preenchido na iteração anterior
#     code = 1
#     lines = 0  # guarda a quantidade de linhas para determinar os endereços de inicio
#     code1_address = 0  # endereço inicial do code1
#     code2_address = 0  # endereço inicial do code2
#
#     with open(file_path, 'rb') as mot:
#         for line in mot:
#             line = line.strip()
#             record = parse_srec_line(line)
#
#             # testa se a linha armazena dados
#             if record['record_type'] == b'S0':
#                 pass
#
#             else:
#                 # endereço inicial do dado
#                 init_address = record['address']
#                 # endereço final do dado
#                 if record['address'] <= 0xFFFF:  # 2 bytes = S1
#                     end_address = record['address'] + record['data_length'] - 3
#                 elif record['address'] <= 0xFFFFFF:  # 3 bytes = S2
#                     end_address = record['address'] + record['data_length'] - 4
#                 elif record['address'] <= 0xFFFFFF:  # 4 bytes = S3
#                     end_address = record['address'] + record['data_length'] - 5
#
#                 if lines == 0:
#                     code1_address = record['address']
#
#                 # verifica se a linha pertence à segunda parte, se houve um pulo >= 128 bytes
#                 if init_address - previous_end_address >= 128 and code == 1:
#                     code = 2  # indica que houve uma mudança para code 2
#                     previous_end_address = record['address']
#                     code2_address = record['address']
#
#                 # verifica se houve um segundo pulo >= 128 bytes, indicando fim das informações
#                 elif init_address - previous_end_address >= 128 and code == 2:
#                     break  # para de percorrer o arquivo
#
#                 # se a linha faz parte da primeira parte do código:
#                 if code == 1:
#                     # preenche bytes vazios quando o endereço do início da linha é maior
#                     # que o endereço do fim da linha anterior
#                     if previous_end_address < init_address:
#                         code1 += (init_address - previous_end_address) * 'FF'
#
#                     # junta o dado à primeira string
#                     code1 += record["data"]
#
#                 # se a linha fizer parte da segunda parte do código
#                 if code == 2:
#                     # preenche bytes vazios quando o endereço do início da linha
#                     # é maior que o endereço do fim da linha anterior
#                     if previous_end_address < init_address:
#                         code2 += (init_address - previous_end_address) * 'FF'
#
#                     # junta o dado à segunda string
#                     code2 += record["data"]
#
#                 # atualiza o endereço final anterior
#                 previous_end_address = end_address
#
#     # completando os códigos para que o tamanho seja múltiplo de 64
#     code1 = mul64(code1)
#     code2 = mul64(code2)
#
#     code1_size = len(bytearray.fromhex(code1))
#     print('code 1: ', code1_size)
#     code2_size = len(bytearray.fromhex(code2))
#     print('code 2: ', code2_size)
#
#     app = {
#         'data': code2,
#         'address': code2_address,
#         'size': code2_size
#     }
#
#     vector_table = {
#         'data': code1,
#         'address': code1_address,
#         'size': code1_size
#     }
#
#     return app, vector_table


def mot_to_binary_rl(file_path):
    code1 = ''  # string que contém a primera parte do código
    code2 = ''  # string que contém a segunda parte do código
    previous_end_address = 0  # guarda o último endereço preenchido na iteração anterior
    code = 1
    lines = 0  # guarda a quantidade de linhas para determinar os endereços de inicio
    code1_address = 0  # endereço inicial do code1
    code2_address = 0  # endereço inicial do code2

    with open(file_path, 'rb') as mot:
        for line in mot:
            line = line.strip()
            record = parse_srec_line(line)

            # testa se a linha armazena dados
            if record['record_type'] == b'S0':
                pass

            else:
                # endereço inicial do dado
                init_address = record['address']
                # endereço final do dado
                if record['address'] <= 0xFFFF:  # 2 bytes = S1
                    end_address = record['address'] + record['data_length'] - 3
                elif record['address'] <= 0xFFFFFF:  # 3 bytes = S2
                    end_address = record['address'] + record['data_length'] - 4
                elif record['address'] <= 0xFFFFFF:  # 4 bytes = S3
                    end_address = record['address'] + record['data_length'] - 5

                if lines == 0:
                    code1_address = record['address']

                # verifica se a linha pertence à segunda parte, se houve um pulo >= 128 bytes
                if init_address - previous_end_address >= 100 and code == 1:
                    code = 2  # indica que houve uma mudança para code 2
                    previous_end_address = record['address']
                    code2_address = record['address']

                # verifica se houve um segundo pulo >= 128 bytes, indicando fim das informações
                elif init_address - previous_end_address >= 256 and code == 2:
                    break  # para de percorrer o arquivo

                # se a linha faz parte da primeira parte do código:
                if code == 1:
                    # preenche bytes vazios quando o endereço do início da linha é maior
                    # que o endereço do fim da linha anterior
                    if previous_end_address < init_address:
                        code1 += (init_address - previous_end_address) * 'FF'

                    # junta o dado à primeira string
                    code1 += record["data"]

                # se a linha fizer parte da segunda parte do código
                if code == 2:
                    # preenche bytes vazios quando o endereço do início da linha
                    # é maior que o endereço do fim da linha anterior
                    if previous_end_address < init_address:
                        code2 += (init_address - previous_end_address) * 'FF'

                    # junta o dado à segunda string
                    code2 += record["data"]

                # atualiza o endereço final anterior
                previous_end_address = end_address

    return code1, code2, code1_address, code2_address


# Função: build_header
# Parâmetros de Entrada: header (dicionário com informações do cabeçalho)
# Saída: Dados do cabeçalho empacotados
# Operação: Constrói o cabeçalho conforme a versão especificada no dicionário e o empacota.
def build_static_rx(static, version):

    static_format = 'IIIIIIIIII12s'
    static_data = struct.pack(
        static_format, static["exch_mode"], static["fw_rev"], static["vecstart"],
        static["vecend"], static["addstart"], static["addend"], static["addcrc"],
        static["numslaves"], static["exch_mode_slaves"], static["first_update"],
        bytes(static["prod_ver"], 'utf-8'))
    static_data = binascii.hexlify(static_data).decode('utf-8')
    version = binascii.hexlify(version).decode('utf-8')

    return static_data + version


def mot2bin(file_path, file_type, static=''):
    vec_table, app, vec_table_add, app_add = mot_to_binary_rl(file_path)

    if file_type == 'boot_rl':
        app = app[:-64] + static

    vec_table = mul64(vec_table)
    app = mul64(app)

    dict_app = {
        'data': app,
        'address': app_add
    }

    dict_vt = {
        'data': vec_table,
        'address': vec_table_add
    }
    return dict_app, dict_vt


def build_static_rl(static):
    static_format = 'IIIIIII'
    static_data = struct.pack(
        static_format, static["comm_address"], static["fw_rev"], static["vecstart"],
        static["vecend"], static["addstart"], static["addend"], static["crc"])
    static_data = binascii.hexlify(static_data).decode('utf-8')

    return static_data


def calculate_checksum(data):
    # Soma os bytes
    checksum_sum = 0
    for i in range(2, len(data), 2):
        byte = data[i:i+2]
        checksum_sum += int(byte, 16)

    # Descarta o byte mais significativo e retém o byte menos significativo
    checksum_lsb = checksum_sum & 0xFF

    # Calcula o complemento de um (ones' complement)
    checksum_complement = 0xFF - checksum_lsb

    return checksum_complement


def ascii_to_mot(input_string, init_address):
    # Verifica se a string tem um número par de caracteres
    if len(input_string) % 2 != 0:
        raise ValueError("A string deve ter um número par de caracteres.")

    # Inicializa a string de saída
    output_string = ""

    # Divide a string em pares de caracteres
    hex_pairs = [input_string[i:i+2] for i in range(0, len(input_string), 2)]

    # Escreve os dados no formato S-record
    address = init_address
    line_length = 0
    record_data = ""

    for hex_pair in hex_pairs:
        decimal_value = int(hex_pair, 16)
        record_data += "{:02X}".format(decimal_value)
        line_length += 1

        if line_length > 15:  # Número máximo de bytes em uma linha S3
            record = ""
            # Adiciona a linha no formato S-record adequado à ‘string’ de saída
            if address <= 0xFFFF:  # 2 bytes = S1
                record = "S1{:02X}{:04X}{}".format(line_length + 3, address, record_data)
            elif address <= 0xFFFFFF:  # 3 bytes = S2
                record = "S2{:02X}{:06X}{}".format(line_length + 4, address, record_data)
            elif address <= 0xFFFFFFFF:  # 4 bytes = S3
                record = "S3{:02X}{:08X}{}".format(line_length + 5, address, record_data)
            checksum = calculate_checksum(record)
            record += "{:02X}\n".format(checksum)
            output_string += record

            # Reinicia as variáveis
            address += line_length
            line_length = 0
            record_data = ""

    # Adiciona a última linha, se houver dados restantes
    if line_length > 0:
        record = ""
        # Adiciona a última linha no formato S-record adequado à ‘string’ de saída
        if address <= 0xFFFF:  # 2 bytes = S1
            record = "S1{:02X}{:04X}{}".format(line_length + 3, address, record_data)
        elif address <= 0xFFFFFF:  # 3 bytes = S2
            record = "S2{:02X}{:06X}{}".format(line_length + 4, address, record_data)
        elif address <= 0xFFFFFFFF:  # 4 bytes = S3
            record = "S3{:02X}{:08X}{}".format(line_length + 5, address, record_data)
        checksum = calculate_checksum(record)
        record += "{:02X}\n".format(checksum)
        output_string += record

    return output_string


def mot_gen(destination_path, mot_list):
    all_data = 'S00E00004F464653454E5F556D6F742C\n'

    for mot in mot_list:
        all_data += mot
    all_data += 'S70500000000FA'
    with open(destination_path, 'w') as destination:
        destination.write(all_data)


# filepath = r'Arquivos WPS/rl_application.mot'
# destination_path = r"Arquivos WPS/testandoomot.mot"
# app, vector_table = mot_to_binary_rl(filepath)
# print(app['end_address'])
#
# static = {
#     "exch_mode": 0xFFFFFFFF,
#     "fw_rev": 0x00010001,
#     "vecstart": 0x1000,
#     "vecend": 0x1FFF,
#     "addstart": 0x3800,
#     "addend": 0x7E00,
#     "addcrc": 0x04FB,
#     "numslaves": 0x8,
#     "exch_mode_slaves": 0x9,
#     "first_update": 0xAAAAAAAA,
#     "prod_ver": "10101",
# }

# static_data = build_static(static)
# string = ascii_to_mot2(static_data, 0x00)
# print(static_data)
# print(string)





