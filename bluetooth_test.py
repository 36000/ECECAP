import wiringpi

wiringpi.wiringPiSetup()
serial = wiringpi.serialOpen('/dev/rfcomm0',9600)
wiringpi.serialPuts(serial,'b')