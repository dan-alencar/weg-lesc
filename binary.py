import os


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


def concatFiles(destination_path, *paths):
    '''
    Concatena arquivos .bin ou .mot em um arquivo .bin 
    '''
    final_file = open(destination_path, 'wb')
    for path in paths[0:]:
        file = open(path, 'rb')
        content = file.read()
        file.close()
        final_file.write(content)
    final_file.close()
    return final_file
