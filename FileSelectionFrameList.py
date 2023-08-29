
class FileSelectionFrameList:
    def __init__(self,master):
        self.codeframes = []
        self.valid_firmware = []
        self.master = master

    def addFrame(self, frame):
        self.codeframes.append(frame)
        
    def fwValidation(self, frame):
        self.valid_firmware.append(frame)
        print(frame.name + " adicionado com sucesso")
        self.master.controllerframe_list.updateList(self.valid_firmware)
        
    def fwRemove(self,frame):
        self.valid_firmware.remove(frame)
        print(frame.name + " removido com sucesso")
        self.master.controllerframe_list.updateList(self.valid_firmware)

    def removeFrame(self, frame):
        self.codeframes.remove(frame)

    def clearFrames(self):
        self.codeframes.clear()

    def unpackFrames(self):
        for frame in self.codeframes:
            frame.pack_forget()
