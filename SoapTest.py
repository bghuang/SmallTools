import urllib2
import xml.etree.ElementTree as ET

soap_url = 'http://10.108.17.166:8210/SvcMgr'
ns1 = "{http://alcatel-lucent.com/esm/ws/svcmgr/V2_0}"

req = urllib2.Request(soap_url)

loginReq = open('/shome/sms/soap_config/1.login.op.txt','r')
contentText = loginReq.read()
loginReq.close()


req.add_header('Content-type', 'text/xml;charset=utf-8')
resp = urllib2.urlopen(req, contentText)
respXML = resp.read()

root = ET.fromstring(respXML)
sessionid = root.findall('.//'+ns1+'sessionId')[0].text
print sessionid

tree = ET.parse("/shome/sms/soap_config/35.create_group_account.txt")
root = tree.getroot()

for elem in root.findall('.//'+ns1+'sessionId'):
    elem.text = sessionid

reqdata = ET.tostring(root, "utf-8")

print reqdata