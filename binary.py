import os
import struct


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


#
def parse_srec_line(line):
    record_type = line[0:2]
    data_length = int(line[2:4], 16)
    address = line[4:8]
    data = bytearray(line[8:-2])
    checksum = line[-2:]

    return {
        "record_type": record_type,
        "data_length": data_length,
        "address": address,
        "data": data,
        "checksum": checksum
    }


def read_srec_file(file_path, start_address, end_address):
    records = []
    within_range = False

    with open(file_path, "rb") as srec:
        for line in srec:
            line = line.strip()
            record = parse_srec_line(line)
            if int(record["address"], 16) >= start_address and int(record["address"], 16) <= end_address:
                within_range = True
                records.append(record)
            elif within_range and int(record["address"], 16) > end_address:
                break

    return records


# testando
file_path = r"Arquivos WPS\rl_application.mot"
start_address = 0x0050
end_address = 0x2000
srec_records = read_srec_file(file_path, start_address, end_address)

print(srec_records)

# hv = 0x02
# hvalid = 0x34
# pid = "WECC300"
# pv = "V2.0145"
# le = 199786

# header = buildHeader(hv, hvalid, pid, pv, le)
# concatFiles(r'Arquivos Wps\sask.bin', header, r'C:\Users\clara\OneDrive\Documentos\GitHub\weg-lesc\Arquivos WPS\Application_PADRAO_vector124.bin',
#             r'C:\Users\clara\OneDrive\Documentos\GitHub\weg-lesc\Arquivos WPS\rl_application.mot')
# # print(readBinaryFile('sask.bin'))
# print(fileSize(r'Arquivos Wps\sask.bin'))
# print(fileSize(r'C:\Users\clara\OneDrive\Documentos\GitHub\weg-lesc\Arquivos WPS\Application_PADRAO_vector124.bin') +
#       fileSize(r'C:\Users\clara\OneDrive\Documentos\GitHub\weg-lesc\Arquivos WPS\rl_application.mot')+32)

# header2 = buildHeader(hv, hvalid, pid, pv, le)
# concatFiles(r'Arquivos Wps\teste.bin', header)
