from win32gui import FindWindow
from win32api import SendMessage

WM_SET_WAVE = 0x0400 + 0x0004
WM_SET_SHUTTER = 0x0400 + 0x0005;

class Mono_connections:
    def __init__(self):
        self.target = None
        self.connected = False
        self.wl = 500
        self.shutter = 0    # 0 for close, 1 for open

    def connect_to_mono(self):
        self.target = FindWindow(None, 'Mono')
        if self.target != 0:
            self.connected = True
            SendMessage(self.target, WM_SET_WAVE, self.wl, 0)
            SendMessage(self.target, WM_SET_SHUTTER, self.shutter, 0)

    def set_wl(self, wl):
        if self.connected:
            self.wl = wl
            SendMessage(self.target, WM_SET_WAVE, wl, 0)

    def set_shutter(self, shutter):
        if self.connected:
            self.shutter = shutter
            SendMessage(self.target, WM_SET_SHUTTER, shutter, 0)


