import struct


def build_header(header_ver, header_valid, prod_id, prod_version, length):
    header_format = 'BB16s10sI'
    header_data = struct.pack(
        header_format, header_ver, header_valid, bytes(prod_id, 'utf-8'), bytes(prod_version, 'utf-8'), length)
    return header_data


header_ver = 0x02
header_valid = 0x00
prod_id = "CFW510"
prod_ver = "V2.01"
length = 0x1000

header = build_header(header_ver, header_valid, prod_id, prod_ver, length)
header = bytearray(header)
print(header)

destination_path = r'Arquivos WPS\teste.bin'
with open(destination_path, 'wb') as file:
    file.write(header)
