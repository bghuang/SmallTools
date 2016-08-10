#!/usr/bin/python2.6
#-*-coding: utf-8-*-
import os
import signal
import sys
import urllib2
import xml.etree.ElementTree as ET
import subprocess
import ConfigParser
import time
import re

def soapConn(contentText):
    soap_url = 'http://10.108.17.166:8210/SvcMgr'
    req = urllib2.Request(soap_url)
    req.add_header('Content-type', 'text/xml;charset=utf-8')
    resp = urllib2.urlopen(req, contentText)
    resp_result = resp.read()
    return resp_result

ns1 = "{http://alcatel-lucent.com/esm/ws/svcmgr/V2_0}"
LoginTem = '/shome/sms/soap_config/1.login.op.txt'
LogoutTem = '/shome/sms/soap_config/2.logout.op.txt'
ActionTemp = "/shome/sms/soap_config/35.create_group_account.txt"
command = 'lwp-request -m POST -c "text/xml; charset=utf-8" -H "SOAPAction:" -ses http://10.108.17.166:8210/SvcMgr'
wsagentLog ="/sms/smslog/wsagent/wsagent_0"
usertaskLog = "/sms/smslog/usertask/uol190.03.44"
workorderLog = "/sms/smslog/usertask/workorder.log"
# Get the dir of python script locate in.
#realdir = os.path.split(os.path.realpath(__file__))[0]
patten = re.compile(r'<sessionId>(.*?)</sessionId>')

# Get current working dir
#it can use below method or
#    print os.path.abspath(os.curdir)
#    print os.path.abspath('.')

realdir = os.getcwd()

command1 = 'exec tail -f ' + wsagentLog + ' > ' + realdir + '/wsagent.log'
command2 = 'exec tail -f ' + usertaskLog + ' > ' + realdir + '/usertask.log'
command3 = 'exec tail -f ' + usertaskLog + ' > ' + realdir + '/workorder.log'

outputLog =  realdir + '/output.txt'


if len(sys.argv) < 2:
    print "Please input Action Template file name."
    quit()

ActionTemp = sys.argv[1]

origin = sys.stdout
f = open(outputLog, 'wb')
sys.stdout = f

print "Action template: ", ActionTemp

# Login

with open(LoginTem,'r') as loginReq:
    contentText = loginReq.read()


respXML = soapConn(contentText)

#print respXML

root = ET.fromstring(respXML)
sessionid = root.findall('.//'+ns1+'sessionId')[0].text


print "Session ID: ",sessionid



print "-------------------------------------------------------------------------"

print "Req XML: "
print

with open (ActionTemp, "r") as f:
    datatemplate = f.read()


#contentData = datatemplate % sessionid

contentData = patten.sub("<sessionId>" + sessionid + "</sessionId>",datatemplate)


#contentData = patten.sub(sessionid,contentText)


print contentData



print "-------------------------------------------------------------------------"
print "Resp Result:"
print

# Start monitor Logs

#p1 = subprocess.Popen('exec tail -f ' + wsagentLog + ' > ' + realdir + '/wsagent.log', shell = True)
#p2 = subprocess.Popen('exec tail -f ' + usertaskLog + ' > ' + realdir + '/usertask.log', shell = True)
#p3 = subprocess.Popen('exec tail -f ' + usertaskLog + ' > ' + realdir + '/workorder.log', shell = True)

p1 = subprocess.Popen(command1, shell = True)
p2 = subprocess.Popen(command2, shell = True)
p3 = subprocess.Popen(command3, shell = True)



#pid1 = p1.pid
#command3 = 'tail -f ' + workorderLog + ' > ' + realdir + '/workorder.log'
#command3list = command3.split()

# Start send soap request

start_time = time.localtime()

subproc = subprocess.Popen([command],stdin=subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)

#subproc.stdin,write(contentData)
stdoutdata,stderrdata = subproc.communicate(contentData)

#print "subproc.returncode: ",subproc.returncode
#print "stdoutdata: "
print stdoutdata
#print "stderrdata: ", stderrdata

respXML = stdoutdata.splitlines()[-1]


end_time = time.localtime()

'''
respXML = soapConn(contentData)
'''

# Stop monitor Logs

'''
p1.send_signal(signal.SIGINT)
p1.send_signal(signal.SIGTERM)
p2.send_signal(signal.SIGINT)
p3.send_signal(signal.SIGINT)

#p3.wait()
'''

p1.terminate()
p2.terminate()
p3.terminate()



#print logcontent

#print respXML

print "-------------------------------------------------------------------------"

print "Parsed Resp XML (for manul test analyses only)"
print
root = ET.fromstring(respXML)
for item in root.findall('.//*'):
   print item.tag, " : ", item.text



#Logout
with open(LogoutTem,'r') as logoutReq:
    contentText = logoutReq.read()

contentData = contentText % sessionid


respXML = soapConn(contentData)

print "-------------------------------------------------------------------------"
print "Session ID: ", sessionid
print "Action template: ", ActionTemp
print "Start Time: ", time.asctime(start_time)
print "End Time: ", time.asctime(end_time)
#print os.path.split(os.path.realpath(__file__))

sys.stdout = origin
f.close()

with open(outputLog, "r") as f:
    print f.read()