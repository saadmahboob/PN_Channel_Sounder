import time
import serial

ser=serial.Serial(
    port='COM5',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE
)

#ser.open()
ser.isOpen()

ser.write('SN?\r\n')
#ser.write('ID?\r\n')
out=''
time.sleep(2)
while ser.inWaiting() > 0:
    out += ser.read(1)
if out != '':
    print ">>" + out
ser.close()


