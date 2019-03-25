import json

from os.path import dirname, abspath, join
import sys

# Find code directory relative to our directory
THIS_DIR = dirname(__file__)
DISC_DIR = abspath(join(join(THIS_DIR, 'discovery'), 'lib'))
AUTH_DIR = abspath(join(join(THIS_DIR, 'authorization'), 'lib'))
sys.path.append(DISC_DIR)
sys.path.append(AUTH_DIR)

import Domainconnect_auth

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class TestResults:

    def __init__(self):
        self.passCount = 0
        self.failCount = 0

    def Reset(self):
        self.passCount = 0
        self.failCount = 0
        
    def Pass(self, message=None):
        self.passCount = self.passCount + 1

        final_message = bcolors.OKGREEN + 'Passed' + bcolors.ENDC
        if message:
            final_message = final_message + ': ' + message
        print(final_message)

    def Fail(self, message=None):
        self.failCount = self.failCount + 1

        final_message = bcolors.FAIL + 'Failed' + bcolors.ENDC
        if message:
            final_message = final_message + ': ' + message
        print(final_message)

_testResults = TestResults()

def RunTests():
    
    _testResults.Reset()
    
    ZoneTests()

    print("Failed Count = " + str(_testResults.failCount))
    print("Passed Count = " + str(_testResults.passCount))

def ZoneTests():

    tests = list()
    #NS Record
    tests.append({
      "title": "Converting NS record from cPanel to DomainConnect",
      "from_cpanel": json.loads('[{"nsdname":"ns1.narcissus.cpanel.net","ttl":"86400","name":"car.com.","record":null,"Line":11,"class":"IN","type":"NS","line":11}]'),
      "to_dc": json.loads('[{"ttl":"86400","name":"@","data":"ns1.narcissus.cpanel.net","type":"NS"}]'),
    })
    #A Record at apex
    tests.append({
      "title": "Converting A record at apex from cPanel to DomainConnect",
      "from_cpanel": json.loads('[{"ttl":"14400","name":"car.com.","record":"10.1.34.214","Line":13,"address":"10.1.34.214","class":"IN","type":"A","line":13}]'),
      "to_dc": json.loads('[{"ttl":"14400","name":"@","data":"10.1.34.214","type":"A"}]'),
    })
    #MX Record
    tests.append({
      "title": "Converting MX record from cPanel to DomainConnect",
      "from_cpanel": json.loads('[{"ttl":"14400","name":"car.com.","preference":"0","record":null,"Line":14,"class":"IN","type":"MX","line":14,"exchange":"car.com"}]'),
      "to_dc": json.loads('[{"priority":"0","ttl":"14400","name":"@","data":"car.com","type":"MX"}]'),
    })
    #CNAME Record
    tests.append({
      "title": "Converting CNAME record from cPanel to DomainConnect",
      "from_cpanel": json.loads('[{"ttl":"14400","name":"mail.car.com.","cname":"car.com","record":"car.com","Line":15,"class":"IN","type":"CNAME","line":15}]'),
      "to_dc": json.loads('[{"ttl":"14400","name":"mail","data":"car.com","type":"CNAME"}]'),
    })
    #A Record subdomain
    tests.append({
      "title": "Converting A record subdomain from cPanel to DomainConnect",
      "from_cpanel": json.loads('[{"ttl":"14400","name":"ftp.car.com.","record":"10.1.34.214","Line":17,"address":"10.1.34.214","class":"IN","type":"A","line":17}]'),
      "to_dc": json.loads('[{"ttl":"14400","name":"ftp","data":"10.1.34.214","type":"A"}]'),
    })
    #TXT Record
    tests.append({
      "title": "Converting TXT record from cPanel to DomainConnect",
      "from_cpanel": json.loads('[{"ttl":"14400","name":"car.com.","unencoded":1,"record":"v=spf1 +a +mx +ip4:10.1.34.214 ~all","Line":18,"txtdata":"v=spf1 +a +mx +ip4:10.1.34.214 ~all","class":"IN","type":"TXT","char_str_list":["\\"v=spf1 +a +mx +ip4:10.1.34.214 ~all\\""],"line":18}]'),
      "to_dc": json.loads('[{"ttl":"14400","name":"@","data":"v=spf1 +a +mx +ip4:10.1.34.214 ~all","type":"TXT"}]'),
    })
    #A Record
    tests.append({
      "title": "Converting SRV record from cPanel to DomainConnect",
      "from_cpanel": json.loads('[{"priority":"1","ttl":"14400","name":"_sip._tcp.car.com.","port":"3","target":"forks.com","record":null,"Line":27,"weight":"2","class":"IN","type":"SRV","line":27}]'),
      "to_dc": json.loads('[{"protocol":"tcp","priority":"1","ttl":"14400","name":"@","data":"forks.com","port":"3","service":"sip","weight":"2","type":"SRV"}]'),
    })

    for test in tests:
      #JSON doesn't give us ints back, but DC libs require it
      for key in ["ttl","priority","weight","port"]:
        for to_dc in test["to_dc"]:
          if to_dc.has_key( key ):
            to_dc[key] = int(to_dc[key])
      TestZoneConvertingToDC( test["title"], "car.com", test["from_cpanel"], test["to_dc"] )

def TestZoneConvertingToDC(title, domain, from_cpanel, expected):

    returned = Domainconnect_auth.ConvertZoneToDC( domain, from_cpanel )
    passed = False

    if expected == returned:
        passed = True
    else:
        print "%s test failed. Here's what we were expecting" % ( title )
        print json.dumps( expected, sort_keys=True, indent=4, separators=( ',', ': ' ) )
        print "Here's what we got:"
        print json.dumps( returned, sort_keys=True, indent=4, separators=( ',', ': ' ) )
       
    print(title)
    if passed:
        _testResults.Pass()
    else:
        _testResults.Fail()
