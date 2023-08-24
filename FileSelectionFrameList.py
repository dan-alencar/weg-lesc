
class FileSelectionFrameList:
    def __init__(self):
        self.codeframes = []

    def addFrame(self, frame):
        self.codeframes.append(frame)

    def removeFrame(self, frame):
        self.codeframes.remove(frame)

    def clearFrames(self):
        self.codeframes.clear()

    def unpackFrames(self):
        for frame in self.codeframes:
            frame.pack_forget()
