#import os
import csv
import pynmea2
import serial

#*************
# Code adapted from Austin Alberts (aalberts@ntia.doc.gov)
# and modified by Linh Vu

# Requirement: Windows , Python 2.x, MR-350PS4 GPS receiver

# This code is written to parse the NMEA messages
# and store Lat/Long/Alt data to a csv file
#*************

USBPORT = 'COM4' # go to Device Manager to check for comm port number
BAUD_RATE = 4800
#FILENAME_INPUT = raw_input('Enter the file name: ')
#FILENAME = FILENAME_INPUT + '.csv'
FILENAME = 'GPStest.csv'
print ("Press Ctrl + C to quit collecting information\n")
with open(FILENAME, 'wb') as fp:
    a = csv.writer(fp, delimiter=',')
    try:
        while(1):
            with serial.Serial(USBPORT, BAUD_RATE) as ser:
                s0 = ser.read()
                #print s0
                if(s0 == '$'):
                    s1 = ser.readline()
                    #print s1
                    msg = pynmea2.parse(s1, BAUD_RATE)
                    #print msg
                    if (s1[0:5] == 'GPGGA'):
                        cols = [str(msg.timestamp), msg.latitude, msg.lat_dir,
                                msg.longitude, msg.lon_dir, str(msg.altitude),
                                msg.altitude_units, str(msg.num_sats)]
                        a.writerow(cols)
                        print cols
    except KeyboardInterrupt:
        pass
