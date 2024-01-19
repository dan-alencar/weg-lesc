from BinaryToMot import calculate_checksum


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
            record = ""
            # Adiciona a linha no formato S-record adequado à ‘string’ de saída
            if address <= 0xFFFF:  # 2 bytes = S1
                record = "S1{:02X}{:04X}{}".format(line_length + 3, address, record_data)
            elif address <= 0xFFFFFF:  # 3 bytes = S2
                record = "S2{:02X}{:06X}{}".format(line_length + 4, address, record_data)
            elif address <= 0xFFFFFFFF:  # 4 bytes = S3
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
        record = ""
        # Adiciona a última linha no formato S-record adequado à ‘string’ de saída
        if address <= 0xFFFF:  # 2 bytes = S1
            record = "S1{:02X}{:04X}{}".format(line_length + 3, address, record_data)
        elif address <= 0xFFFFFF:  # 3 bytes = S2
            record = "S2{:02X}{:06X}{}".format(line_length + 4, address, record_data)
        elif address <= 0xFFFFFFFF:  # 4 bytes = S3
            record = "S3{:02X}{:08X}{}".format(line_length + 5, address, record_data)
        checksum = calculate_checksum(record)
        record += "{:02X}\n".format(checksum)
        output_string += record

    return output_string

    with open('C:\Users\danfi\Documents\GitHub\weg-lesc\Arquivos WPS\memoria.mot', 'w') as destination:
        destination.write(all_data)