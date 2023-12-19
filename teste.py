def calculate_checksum(data):
    # Calculate checksum using 0xFF - (sum & 0xFF)
    checksum = (0xFF - (sum(data) & 0xFF)) & 0xFF
    return checksum


def bin_to_srec(input_file, output_file, max_data_size=16):
    with open(input_file, 'rb') as f:
        data = f.read()

    with open(output_file, 'w') as f:
        address = 0
        while address < len(data):
            chunk_size = min(max_data_size, len(data) - address)
            chunk = data[address : address + chunk_size]

            # Calculate the checksum
            checksum = calculate_checksum(chunk)

            # Write SREC record to the file
            f.write('S1{:02X}{:04X}'.format(chunk_size + 3, address))
            f.write(''.join('{:02X}'.format(byte) for byte in chunk))
            f.write('{:02X}\n'.format(checksum))

            address += chunk_size

        # Write the S7 record at the end of the file with the starting address
        f.write('S903{:04X}{:02X}\n'.format(0, (~(0 + 3) & 0xFF)))


if __name__ == "__main__":
    input_file = r"C:\Users\clara\OneDrive\Área de Trabalho\rtdwbin.bin"
    output_file = r"C:\Users\clara\OneDrive\Área de Trabalho\rtdwbin.mot"
    bin_to_srec(input_file, output_file)


