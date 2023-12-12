def generate_log_file(destination_path, wps_header):
    # firmware_content = ''
    # controller_content = ''
    configs_content = ''

    # for firmware in firmwares:
    #     firmware_content += firmware[0:]
    #
    # for controller in controllers:
    #     controller_content += controller[0:]

    with open(destination_path, 'w') as destination:
        for key in wps_header:
            print(key, ': ', str(wps_header[key]))
            destination.write(key)
            destination.write(': ')
            destination.write(str(wps_header[key]))
            destination.write('\n')



header = {
        "header_ver": 0x02,
        "header_valid": 0x00,
        "prod_id": 'WC100',
        "prod_ver": 'v4.10',
        # tamanho dos dados + cabeçalho wps + cabeçalho versionamento + crc
        "length": 12345
         }

filepath = r"C:\Users\clara\OneDrive\Área de Trabalho\logteste.txt"

generate_log_file(filepath, header)
