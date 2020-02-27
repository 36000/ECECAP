import wiringpi, bluetooth, subprocess

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
                nearby_devices = bluetooth.discover_devices(duration=5,lookup_names=True,
                                                            flush_cache=True, lookup_class=False)
                for device in nearby_devices:
                    if device[0] == addr and device[1] == name:
                        found = True
                        self.print('Device Found!')

            try:
                self.s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                self.s.connect((addr,1))
                # self.s.listen(1)

                # uuid = "a3259ff2-c323-476f-baa9-fdd93248350b"
                # bluetooth.advertise_service(
                #     self.s,
                #     "SampleServer",
                #     service_id = uuid,
                #     service_classes = [uuid, bluetooth.SERIAL_PORT_CLASS],
                #     profiles = [bluetooth.SERIAL_PORT_PROFILE]
                # )
                   
                # self.cs, c_addr = self.s.accept()

                self.print('Connected to ' +  addr)
                connected = True

            except bluetooth.BluetoothError as err:
                try:
                    self.print('Error Connecting: ' + err.strerror)
                except:
                    pass
                self.print('Trying again.')

    def getChar(self):
        self.s.recv(1024)
    
    def send(self, data):
        self.s.send(data)
    
    def print(self, string):
        print('Bluetooth-Module: ' + string)
    
    def clean(self):
        #self.cs.close()
        self.s.close()