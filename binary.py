import os
import struct
from crc import calculate_crc16
from random import randbytes


# Lê um arquivo .bin a partir do seu path e retorna este arquivo.
def read_binary_file(path):
    file = open(path, 'rb')
    content1 = file.read()
    file.close()

    return content1


# Retorna o tamanho do arquivo em bytes a partir do seu path.
def file_size(path):
    return os.path.getsize(path)


# Concatena arquivos .bin ou .mot em um arquivo .bin
def concat_files(destination_path, header, *paths):
    final_file = open(destination_path, 'wb')
    final_file.write(header)
    for path in paths[0:]:
        file = open(path, 'rb')
        content = file.read()
        file.close()
        final_file.write(content)
    final_file.close()
    return final_file


def concat_files2(destination_path, *paths):
    content = bytearray()
    i = 1
    for path in paths[0:]:
        print('code',i)
        i += 1
        content += (mot_to_binary(path, 2, 0x3800, 0x7E00))
    final_file = content
    with open(destination_path, 'wb') as destination:
        destination.write(final_file)
    return final_file


# Monta o cabeçalho do arquivo.
def build_header(header):
    header_ver = int(header['header_ver'])

    match header_ver:
        case 1:
            header_format = 'BB12s10sI'
            header['prod_id'] = header['prod_id'].ljust(12)
        case 2:
            header_format = 'BB16s10sI'
            header['prod_id'] = header['prod_id'].ljust(16)
        case _:
            raise ValueError(f"Versão do cabeçalho não suportada.")

    header['prod_ver'] = header['prod_ver'].ljust(10)
    header_data = struct.pack(
        header_format, header_ver, header['header_valid'], bytes(header['prod_id'], 'utf-8'),
        bytes(header['prod_ver'], 'utf-8'), header['length'])

    return header_data


def build_version_header(version_h, version_l
                         , offset_adds, length, interface, comm_address, code_id, offset_vec, offset_app):
    header_format = '>HHIIBBBII'
    version_header_data = struct.pack(
        header_format, version_h, version_l
        , offset_adds, length, interface, comm_address, code_id, offset_vec, offset_app)
    return version_header_data


# percorre uma linha de um aquivo .mot e separa as informações em sua estrutura
def parse_srec_line(line, firmware):
    if firmware == 2:
        record_type = line[0:2]
        data_length = int(line[2:4], 16)
        address = int(line[4:8], 16)
        data = line[8:-2].decode('utf-8')
        checksum = line[-2:]

        return {
            "record_type": record_type,
            "data_length": data_length,
            "address": address,
            "data": data,
            "checksum": checksum
        }

    if firmware == 1:
        record_type = line[0:2]
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


# completa a string de dados quando o tamanho não é multiplo de 64
def mul64(data):
    length = len(data) / 2
    if length % 64 == 0:
        return data
    else:
        return data + int(64 - (length % 64)) * 'FF'


