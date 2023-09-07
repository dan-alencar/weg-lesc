
class FileSelectionFrameList:
    def __init__(self,master):
        self.codeframes = []
        self.valid_firmware = []
        self.master = master

    def addFrame(self, frame):
        self.codeframes.append(frame)
        
    def fwValidation(self, frame):
        self.valid_firmware.append(frame)
        # print(frame.name + " adicionado com sucesso")
        self.aux = []
        for option in self.valid_firmware:
            self.aux.append(option.index)
        self.aux.sort()
        print(self.aux)
        self.master.controllerframe_list.updateList(self.aux)
        
    def fwRemove(self,frame):
        self.valid_firmware.remove(frame)
        index = self.searchbyIndex(self.aux, frame)
        # print(frame.name + " removido com sucesso")
        if index!=-1:
            self.aux.remove(index)
        self.master.controllerframe_list.updateList(self.aux)

    def removeFrame(self, frame):
        self.codeframes.remove(frame)
        self.fwRemove(frame)

    def clearFrames(self):
        self.codeframes.clear()
        self.valid_firmware.clear()

    def unpackFrames(self):
        for frame in self.codeframes:
            frame.pack_forget()
    
    def searchbyIndex(self, repository, frame):
        try:
            index = repository.index(frame.index)
            print(f"{frame} encontrado na posição {index}")
        except ValueError:
            index = -1
            print(f"{frame} não encontrado")
        return index