def generate_crc16_table():
    poly = 0x8408
    table = [0] * 256

    for i in range(256):
        crc = i
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ poly
            else:
                crc >>= 1
        table[i] = crc & 0xFFFF

    return table


def crc16_encode(data):
    crc = 0x0000
    crc_table = generate_crc16_table()

    for byte in data:
        crc = (crc >> 8) ^ crc_table[(crc ^ byte) & 0xFF]

    return crc & 0xFFFF

# def crc16_encode(data):
#     crc = 0x0000
#     poly = 0x8408
#
#     for byte in data:
#         crc ^= (byte << 8)
#         for _ in range(8):
#             if crc & 0x8000:
#                 crc = (crc << 1) ^ poly
#             else:
#                 crc <<= 1
#
#     return crc & 0xFFFF


def hex_string_to_bytearray(hex_string):
    # Remove any leading "0x" or "0X" if present
    hex_string = hex_string.replace("0x", "").replace("0X", "")

    # Ensure the length of the hex string is even
    if len(hex_string) % 2 != 0:
        hex_string = "0" + hex_string

    # Convert the hex string to a bytearray
    byte_array = bytearray.fromhex(hex_string)

    return byte_array


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

# aux = "FD730204010000FD730A04040000FBE2F4FEFFFFFD68EDFBE29822E1FFFD68ECFBEA0001FD68E30535EA0305E9A60103FBEE000001FD68E0055C630200020A050201010057454700436F72706F726174650056342E3030000501060108012501780179017B0126018C01A101A301"
# a = hex_string_to_bytearray(aux)
# print(a)
# b = crc16_encode(a)
# print(b)