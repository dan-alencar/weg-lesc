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
    return crc

def encode_data(data):
    crc = calculate_crc16(data)
    encoded_data = data + crc.to_bytes(2, byteorder='big')
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


# file = file_to_byte_array("C:\\Users\\danfi\\Documents\\Application_PADRAO_vector124.bin")

# # Provided input data
# # input_hex_array = ["01", "00", "43", "46", "57", "31", "30", "30", "20", "20", "20", "20", "20", "20", "76", "34", "2E", "32", "30", "20", "20", "20", "20", "20", "20", "00", "00", "00"]
# input_data = file
# # print(bytearray_to_hex_string(input_data))
# # Example usage for encoding
# encoded_data = encode_data(input_data)
# # print("Encoded Data:", encoded_data)

# # Example usage for decoding
# if verify_crc16(encoded_data):
#     decoded_data = bytearray_to_hex_string(decode_data(encoded_data))
#     print("Decoded Data:", decoded_data)
# else:
#     print("CRC verification failed. Data may be corrupted.")
