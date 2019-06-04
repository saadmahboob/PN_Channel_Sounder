# -*- coding: utf-8 -*-
#*************
# This code is written to parse the NMEA messages
# and store Lat/Long/Alt data to a csv file
#*************

import csv
import pynmea2
import serial

USBPORT = 'COM4' # go to Device Manager to check for comm port number
BAUD_RATE = 4800
#FILENAME_INPUT = raw_input('Enter the file name: ')
#FILENAME = FILENAME_INPUT + '.csv'
FILENAME = 'GPStest.csv'
print ('\nPress Ctrl + C to quit collecting information\n')
with open(FILENAME, 'wb') as fp:
    a = csv.writer(fp, delimiter=',')
    header = ['GPS time (hh:mm:ss.ssss)', 'latitude (deg)', 'latitude direction', 'longitude (deg)', 'longitude direction', 'altitude', 'altitude units', 'number of satellites']
    a.writerow(header)
    try:
        while(True):
            with serial.Serial(USBPORT, BAUD_RATE) as ser:
                gpsString = ser.readline()
                #print s0
                if(gpsString[0:6] == '$GPGGA'):
                    msg = pynmea2.parse(gpsString, BAUD_RATE)
                    #print msg
                   
                    cols = [str(msg.timestamp), msg.latitude, msg.lat_dir,
                            msg.longitude, msg.lon_dir, str(msg.altitude),
                            msg.altitude_units, str(msg.num_sats)]
                    a.writerow(cols)
                    print cols
                      
                        
    except KeyboardInterrupt:
        pass
