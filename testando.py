
# percorre uma linha de um aquivo .mot e separa as informações em sua estrutura
def parse_srec_line(line):
    record_type = line[0:2]
    data_length = int(line[2:4], 16)
    address = int(line[4:8],16)
    data = line[8:-2].decode('utf-8')
    checksum = line[-2:]

    # # Preenche as linhas caso o dado seja menor que 16 bytes
    # if len(data) < 32:
    #     for i in range(32-len(data)):
    #         data = data + 'F'

    # print(data)

    # # transforma o dado em bytearray
    # data = bytearray.fromhex(data)

    return {
        "record_type": record_type,
        "data_length": data_length,
        "address": address,
        "data": data,
        "checksum": checksum
    }
    
# completa a string de dados quando o tamanho não é multiplo de 64
def mul64(data):
    length = len(data)/2
    if length % 64 == 0:
        return data
    else:
        return data + int(64-(length % 64)) * 'FF'
    
    
def binary_gen2(destination_file, motfile):
    code1 = '' # string que contém a primera parte do código
    code2 = '' # string que contém a segunda parte do código
    end_address = 0 # guarda o último endereço preenchido
    previous_end_address = 0 # guarda o último endereço preenchido na iteração anterior
    
    with open(destination_file,'wb') as destination:
        with open(motfile,'rb') as mot:
            for line in mot:
                line = line.strip()
                record = parse_srec_line(line)
                
                # endereço inicial do dado
                init_address = record['address']  
                # endereço final do dado
                end_address = record['address'] + record['data_length'] - 3
                
                # verifica se a linha pertence à primeira parte
                if record['record_type'] == b'S1' and record['address'] < int(0xFFF):
                    
                    # preenche bytes vazios quando o endereço do início da linha é maior que o endereço do fim da linha anterior
                    if previous_end_address + 1 < init_address:
                        code1 += (init_address-previous_end_address)*'FF'
                        
                    # junta o dado à primeira string
                    code1 += record["data"]
                
                # verifica se a linha pertence à segunda parte    
                elif record['record_type'] == b'S1' and record['address'] >= int(0x3000):
                    
                    # se a linha for a primeira da segunda parte, altera o valor do endereço final da linha anterior
                    if record['address'] == int(0x3000):
                        previous_end_address = 0x2FFF
                        
                    # preenche bytes vazios quando o endereço do início da linha é maior que o endereço do fim da linha anterior    
                    if previous_end_address + 1 < init_address:
                        code2 += (init_address-previous_end_address)*'FF'
                        
                    # junta o dado à segunda string
                    code2 += record["data"]
                
                # atualiza o endereço final anterior
                previous_end_address = end_address
        
        # completando os códigos para que o tamanho seja múltiplo de 64              
        code1 = mul64(code1)
        code2 = mul64(code2)
        
        # escrevendo o arquivo binário
        binary_data = bytearray.fromhex(code1 + code2)
        destination.write(binary_data)
        
                    
                    
                    
                

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
binary_gen2(destination_path,file_path)
 