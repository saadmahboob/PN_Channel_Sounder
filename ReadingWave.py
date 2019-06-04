import visa


try:
    #Open Connection
    rm = visa.ResourceManager('C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\agvisa\\agbin\\visa32.dll')
    #Connect to VISA Address
    #LAN - VXI-11 Connection:  'TCPIP0::xxx.xxx.xxx.xxx::inst0::INSTR'
    #LAN - HiSLIP Connection:  'TCPIP0::xxx.xxx.xxx.xxx::hislip0::INSTR'
    #USB Connection: 'USB0::xxxxxx::xxxxxx::xxxxxxxxxx::0::INSTR'
    #GPIB Connection:  'GPIP0::xx::INSTR'
    Address = 'TCPIP0::169.254.112.196::inst0::INSTR'
    
    myinst = rm.open_resource(Address)
    
    myinst.clear()
    
    #Set Timeout - 10 seconds
    myinst.timeout =  10000    
    idn = myinst.query("*IDN?")
    print 'Connected to ' + idn
    
    myinst.write(':FORMat:TRACe:DATA REAL,32')
    myinst.write(':FORMat:BORDer SWAPped')
    data = myinst.query_binary_values(':fetch:wav2?')
    
    myinst.clear()
    myinst.close()
    
    print 'done'
    
except Exception as err:
    #This is included to properly close the instrument connection in case of any errors
    if myinst != None:
        myinst.close()
        
    print 'Exception: ' + str(err.message)