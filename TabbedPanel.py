import customtkinter as ctk
from BodyFrame import BodyFrame

class TabbedPanel(ctk.CTkTabview):
    '''
    Menu para visualização de múltiplas janelas
    '''
    def __init__(self, master, **kwargs):
        
        super().__init__(master, **kwargs)
        self.add("Códigos")
        self.add("Microcontroladores")
        self.codeframe = BodyFrame(master=self.tab("Códigos"), repository=master.codeframe_list, type="code")
        self.codeframe.pack(fill=ctk.BOTH, expand = ctk.TRUE)
        self.controllerframe = BodyFrame(master=self.tab("Microcontroladores"), repository=master.controllerframe_list, type="controller")
        self.controllerframe.pack(fill=ctk.BOTH, expand = ctk.TRUE)
        