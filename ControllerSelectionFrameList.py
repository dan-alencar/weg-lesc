
class ControllerSelectionFrameList:
    def __init__(self):
        self.controllerframes = []
        self.optionList = []

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
            
    def updateFrames(self):
        for frame in self.controllerframes:
            frame.optionmenu.configure(values = self.optionList)
            
    def updateList(self, repository):
        self.optionList = []
        for option in repository:
            self.optionList.append(option.name)
        self.updateFrames()