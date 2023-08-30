import os
import struct


def readBinaryFile(path):
    '''
    Lê um arquivo .bin a partir do seu path e retorna este arquivo
    '''
    file = open(path, 'rb')
    content1 = file.read()
    file.close()

    return content1


def fileSize(path):
    '''
    Retorna o tamanho do arquivo em bytes a partir do seu path
    '''
    return os.path.getsize(path)


def concatFiles(destination_path, header, *paths):
    '''
    Concatena arquivos .bin ou .mot em um arquivo .bin 
    '''
    final_file = open(destination_path, 'wb')
    final_file.write(header)
    for path in paths[0:]:
        file = open(path, 'rb')
        content = file.read()
        file.close()
        final_file.write(content)
    final_file.close()
    return final_file


def buildHeader(header_ver, header_valid, prod_id, prod_version, length):
    header_format = 'BB16s10sI'
    header_data = struct.pack(
        header_format, header_ver, header_valid, bytes(prod_id, 'utf-8'), bytes(prod_version, 'utf-8'), length)
    return header_data


# testando
hv = 0x02
hvalid = 0x00
pid = "WECC300"
pv = "V2.01"
le = 199786

header = buildHeader(hv, hvalid, pid, pv, le)
concatFiles('sask.bin', header, r'C:\Users\clara\OneDrive\Documentos\GitHub\weg-lesc\Arquivos WPS\Application_PADRAO_vector124.bin',
            r'C:\Users\clara\OneDrive\Documentos\GitHub\weg-lesc\Arquivos WPS\rl_application.mot')
# print(readBinaryFile('sask.bin'))
print(fileSize('sask.bin'))
print(fileSize(r'C:\Users\clara\OneDrive\Documentos\GitHub\weg-lesc\Arquivos WPS\Application_PADRAO_vector124.bin') +
      fileSize(r'C:\Users\clara\OneDrive\Documentos\GitHub\weg-lesc\Arquivos WPS\rl_application.mot')+32)
