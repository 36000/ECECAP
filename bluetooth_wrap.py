import bluetooth, subprocess
import scipy.signal as scs
import struct
from time import sleep

class BluetoothWrap:
    def __init__(self, sample_size=1600):
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
        self.sample_size = sample_size

    def getChar(self):
        return self.s.recv(1)
    
    def getAudio(self):
        signal = bytearray()
        while len(signal) < 1600:
            signal.extend(self.s.recv(self.sample_size))
        
        return signal

        try:
            x = struct.unpack('f', signal)
        except struct.error:
            return signal
        return x


        downsample = 16

        pdm_b = []
        for ba in signal:
            for b in bin(ba)[2:]:
                pdm_b.append(int(b))

        return pdm_b

        b, a = scs.butter(3, 0.05)
        pdm_b = scs.lfilter(b, a, pdm_b)

        try:
            return scs.decimate(pdm_b, downsample).copy(order='C')
        except ValueError:
            return None

    def send(self, data):
        self.s.send(data)
    
    def print(self, string):
        print('Bluetooth-Module: ' + string)
    
    def clean(self):
        self.s.close()