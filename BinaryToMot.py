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
def mot_to_binary(file_path, firmware):
    code1 = ''  # string que contém a primera parte do código
    code2 = ''  # string que contém a segunda parte do código
    previous_end_address = 0  # guarda o último endereço preenchido na iteração anterior
    lines = 0  # guarda a quantidade de linhas para determinar os endereços de inicio
    binary_data = ''
    code = 1

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

                    # verifica se a linha pertence à segunda parte, se houve um pulo >= 128 bytes
                    if init_address - previous_end_address >= 128 and code == 1:
                        code = 2  # indica que houve uma mudança para code 2
                        previous_end_address = record['address']

                    # verifica se houve um segundo pulo >= 128 bytes, indicando fim das informações
                    elif init_address - previous_end_address >= 128 and code == 2:
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
    return code1, code2


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
            # Adiciona a linha no formato S-record S3 à string de saída
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
        record = "S3{:02X}{:04X}{}\n".format(line_length + 5, address, record_data)
        checksum = calculate_checksum(record)
        record += "{:02X}\n".format(checksum)
        output_string += record

    return output_string


def mot_gen(destination_path, mot_data):
    with open(destination_path, 'w') as destination:
        destination.write(mot_data)


filepath = r'Arquivos WPS/rl_application.mot'
destination_path = r'Arquivos WPS/testandoomot.mot'
code1, code2 = mot_to_binary(filepath, 2)
print(code1)
result_mot_string = ascii_to_mot(code1, 0)
mot_gen(destination_path, result_mot_string)
print(result_mot_string)


