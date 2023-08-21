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
    return crc.to_bytes(2, byteorder='big')

def encode_and_compile(hex_array):
    byte_array = [int(hex_str, 16) for hex_str in hex_array]
    compiled_data = bytes(byte_array)
    
    crc = calculate_crc16(compiled_data)
    
    encoded_data = compiled_data + crc
    return encoded_data.hex()

# Example usage
input_hex_array = ["01", "00", "43", "46", "57", "31", "30","30","20","20","20","20","20","20", "76", "34", "2E", "32", "30","20","20","20","20","20","20","00","00","00"]
encoded_string = encode_and_compile(input_hex_array)
print("Encoded String:", encoded_string)
