
class ControllerSelectionFrameList:
    def __init__(self):
        self.controllerframes = []

    def addFrame(self, frame):
        self.controllerframes.append(frame)

    def removeFrame(self, frame):
        self.controllerframes.remove(frame)

    def clearFrames(self):
        self.controllerframes.clear()

    def unpackFrames(self):
        for frame in self.controllerframes:
            frame.pack_forget()
