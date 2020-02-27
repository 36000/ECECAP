import bluetooth, subprocess
from time import sleep

class BluetoothWrap:
    def __init__(self):
        connected = False
        while not connected:
            name = 'HC-06'
            addr = '98:D3:41:FD:76:EB'
            nearby_devices = []
            found = False
            while not found:
                self.print('Searching For Device...')
                b_is_on = False
                while not b_is_on:
                    try:
                        nearby_devices = bluetooth.discover_devices(duration=3,lookup_names=True,
                                                                    flush_cache=True, lookup_class=False)
                        b_is_on = True
                    except OSError:
                        self.print('Bluetooth Still Off...')
                        sleep(1.0) # wait for bluetooth to turn on
                for device in nearby_devices:
                    if device[0] == addr and device[1] == name:
                        found = True
                        self.print('Device Found!')

            try:
                self.s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                self.s.connect((addr,1))
                self.print('Connected to ' +  addr)
                connected = True

            except bluetooth.BluetoothError as err:
                try:
                    self.print('Error Connecting: ' + err.strerror)
                except:
                    pass
                self.print('Trying again.')

    def getChar(self):
        c = self.s.recv(1)
        return c
    
    def getAudio(self):
        return self.s.recv(6000)

    def _temp(self):
        c = self.s.recv(1)
        if c == b'\xfc':
            return 's'
        if c == b'\x80':
            return 'f'
        if c == b'\xdf':
            return 'r'
        if c == b'\x00':
            return 'l'
        return 'E'

    def send(self, data):
        self.s.send(data)
    
    def print(self, string):
        print('Bluetooth-Module: ' + string)
    
    def clean(self):
        #self.cs.close()
        self.s.close()