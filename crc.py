# Função: calculate_crc16
# Parâmetros de Entrada: data (dados a serem usados no cálculo do CRC)
# Saída: Tupla contendo o CRC calculado (crc_h, crc_l)
# Operação: Calcula o CRC-16 para os dados fornecidos usando o algoritmo modificado de X-25.
def calculate_crc16(data):
    crc = 0xFFFF

    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1

    if crc & 0xFF:
        crc_l = format(crc & 0xFF, 'x')
    else:
        crc_l = "00"

    if crc >> 8:
        crc_h = format(crc >> 8, 'x')
    else:
        crc_h = "00"

    return crc_h, crc_l


# Função: encode_data
# Parâmetros de Entrada: data (dados a serem codificados)
# Saída: String hexadecimal dos dados codificados com o CRC anexado
# Operação: Calcula o CRC dos dados fornecidos e anexa-o à representação hexadecimal dos dados.
def encode_data(data):
    crc = calculate_crc16(data)
    encoded_data = data + crc.to_bytes(2, byteorder='little')
    return encoded_data.hex()


# Função: verify_crc16
# Parâmetros de Entrada: data_with_crc (dados codificados com CRC)
# Saída: True se o CRC for válido, False caso contrário
# Operação: Verifica se o CRC no final dos dados corresponde ao CRC calculado dos dados restantes.
def verify_crc16(data_with_crc):
    crc = int(data_with_crc[-4:], 16)
    data = bytearray.fromhex(data_with_crc[:-4])
    calculated_crc = calculate_crc16(data)
    return crc == calculated_crc


# Função: decode_data
# Parâmetros de Entrada: data_with_crc (dados codificados com CRC)
# Saída: Dados decodificados (sem o CRC)
# Operação: Converte a representação hexadecimal dos dados para um array de bytes.
def decode_data(data_with_crc):
    data = bytearray.fromhex(data_with_crc[:-4])
    return data


# Função: file_to_byte_array
# Parâmetros de Entrada: file_path (caminho do arquivo)
# Saída: Array de bytes representando o conteúdo do arquivo
# Operação: Lê o conteúdo do arquivo no caminho especificado e retorna como um array de bytes.
def file_to_byte_array(file_path):
    try:
        with open(file_path, "rb") as file:
            byte_array = bytearray(file.read())
            return byte_array
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print("An error occurred:", str(e))


# Função: bytearray_to_hex_string
# Parâmetros de Entrada: byte_array (array de bytes a ser convertido)
# Saída: Representação hexadecimal do array de bytes
# Operação: Converte um array de bytes para uma string hexadecimal.
def bytearray_to_hex_string(byte_array):
    hex_string = ''.join(format(byte, '02X') for byte in byte_array)
    return hex_string

