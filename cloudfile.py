
import urllib2
import requests
import json as json
import top
import os
import hashlib
import re     
import ProgFlash 

def downfile(fileurl, filename):    
    print "downloading file : " + fileurl + " ..."    
    f = urllib2.urlopen(fileurl)
    data = f.read()    
    with open(top.binpath + filename, "wb") as code:
        code.write(data)
    print 'download done'    
    pass 

def sha1file(filename):
    try:
        f = open(top.binpath + filename, "rb")
    except:
        return 'err'
        
    data = f.read(os.path.getsize(top.binpath+filename))
    hm = hashlib.sha1(data)
    f.close()    
    return str(hm.hexdigest())    

def checkbin():
    print 'Start check local bin files ...'
    status = True
    try:
        f = open(top.binpath + 'index.json', "rb")
    except:
        return False
        
    data = f.read(os.path.getsize(top.binpath+'index.json'))        
    js = json.loads(data)    
    
    for i in range(0, len(js['file'])):        
        x = js["file"][i]   
        if x is None: 
            pass
        else:
            if (x['sha1'] == ''):
                if (( sha1file(x['filename'])) == 'err'):
                    status = False
                else :    
                    #print 'skip file check file [', x['filename'], ' ]'
                    pass
                                   
            elif  (x['sha1'] == sha1file(x['filename'])):
                #print 'file [', x['filename'],'] check ok'
                pass                
            else:
                print 'file [', x['filename'],'] check error'
                print 'cloud sha1 = ' +  x['sha1'] + 'calc sha1 = ' + sha1file(x['filename'])                 
                status = False    
    
    if (status == False):        
        return False
    else:
        print 'all files check ok with version : ', js['ver']
        return js['ver']        
    
def getbin():
    
    url = 'http://a.vvlogic.com/index.json'
    r = requests.get(url)  
    js = json.loads(r.text)
    
    checkresult = checkbin()
    if ( checkresult == False):
        print 'local files check error.'
    elif ( js['ver'] == checkresult):
        #print 'local file check OK'
        pass
    else:
        print 'local file version mismatch with cloud'
        checkresult = False
    
    if (checkresult == False):
        print 'start to download file from cloud'
        re = requests.get(url)
    
        with open(top.binpath + "index.json", "wb") as code:
            code.write(re.content)
        
        checkresult = True
        
        for i in range(0, len(js['file'])):
        #print js["file"][i]
            x = js["file"][i]   
            if x is None: 
                pass
            else:
                print '\r\n'
                
                if ((x['filename'] == 'config.json') and (checkConfig() == True)) :
                    print 'Skip download config.json, use local file.'
                    continue
                else:
                    pass                                                    
                
                print 'get file:' ,x['filename'],'\r\n' ,x                
                downfile(x['url'],x['filename'])                    
                
                if  (x['sha1'] == sha1file(x['filename'])):
                    print 'file sha1 check pass'
                elif (x['sha1'] == ''):
                    print 'file sha1 check skip'
                else:
                    print 'config sha1 = ' +  x['sha1'] + ' calc sha1 = ' + sha1file(x['filename'])
                    print 'file sha1 check failed'
                    checkresult = False
        
        return checkresult
    
def jsonAdd (fieldstr, datastr):    
    pass

def checkConfig():
    try:
        f = open(top.binpath + "config.json", "rb")
    except:
        print 'config.json open error.'
        return False
    
    data = f.read(os.path.getsize(top.binpath+'config.json'))
    try:        
        js = json.loads(data)
    except:
        print 'config file json parse error.'
        return False
        
    if 'mqtt_server' not in js:
        print 'miss mqtt_server'
        return False        
    elif 'mqtt_port' not in js:
        print 'miss mqtt_port'
        return False
    elif 'sert_topic' not in js:
        print 'miss sert_topic'
        return False
    elif 'baudrate' not in js:
        print 'miss baudrate'
        return False

    return True

