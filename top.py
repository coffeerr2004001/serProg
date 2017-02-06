'''
serProg for serT
fangbo 2017.02.06
'''
import re
import platform
import scanwin
import cloudfile

binpath = './bin/'
#comport = 'COM1'

if __name__ == '__main__':
        
    
    if (platform.architecture()[1] != 'WindowsPE'):
        pass
        #print 'support windows only.'
        #exit()
    else:
        print 'Available com port:\r\n----'
        for port, desc, hwid in sorted(scanwin.comports()):
            print("{}: {} [{}]".format(port, desc, hwid))

    pcom1 = re.compile(r'(C|c)(O|o)(M|m)\d+$')    
    while True:
        comnumber = raw_input("Enter com number\r\n")
        
        if ((pcom1.match(comnumber))):                    
            break
        else:
            print 'Error input = ', comnumber           
    
    cloudfile.getbin()
    cloudfile.buildConfig()    
    
    cloudfile.writeAllbin(comnumber)   
    
            
       
   
    
