

import esptool
from string import Template
import sys
import top

#@Timeout.timelimited(5)
def eraseChip(comName):
    try:    
        sys.argv=(
                Template("esptool.py --port " + comName + " erase_flash")
                    .substitute(globals())
                    .split()
                    )    
        esptool.main()
    except:
        print 'erase chip error'
    
def writeBin(comName, filename, address):
    
    status = True
    cmd = "esptool.py --port " + comName + " write_flash -fm dout -fs 8m " + address + " " + top.binpath + filename
    #print cmd
    try:
        sys.argv=(
                Template(cmd)
                    .substitute(globals())
                    .split()
                    )    
        esptool.main()
    except:
        print 'write bin ' + filename + ' error'
        status = False
    pass

    return status



    