def buildConfig():    
    if (True == checkConfig()):        
        msg = "Update config file?(y/n)\r\n"    
        while True:
            typedata = raw_input(msg)
            
            if (typedata == 'y'):                
                break
            elif (typedata == 'n'):
                return
                break
            else:                
                print 'Error input = ', typedata    
    
    jsonstr = '{\r\n'
    msg = "Wifi config mode: \r\n" \
    "1 for Airkiss or smartConfig(default).\r\n" \
    "2 for Fixed in config file.\r\n"
    
    while True:
        typedata = raw_input(msg)
        
        if ((typedata == '1') or (typedata == '')):
            nextStepFlg = False
            break
        elif (typedata == '2'):
            nextStepFlg = True
            break
        else:
            nextStepFlg = False
            print 'Error input = ', typedata    

    if nextStepFlg is True:        
        msg = 'Enter ap ssid:\r\n'
        while True:
            typedata = raw_input(msg)
            
            if (typedata != ''):
                jsonstr = jsonstr + '\"ap_ssid\":\"' +  typedata + '\",\r\n'
                #print '\r\n' + jsonstr
                break        
            else:
                print 'Error input', typedata
                
        msg = 'Enter ap password:\r\n'
        while True:
            typedata = raw_input(msg)
            
            if (typedata != ''):
                jsonstr = jsonstr + '\"ap_password\":\"' +  typedata + '\",\r\n'
                #print '\r\n' + jsonstr
                break        
            else:
                print 'Error input', typedata
    
    msg = "mqtt server config: \r\n" \
    "1 for eclipse iot broker(iot.eclipse.org:1883)(default).\r\n" \
    "2 for vvloigc debug broker(f.vvlogic.com:9001,vv@vv) .\r\n" \
    "3 for user specific.\r\n" \
    
    while True:
        typedata = raw_input(msg)
        
        if ((typedata == '1') or (typedata == '')): 
            jsonstr = jsonstr + '\"mqtt_server\":\"' +  'iot.eclipse.org' + '\",\r\n'
            jsonstr = jsonstr + '\"mqtt_port\":' +  '1883' + ',\r\n'           
            nextStepFlg = False
            break
        elif (typedata == '2'):
            jsonstr = jsonstr + '\"mqtt_server\":\"' +  'f.vvlogic.com' + '\",\r\n'
            jsonstr = jsonstr + '\"mqtt_port\":' +  '9001' + ',\r\n'
            jsonstr = jsonstr + '\"mqtt_username\":' +  '\"vv\"' + ',\r\n'
            jsonstr = jsonstr + '\"mqtt_password\":' +  '\"vv\"' + ',\r\n'            
            nextStepFlg = False
            break
        elif (typedata == '3'):
            nextStepFlg = True
            break        
        else:
            nextStepFlg = False
            print 'Error input = ', typedata
    
    if nextStepFlg is True:
        msg = 'Enter mqtt server name:\r\n'
        pre = re.compile(r'\S+\.\S+$')
        while True:
            typedata = raw_input(msg)
              
            if pre.match(typedata):
                jsonstr = jsonstr + '\"mqtt_server\":\"' +  typedata + '\",\r\n'                
                break        
            else:
                print 'Error input', typedata
        
        msg = 'Enter mqtt server port(default 1883):\r\n'       
        pre = re.compile(r'\d+$')
        while True:
            typedata = raw_input(msg)          
            if (typedata == '') :
                jsonstr = jsonstr + '\"mqtt_port\":' +  '1883' + ',\r\n'
                #print '\r\n' + jsonstr
                break
            elif pre.match(typedata):
                jsonstr = jsonstr + '\"mqtt_port\":' +  typedata + ',\r\n'
                break;
            else:
                print 'Error input', typedata
                
        msg = 'Enter mqtt username (default null):\r\n'        
        while True:
            typedata = raw_input(msg)          
            if (typedata == '') :
                nextStepFlg = False                
                break            
            else:
                jsonstr = jsonstr + '\"mqtt_username\":\"' +  typedata + '\",\r\n'                
                break
            
        if nextStepFlg is True:
            msg = 'Enter mqtt password:\r\n'        
            while True:
                typedata = raw_input(msg)          
                if (typedata != '') :
                    jsonstr = jsonstr + '\"mqtt_password\":\"' +  typedata + '\",\r\n'
                    break            
                else:
                    print 'Error input = ', typedata                                    
                    break
                    
    msg = "Select baudrate: \r\n" \
    "1 for 115200(default)\r\n" \
    "2 for 9600\r\n" \
    "3 for 74880\r\n" \
    
    while True:
        typedata = raw_input(msg)
        
        if ((typedata == '1') or (typedata == '')):
            jsonstr = jsonstr + '\"baudrate\":' +  '115200' + ',\r\n'
            break
        elif (typedata == '2'):
            jsonstr = jsonstr + '\"baudrate\":' +  '9600' + ',\r\n'
            break
        elif (typedata == '2'):
            jsonstr = jsonstr + '\"baudrate\":' +  '74880' + ',\r\n'
            break
        else:
            nextStepFlg = False
            print 'Error input = ', typedata    
    
    msg = "Data topic: \r\n"    
    
    while True:
        typedata = raw_input(msg)
        
        if (typedata != ''):
            jsonstr = jsonstr + '\"sert_topic\":\"' +  typedata + '\",\r\n'
            break            
        else:
            nextStepFlg = False
            print 'Error input = ', typedata
        
    jsonstr = jsonstr + '\"end\":\"end\"\r\n}'    
    try:
        f = open(top.binpath + "config.json", "wb")    
        f.write(jsonstr)
        f.close()
    except:
        print 'write config.json error'
        return False
    
    print 'Updated local config.json file'
    return True                    

def writeAllbin (comName):
    try:
        f = open(top.binpath + "index.json", "rb")
    except:
        print 'index.json open error.'
        return False
    
    data = f.read(os.path.getsize(top.binpath+"index.json"))    
    f.close()
    
    js = json.loads(data)
    
    for i in range(0, len(js['file'])):
        
        x = js["file"][i]   
        if x is None: 
            pass
        else:
            print 'start write ' + x['filename'] + ' to ' + x['add']            
            ProgFlash.writeBin(comName, x['filename'], x['add'])
            return False
    print 'Program all bin finish.'    
    return True

    
if __name__ == '__main__':
    pass
    #writeAllbin('COM9')    
    #getbin()
    #buildConfig()
    
    
    
    
    
    
            
    