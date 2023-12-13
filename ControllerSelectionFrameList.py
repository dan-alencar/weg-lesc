# Classe: ControllerSelectionFrameList
# Descrição: Gerencia uma lista de frames de seleção de controladores.
class ControllerSelectionFrameList:
    # Método: __init__
    # Parâmetros de Entrada: master (janela principal)
    # Operação: Inicializa a lista de frames e a lista de opções.
    def __init__(self, master):
        self.controllerframes = []
        self.optionList = []
        self.master = master

    # Método: addFrame
    # Parâmetros de Entrada: frame (frame a ser adicionado à lista)
    # Operação: Adiciona um frame à lista de frames.
    def addFrame(self, frame):
        self.controllerframes.append(frame)

    # Método: removeFrame
    # Parâmetros de Entrada: frame (frame a ser removido da lista)
    # Operação: Remove um frame da lista de frames.
    def removeFrame(self, frame):
        self.controllerframes.remove(frame)

    # Método: clearFrames
    # Parâmetros de Entrada: Nenhum
    # Operação: Limpa a lista de frames e a lista de opções.
    def clearFrames(self):
        self.controllerframes.clear()
        self.optionList.clear()

    # Método: unpackFrames
    # Parâmetros de Entrada: Nenhum
    # Operação: Desempacota todos os frames da lista.
    def unpackFrames(self):
        for frame in self.controllerframes:
            frame.pack_forget()

    # Método: updateList
    # Parâmetros de Entrada: repository (repositório de opções)
    # Operação: Atualiza a lista de opções com base no repositório e, em seguida, atualiza os frames.
    def updateList(self, repository):
        self.optionList = []
        for option in repository:
            self.optionList.append("FW " + str(option + 1))
        self.updateFrames()

    # Método: updateFrames
    # Parâmetros de Entrada: Nenhum
    # Operação: Atualiza os frames com as opções da lista.
    def updateFrames(self):
        for frame in self.controllerframes:
            # frame.optionmenu.set('Selecione uma opção')
            currentoption = frame.optionmenu.get()
            try:
                index = self.optionList.index(currentoption)
            except ValueError:
                frame.optionmenu.set("Selecione uma opção")
            frame.optionmenu.configure(values = self.optionList)