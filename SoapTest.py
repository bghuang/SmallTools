import urllib2
import xml.etree.ElementTree as ET
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
ActionTemp = "/shome/sms/soap_config/35.create_group_account.txt"


config = ConfigParser.SafeConfigParser()
with open("test_config.cfg","rb") as cfgfile:
    config.readfp(cfgfile)
    sessionid =config.get("info","SessionID")
print "sid:",sessionid



#for elem in root.findall('.//'+ns1+'faultstring'):
#    print elem.text

#with open("test_config.cfg","wb") as cfgfile:
#    config.set("info","SessionID", "2")
#    config.write(cfgfile)

'''
with open(LoginTem,'r') as loginReq:
    contentText = loginReq.read()

respXML = soapConn(contentText)

#print respXML

root = ET.fromstring(respXML)
sessionid = root.findall('.//'+ns1+'sessionId')[0].text

'''

#print "Session ID: ",sessionid


print "-------------------------------------------------------------------------"

print "Req XML: "
print

with open (ActionTemp, "r") as f:
    datatemplate = f.read()

contentData = datatemplate % sessionid

print contentData


print "-------------------------------------------------------------------------"
print "Resp XML:"
print
contentText = contentData
respXML = soapConn(contentText)
print respXML

'''

print "-------------------------------------------------------------------------"

print "Parsed Restp XML (for manul test analyses only)"
print
root = ET.fromstring(respXML)
for item in root.findall('.//*'):
   print item.tag, " : ", item.text

'''