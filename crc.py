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


    # crc = invert_crc(crc)

    if crc & 0xFF:
        CRCL = format(crc & 0xFF, 'x')
    else:
        CRCL = "00"

    if crc >> 8:
        CRCH = format(crc >> 8, 'x')
    else:
        CRCH = "00"

    return CRCH, CRCL



def invert_crc(crc):
    # Original hexadecimal string
    original_hex_string = "5C00"

    # Convert hexadecimal string to integer
    original_variable = int(original_hex_string, 16)

    # Convert integer to bytes and invert the bytes
    inverted_bytes = original_variable.to_bytes((original_variable.bit_length() + 7) // 8, byteorder='big')
    inverted_variable = int.from_bytes(inverted_bytes[::-1], byteorder='big')

    # Convert the inverted integer back to a hexadecimal string with the same length
    inverted_hex_string = format(inverted_variable, f'0{len(original_hex_string)}X')

    print("Original hexadecimal string:", original_hex_string)
    print("Inverted hexadecimal string:", inverted_hex_string)

    # mask1 = 0b1111111100000000
    # mask2 = 0b0000000011111111
    #
    # part1 = crc & mask1
    # part1 >>= 8
    # part2 = crc & mask2
    # part2 <<= 8
    #
    # crc = part1 ^ part2
    #
    # return crc

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


invert_crc(0x5CAB)
