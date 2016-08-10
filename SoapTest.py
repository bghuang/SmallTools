import xml.etree.ElementTree as ET
import subprocess
import ConfigParser

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

if len(sys.argv) < 2:
    print "Please input Action Template file name."
    quit()

ActionTemp = sys.argv[1]

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

contentData = datatemplate % sessionid

print contentData



print "-------------------------------------------------------------------------"
print "Resp Result:"
print

subproc = subprocess.Popen([command],stdin=subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)

#subproc.stdin,write(contentData)
stdoutdata,stderrdata = subproc.communicate(contentData)

#print "subproc.returncode: ",subproc.returncode
#print "stdoutdata: "
print stdoutdata
#print "stderrdata: ", stderrdata

respXML = stdoutdata.splitlines()[-1]

'''
respXML = soapConn(contentData)

'''

#print respXML

print "-------------------------------------------------------------------------"

print "Parsed Restp XML (for manul test analyses only)"
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