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


# percorre uma linha de um aquivo .mot e separa as informações em sua estrutura
def parse_srec_line(line):
    record_type = line[0:2]
    data_length = int(line[2:4], 16)
    address = line[4:8]
    data = line[8:-2].decode('utf-8')
    checksum = line[-2:]

    # Preenche as linhas caso o dado seja menor que 16 bytes
    if len(data) < 32:
        for i in range(32-len(data)):
            data = data + 'F'

    print(data)

    # transforma o dado em bytearray
    data = bytearray.fromhex(data)

    return {
        "record_type": record_type,
        "data_length": data_length,
        "address": address,
        "data": data,
        "checksum": checksum
    }


# lê um arquivo .mot e armazena as informações de uma seção limitada por dois endereços
def binary_gen(destination_path, file_path, start_address, end_address):
    records = []
    within_range = False

    with open(destination_path, "wb") as destination:
        with open(file_path, "rb") as srec:
            for line in srec:
                line = line.strip()
                record = parse_srec_line(line)
                if record["record_type"] == b'S1':
                    if int(record["address"], 16) >= start_address and int(record["address"], 16) <= end_address:
                        within_range = True
                        records.append(record)
                        destination.write(record["data"])
                    elif within_range and int(record["address"], 16) > end_address:
                        break

    return records


# testando
destination_path = r'Arquivos WPS\comparar.bin'
file_path = r"Arquivos WPS\rl_application.mot"
start_address = 0x0000
end_address = 0x0FFF
srec_records = binary_gen(
    destination_path, file_path, start_address, end_address)

print(srec_records)
