
class SelectionFrameList:
    def __init__(self):
        self.all_frames = []

    def addFrame(self, frame):
        self.all_frames.append(frame)

    def removeFrame(self, frame):
        self.all_frames.remove(frame)

    def clearFrames(self):
        self.all_frames.clear()

    def unpackFrames(self):
        for frame in self.all_frames:
            frame.pack_forget()