# transforma um arquivo .mot em binário
def mot_to_binary(file_path, firmware, init_offset2, final_address):
    code1 = ''  # string que contém a primera parte do código
    code2 = ''  # string que contém a segunda parte do código
    end_address = 0  # guarda o último endereço preenchido
    previous_end_address = 0  # guarda o último endereço preenchido na iteração anterior
    lines = 0  # guarda a quantidade de linhas para determinar os endereços de inicio
    binary_data = ''

    if firmware == 2:  # rl
        with open(file_path, 'rb') as mot:
            for line in mot:
                line = line.strip()
                record = parse_srec_line(line, firmware)

                # testa se a linha armazena dados
                if record['record_type'] != b'S1':
                    pass

                else:
                    # endereço inicial do dado
                    init_address = record['address']
                    # endereço final do dado
                    end_address = record['address'] + record['data_length'] - 3

                    # verifica se a linha pertence à primeira parte
                    if record['address'] < int(0xFFF):

                        # preenche bytes vazios quando o endereço do início da linha é maior que o endereço do fim da linha anterior
                        if previous_end_address < init_address:
                            code1 += (init_address - previous_end_address) * 'FF'

                        # junta o dado à primeira string
                        code1 += record["data"]

                    # verifica se a linha pertence à segunda parte
                    elif int(init_offset2) <= record['address'] < final_address:

                        # se a linha for a primeira da segunda parte, altera o valor do endereço final da linha anterior
                        if record['address'] == int(init_offset2):
                            previous_end_address = init_offset2

                        # preenche bytes vazios quando o endereço do início da linha é maior que o endereço do fim da linha anterior
                        if previous_end_address < init_address:
                            code2 += (init_address - previous_end_address) * 'FF'

                        # junta o dado à segunda string
                        code2 += record["data"]

                    elif record['address'] >= int(final_address):
                        break

                    # atualiza o endereço final anterior
                    previous_end_address = end_address

        # completando os códigos para que o tamanho seja múltiplo de 64
        code1 = mul64(code1)
        code2 = mul64(code2)
        binary_data = bytearray.fromhex(code1 + code2)

    if firmware == 1:  # rx
        with open(file_path, 'rb') as mot:
            for line in mot:
                line = line.strip()
                record = parse_srec_line(line, firmware)

                # testa se a linha armazena dados
                if record['record_type'] != b'S3':
                    pass

                else:
                    # endereço inicial do dado
                    init_address = record['address']
                    # endereço final do dado
                    end_address = record['address'] + record['data_length'] - 5

                    if lines == 0:
                        previous_end_address = record['address']

                    # verifica se a linha pertence à primeira parte
                    if record['address'] < int(0xFFFFFEE4):

                        # preenche bytes vazios quando o endereço do início da linha é maior que o endereço do fim da linha anterior
                        if previous_end_address < init_address:
                            code1 += (init_address - previous_end_address) * 'FF'

                        # junta o dado à primeira string
                        code1 += record["data"]

                    # verifica se a linha pertence à segunda parte
                    elif record['address'] >= int(0xFFFFFEE4):

                        # se a linha for a primeira da segunda parte, altera o valor do endereço final da linha anterior
                        if record['address'] == int(0xFFFFFEE4):
                            previous_end_address = 0xFFFFFEE4

                        # junta o dado à segunda string
                        code2 += record["data"]

                    # atualiza o endereço final anterior
                    previous_end_address = end_address
                    lines += 1  # incrementa o número de linhas
        binary_data = bytearray.fromhex(code2 + code1)
    # escrevendo o arquivo binário
    code1_size = len(bytearray.fromhex(code1))
    code2_size = len(bytearray.fromhex(code2))
    return binary_data, code1_size, code2_size


# gerador de binário

def binary_gen(destination_path, header, version_header, binary_data):
    header_data = build_header(header)

    # calcula o tamanho total do arquivo com o cabeçalho e o crc
    length_total = len(binary_data) + len(version_header) + len(header_data)
    print(length_total)

    # concatena o conteúdo dos arquivos
    content = header_data + version_header + binary_data

    # calcula o crc
    crcH, crcL = calculate_crc16(content)
    if len(crcH)<2:
        crcH = '0' + crcH
    if len(crcL)<2:
        crcL = '0' + crcL
    crc = crcL + crcH + '0000'  # adiciona 2 bytes
    crc = bytearray.fromhex(crc)  # transforma em bytearray

    # escreve o conteúdo no arquivo binário de destino
    with open(destination_path, 'wb') as destination:
        destination.write(content + crc)

#
# concat_files2(r'D:\concat.bin', r'D:\00_SlaveRTDW_ApplicationIHM.mot', r'D:\01_SlaveRTDW_ApplicationRET1.mot',
#               r'D:\02_SlaveRTDW_ApplicationRET2.mot', r'D:\03_SlaveRTDW_ApplicationUCQ.mot', r'D:\04_SlaveRTDW_ApplicationRELE1.mot',
#               r'D:\05_SlaveRTDW_ApplicationRELE2.mot', r'D:\06_SlaveRTDW_ApplicationSPV.mot', r'D:\07_SlaveRTDW_ApplicationEXP.mot')

