class FileSelectionFrameList:
    def __init__(self,master):
        self.codeframes = []
        self.valid_firmware = []
        self.valid_firmware_index = [] #testando a declaração da variável
        self.master = master

    def addFrame(self, frame):
        self.codeframes.append(frame)
        
    def fwValidation(self, frame):
        self.valid_firmware.append(frame)
        self.valid_firmware_index = []
        for option in self.valid_firmware:
            self.valid_firmware_index.append(option.index)
        self.valid_firmware_index.sort()
        print(self.valid_firmware_index)
        # print(self.valid_firmware)
        self.master.controllerframe_list.updateList(self.valid_firmware_index)
        
    def fwRemove(self,frame):
        if frame in self.valid_firmware:
            self.valid_firmware.remove(frame)
        index = self.searchbyIndex(self.valid_firmware_index, frame)
        if index!=-1:
            self.valid_firmware_index.pop(index)
        self.master.controllerframe_list.updateList(self.valid_firmware_index)

    def removeFrame(self, frame):
        self.codeframes.remove(frame)
        self.fwRemove(frame)

    def clearFrames(self):
        self.codeframes.clear()
        self.valid_firmware.clear()

    def unpackFrames(self):
        for frame in self.codeframes:
            frame.pack_forget()
    
    def searchFrameFile(self, option):
        for frame in self.valid_firmware:
            if frame.name == option:
                return frame
    
    def searchbyIndex(self, repository, frame):
        try:
            index = repository.index(frame.index)
            print(f"{frame} encontrado na posição {index}")
        except ValueError:
            index = -1
            print(f"{frame} não encontrado")
        return index
    
    def searchbyName(self, repository, frame_name):
        frame_index = int(frame_name[2:])
        try:
            index = repository.index(frame_index-1)
            print(f"{frame_name} encontrado na posição {index}")
        except ValueError:
            index = -1
            print(f"{frame_name} não encontrado")
        return index