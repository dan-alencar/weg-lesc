# Classe: FileSelectionFrameList
# Descrição: Gerencia uma lista de frames de seleção de arquivos.

class FileSelectionFrameList:
    # Método: __init__
    # Parâmetros de Entrada: master (janela principal)
    # Operação: Inicializa a lista de frames, a lista de firmwares válidos e a lista de índices de firmwares válidos.
    def __init__(self, master):
        self.codeframes = []
        self.valid_firmware = []
        self.valid_firmware_index = [] #testando a declaração da variável
        self.master = master

    # Método: addFrame
    # Parâmetros de Entrada: frame (frame a ser adicionado à lista)
    # Operação: Adiciona um frame à lista de frames.
    def addFrame(self, frame):
        self.codeframes.append(frame)

    # Método: fwValidation
    # Parâmetros de Entrada: frame (frame a ser validado)
    # Operação: Adiciona um frame à lista de firmwares válidos e atualiza a lista de índices de firmwares válidos.
    def fwValidation(self, frame):
        self.valid_firmware.append(frame)
        self.valid_firmware_index = []
        for option in self.valid_firmware:
            self.valid_firmware_index.append(option.index)
        self.valid_firmware_index.sort()
        print(self.valid_firmware_index)
        # print(self.valid_firmware)
        self.master.controllerframe_list.updateList(self.valid_firmware_index)

    # Método: fwRemove
    # Parâmetros de Entrada: frame (frame a ser removido da lista de firmwares válidos)
    # Operação: Remove um frame da lista de firmwares válidos e atualiza a lista de índices de firmwares válidos.
    def fwRemove(self, frame):
        if frame in self.valid_firmware:
            self.valid_firmware.remove(frame)
        index = self.searchbyIndex(self.valid_firmware_index, frame)
        if index != -1:
            self.valid_firmware_index.pop(index)
        self.master.controllerframe_list.updateList(self.valid_firmware_index)

    # Método: removeFrame
    # Parâmetros de Entrada: frame (frame a ser removido da lista de frames)
    # Operação: Remove um frame da lista de frames e da lista de firmwares válidos.
    def removeFrame(self, frame):
        self.codeframes.remove(frame)
        self.fwRemove(frame)

    # Método: clearFrames
    # Parâmetros de Entrada: Nenhum
    # Operação: Limpa a lista de frames, a lista de firmwares válidos e a lista de índices de firmwares válidos.
    def clearFrames(self):
        self.codeframes.clear()
        self.valid_firmware.clear()

    # Método: unpackFrames
    # Parâmetros de Entrada: Nenhum
    # Operação: Desempacota todos os frames da lista.
    def unpackFrames(self):
        for frame in self.codeframes:
            frame.pack_forget()

    # Método: searchFrameFile
    # Parâmetros de Entrada: option (opção de frame)
    # Operação: Procura um frame na lista de firmwares válidos com base na opção fornecida.
    def searchFrameFile(self, option):
        for frame in self.valid_firmware:
            if frame.name == option:
                return frame

    # Método: searchbyIndex
    # Parâmetros de Entrada: repository (repositório), frame (frame a ser buscado)
    # Operação: Procura o índice de um frame na lista de índices.
    def searchbyIndex(self, repository, frame):
        try:
            index = repository.index(frame.index)
            print(f"{frame} encontrado na posição {index}")
        except ValueError:
            index = -1
            print(f"{frame} não encontrado")
        return index

    # Método: searchbyName
    # Parâmetros de Entrada: repository (repositório), frame_name (nome do frame)
    # Operação: Procura o índice de um frame na lista de índices com base no nome.
    def searchbyName(self, repository, frame_name):
        frame_index = int(frame_name[2:])
        try:
            index = repository.index(frame_index-1)
            print(f"{frame_name} encontrado na posição {index}")
        except ValueError:
            index = -1
            print(f"{frame_name} não encontrado")
        return index