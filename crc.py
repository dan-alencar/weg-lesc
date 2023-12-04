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
        CRCL = format(crc & 0xFF, 'x')
    else:
        CRCL = "00"

    if crc >> 8:
        CRCH = format(crc >> 8, 'x')
    else:
        CRCH = "00"

    return CRCH, CRCL


def encode_data(data):
    crc = calculate_crc16(data)
    encoded_data = data + crc.to_bytes(2, byteorder='little')
    return encoded_data.hex()

def verify_crc16(data_with_crc):
    crc = int(data_with_crc[-4:], 16)
    data = bytearray.fromhex(data_with_crc[:-4])
    calculated_crc = calculate_crc16(data)
    return crc == calculated_crc

def decode_data(data_with_crc):
    data = bytearray.fromhex(data_with_crc[:-4])
    return data

def file_to_byte_array(file_path):
    try:
        with open(file_path, "rb") as file:
            byte_array = bytearray(file.read())
            return byte_array
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print("An error occurred:", str(e))

def bytearray_to_hex_string(byte_array):
    hex_string = ''.join(format(byte, '02X') for byte in byte_array)
    return hex_string

