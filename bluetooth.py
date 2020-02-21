import wiringpi, bluetooth, subprocess

class Bluetooth:
    def __init__(self, channel=0):
        nearby_devices = []
        while len(nearby_devices) < 0:
            print('Bluetooth-Module: Searching For Devices...')
            nearby_devices = bluetooth.discover_devices(duration=8,lookup_names=True,
                                                        flush_cache=True, lookup_class=False)
        name = 'HC-06'
        addr = '98:D3:41:FD:76:EB'
        port = 1         # RFCOMM port
        password = "1111" # passkey of the device you want to connect

        subprocess.call("kill -9 `pidof bluetooth-agent`", shell=True)
        status = subprocess.call("bluetooth-agent " + password + " &", shell=True)

        # Now, connect in the same way as always with PyBlueZ
        try:
            s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            s.connect((addr,port))
        except bluetooth.btcommon.BluetoothError as err:
            # Error handler
            pass



        wiringpi.wiringPiSetup()
        self.serial = wiringpi.serialOpen('/dev/rfcomm'+str(channel),9600)
        #self.offset = 141

    def getChar(self):
        c = wiringpi.serialGetchar(self.serial)
        wiringpi.serialFlush(self.serial)
        if c == -1:
            return c
        else:
            return c
            #return chr(c - self.offset)
    
    def putChar(self, char):
        return wiringpi.serialPuts(self.serial, char)