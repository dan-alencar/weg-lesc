import os
import struct
from crc import calculate_crc16


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


# Monta o cabeçalho do arquivo.
def build_header(header_ver, header_valid, prod_id, prod_version, length):
    header_format = 'BB16s10sI'
    header_data = struct.pack(
        header_format, header_ver, header_valid, bytes(prod_id, 'utf-8'), bytes(prod_version, 'utf-8'), length)
    return header_data


# Monta o versionamento do arquivo.
def build_version(length, version_h, version_l, offset_adds, interface, comm_address, code_id):
    header_format = 'HHIIBBB'
    version_data = struct.pack(header_format, version_h, version_l, offset_adds, length, interface, comm_address, code_id)
    return version_data


# percorre uma linha de um aquivo .mot e separa as informações em sua estrutura
def parse_srec_line(line):
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


# completa a string de dados quando o tamanho não é multiplo de 64
def mul64(data):
    length = len(data)/2
    if length % 64 == 0:
        return data
    else:
        return data + int(64-(length % 64)) * 'FF'


# transforma um arquivo .mot em binário
def mot_to_binary(file_path):
    code1 = ''  # string que contém a primera parte do código
    code2 = ''  # string que contém a segunda parte do código
    end_address = 0  # guarda o último endereço preenchido
    previous_end_address = 0  # guarda o último endereço preenchido na iteração anterior

    
    with open(file_path, 'rb') as mot:
        for line in mot:
            line = line.strip()
            record = parse_srec_line(line)

            # endereço inicial do dado
            init_address = record['address']
            # endereço final do dado
            end_address = record['address'] + record['data_length'] - 3

            # verifica se a linha pertence à primeira parte
            if record['record_type'] == b'S1' and record['address'] < int(0xFFF):

                # preenche bytes vazios quando o endereço do início da linha é maior que o endereço do fim da linha anterior
                if previous_end_address < init_address:
                    code1 += (init_address-previous_end_address)*'FF'

                # junta o dado à primeira string
                code1 += record["data"]

            # verifica se a linha pertence à segunda parte
            elif record['record_type'] == b'S1' and record['address'] >= int(0x3000):

                # se a linha for a primeira da segunda parte, altera o valor do endereço final da linha anterior
                if record['address'] == int(0x3000):
                    previous_end_address = 0x3000

                # preenche bytes vazios quando o endereço do início da linha é maior que o endereço do fim da linha anterior
                if previous_end_address < init_address:
                    code2 += (init_address-previous_end_address)*'FF'

                # junta o dado à segunda string
                code2 += record["data"]

            # atualiza o endereço final anterior
            previous_end_address = end_address

    # completando os códigos para que o tamanho seja múltiplo de 64
    code1 = mul64(code1)
    code2 = mul64(code2)

    # escrevendo o arquivo binário
    code1_size = len(bytearray.fromhex(code1))
    code2_size = len(bytearray.fromhex(code2))
    binary_data = bytearray.fromhex(code1 + code2)
    return binary_data


# gerador de binário
def binary_gen(destination_path, file_path, header, version):

    # informações do código
    binary_data = mot_to_binary(file_path)

    # calcula o tamanho total do arquivo com o cabeçalho e o crc
    length_total = len(binary_data) + len(version) + 36
    print(length_total)

    # cabeçalho
    header_data = build_header(
        header['header_ver'], header['header_valid'], header['prod_id'], header['prod_ver'], length_total)

    # concatena o conteúdo dos arquivos
    content = header_data + version + binary_data

    # calcula o crc
    crc = calculate_crc16(content)
    crc = hex(crc)+'0000'  # adiciona 2 bytes
    crc = bytearray.fromhex(crc[2:])  # transforma em bytearray

    # escreve o conteúdo no arquivo binário de destino
    with open(destination_path, 'wb') as destination:
        destination.write(content+crc)


# testando

header = {
    "header_ver": 0x02,
    "header_valid": 0x00,
    "prod_id": "CFW510",
    "prod_ver": "V2.01"
}

version = {
    "version_h": 0x0002,
    "version_l": 0x0002,
    "offset_adds": 0x00000045,
    "interface": 2,
    "comm_address": 0x46,
    "code_id": 0x12
}

destination_path = r'Arquivos WPS\comparar.bin'
versionamento = r'Arquivos WPS\binary\versionamento.bin'
file_path = r'Arquivos WPS\rl_application.mot'

# srec_records = binary_gen(
#     destination_path, file_path, header)