import customtkinter as ctk
from BodyFrame import BodyFrame
from ConfigurationFrame import ConfigurationFrame

class TabbedPanel(ctk.CTkTabview):
    '''
    Menu para visualização de múltiplas janelas
    '''
    def __init__(self, master, **kwargs):
        
        super().__init__(master, **kwargs)
        self.add("Firmware")
        self.add("Controllers")
        self.codeframe = BodyFrame(master=self.tab("Firmware"), repository=master.fileframe_list, type="code")
        self.codeframe.pack(fill=ctk.BOTH, expand = ctk.TRUE)
        self.controllerframe = BodyFrame(master=self.tab("Controllers"), repository=master.controllerframe_list, type="controller")
        self.controllerframe.pack(fill=ctk.BOTH, expand = ctk.TRUE)
        self.add("Config")
        self.configframe = ConfigurationFrame(master = self.tab("Config"))
        self.configframe.pack(fill=ctk.BOTH, expand = ctk.TRUE)
        