import os
import struct
from crc import calculate_crc16


# Função: read_binary_file
# Parâmetros de Entrada: path (caminho do arquivo binário)
# Saída: Conteúdo do arquivo binário lido
# Operação: Abre o arquivo binário no caminho especificado, lê seu conteúdo e retorna.
def read_binary_file(path):
    file = open(path, 'rb')
    content1 = file.read()
    file.close()

    return content1


# Função: file_size
# Parâmetros de Entrada: path (caminho do arquivo)
# Saída: Tamanho do arquivo em bytes
# Operação: Obtém e retorna o tamanho do arquivo no caminho especificado.
def file_size(path):
    return os.path.getsize(path)


# Função: concat_files
# Parâmetros de Entrada: destination_path (caminho do arquivo de destino), header (cabeçalho),
# paths (caminhos dos arquivos a serem concatenados)
# Saída: Arquivo binário resultante da concatenação
# Operação: Abre os arquivos especificados, concatena o conteúdo junto com o cabeçalho
# e salva o resultado no arquivo de destino.
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


# Função: concat_files2
# Parâmetros de Entrada: destination_path (caminho do arquivo de destino),
# paths (caminhos dos arquivos a serem concatenados)
# Saída: Arquivo binário resultante da concatenação
# Operação: Converte o conteúdo dos arquivos especificados para bytearray e concatena.
# Salva o resultado no arquivo de destino.
def concat_files2(destination_path, *paths):
    final_file = bytearray()
    i = 1
    for path in paths[0:]:
        print()
        print(path)
        i += 1
        content, _, _ = mot_to_binary(path[0], path[1], 0x3800, 0x7E00)
        final_file += content
    with open(destination_path, 'wb') as destination:
        destination.write(final_file)
    return final_file


# Função: build_header
# Parâmetros de Entrada: header (dicionário com informações do cabeçalho)
# Saída: Dados do cabeçalho empacotados
# Operação: Constrói o cabeçalho conforme a versão especificada no dicionário e o empacota.
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


# Função: build_version_header
# Parâmetros de Entrada: version_h, version_l, offset_adds, length, interface,
# comm_address, code_id, offset_vec, offset_app, optional
# Saída: Dados do cabeçalho da versão empacotados
# Operação: Empacota os parâmetros fornecidos para formar o cabeçalho do versionamento.
def build_version_header(version_h, version_l, offset_adds, length, interface,
                         comm_address, code_id, offset_vec, offset_app, optional):
    header_format = '>HHIIBBBIIB'
    version_header_data = struct.pack(
        header_format, version_h, version_l
        , offset_adds, length, interface, comm_address, code_id, offset_vec, offset_app, optional)
    return version_header_data


# Função: parse_srec_line
# Parâmetros de Entrada: line (linha do arquivo .mot), firmware (tipo de firmware)
# Saída: Dicionário contendo informações da linha
# Operação: Analisa a linha do arquivo .mot e extrai informações com base no tipo de firmware.
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


# Função: mul64
# Parâmetros de Entrada: data (string de dados)
# Saída: String de dados com tamanho múltiplo de 64
# Operação: Completa a string de dados com 'FF' para tornar seu tamanho múltiplo de 64.
def mul64(data):
    length = len(data) / 2
    if length % 64 == 0:
        return data
    else:
        return data + int(64 - (length % 64)) * 'FF'


# Função: mot_to_binary
# Parâmetros de Entrada: file_path, firmware, init_offset2, final_address
# Saída: Dados binários resultantes da conversão do arquivo .mot
# Operação: Converte o conteúdo de um arquivo .mot para dados binários, divididos em duas partes
# com base nos parâmetros fornecidos.
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
    print('code 1: ', code1_size)
    code2_size = len(bytearray.fromhex(code2))
    print('code 2: ', code2_size)
    return binary_data, code1_size, code2_size


# Função: binary_gen
# Parâmetros de Entrada: destination_path, header, version_header, binary_data
# Saída: Arquivo binário resultante da geração
# Operação: Gera um arquivo binário combinando cabeçalho, cabeçalho de versão e dados binários.
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



# concat_files2(r'F:\CORPORATE_MOT\concatenado.bin', (r"F:\CORPORATE_MOT\231208B_Corporate_8_2M.mot", 1),(r"F:\CORPORATE_MOT\231208B_Hardlock_8.mot", 2), (r"F:\CORPORATE_MOT\231208B_IHM_8.mot", 2))

