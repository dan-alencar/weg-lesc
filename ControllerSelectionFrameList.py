
class ControllerSelectionFrameList:
    def __init__(self, master):
        self.controllerframes = []
        self.optionList = []
        self.master = master

    def addFrame(self, frame):
        self.controllerframes.append(frame)

    def removeFrame(self, frame):
        self.controllerframes.remove(frame)

    def clearFrames(self):
        self.controllerframes.clear()
        self.optionList.clear()

    def unpackFrames(self):
        for frame in self.controllerframes:
            frame.pack_forget()
            
    def updateList(self, repository):
        self.optionList = []
        for option in repository:
            self.optionList.append("FW " + str(option + 1))
        self.updateFrames()
    
    def updateFrames(self):
        for frame in self.controllerframes:
            # frame.optionmenu.set('Selecione uma opção')
            currentoption = frame.optionmenu.get()
            try:
                index = self.optionList.index(currentoption)
            except ValueError:
                frame.optionmenu.set("Selecione uma opção")
            frame.optionmenu.configure(values = self.optionList)