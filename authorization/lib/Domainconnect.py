from flask import Flask
from flask import request
from flask import Response
from DomainConnectApplyZone import DomainConnect
import subprocess
import json
app = Flask(__name__)

@app.route("/v2/domainTemplates/providers/<string:providerid>/services/<string:serviceid>/apply")
def apply( providerid, serviceid ):
    confirm = request.args.get("confirm")
    if not confirm:
        dc = DomainConnect( providerid, serviceid )
        #TODO catch the error

        domain = request.args.get('domain')
        if not domain:
            return "URL is missing required parameters. Please notify Service Provider"

        host = request.args.get('host')
        redirect_uri = request.args.get("redirect_uri")
        state = request.args.get("state")
        providername = request.args.get("providerName")
        groupid = request.args.get("groupId")
        sig = request.args.get("sig")

        if dc.is_signed_required():
            #TODO do
            return "Error: Template requires signature, and this is unimplemented\n"

        location_offset = get_index( request.url, '/', 3 )
        confirm_url = (request.url[:location_offset] + ":2083" + request.url[location_offset:]).replace(".dispatch.py", "") + "&confirm=1"
        return "Are you sure? If so, please go to: %s" % ( confirm_url )
    else:
    #def Apply(self, zone_records, domain, host, params, groupId=None, qs=None, sig=None, key=None):
        return "Now I'm ready to rumble\n"

def get_index(input_string, sub_string, ordinal):
    current = -1
    for i in range(ordinal):
        current = input_string.index(sub_string, current + 1)
    return current

def fetchzone_records( domain ):
    zone_json = subprocess.check_output(["cpapi2", "--output=json", "ZoneEdit", "fetchzone_records", "domain=%s" % ( domain )])
    zone = json.loads( zone_json )
    return zone["cpanelresult"]["data"]

'''
This are all examples of entries you'll find in the zone['cpanelresult']['data'] array
         {
            "ttl" : "86400",
            "Line" : 4,
            "class" : "IN",
            "record" : null,
            "minimum" : "86400",
            "line" : 4,
            "mname" : "ns1.cpanel.ninja",
            "Lines" : 6,
            "retry" : "1800",
            "name" : "dctest.com.",
            "expire" : "1209600",
            "type" : "SOA",
            "refresh" : "3600",
            "serial" : "2019032403",
            "rname" : "root.dc.cpanel.ninja"
         },
         {
            "type" : "NS",
            "name" : "dctest.com.",
            "line" : 11,
            "record" : null,
            "nsdname" : "ns1.cpanel.ninja",
            "class" : "IN",
            "ttl" : "86400",
            "Line" : 11
         },
         {
            "ttl" : "14400",
            "Line" : 15,
            "class" : "IN",
            "address" : "3.92.156.200",
            "name" : "dctest.com.",
            "type" : "A",
            "record" : "3.92.156.200",
            "line" : 15
         },
         {
            "exchange" : "dctest.com",
            "Line" : 17,
            "ttl" : "14400",
            "class" : "IN",
            "preference" : "0",
            "name" : "dctest.com.",
            "type" : "MX",
            "record" : null,
            "line" : 17
         },
         {
            "ttl" : "14400",
            "Line" : 19,
            "class" : "IN",
            "cname" : "dctest.com",
            "name" : "mail.dctest.com.",
            "type" : "CNAME",
            "record" : "dctest.com",
            "line" : 19
         },
         {
            "type" : "TXT",
            "name" : "dctest.com.",
            "char_str_list" : [
               "\"v=spf1 +a +mx +ip4:3.92.156.200 ~all\""
            ],
            "txtdata" : "v=spf1 +a +mx +ip4:3.92.156.200 ~all",
            "line" : 22,
            "record" : "v=spf1 +a +mx +ip4:3.92.156.200 ~all",
            "unencoded" : 1,
            "class" : "IN",
            "Line" : 22,
            "ttl" : "14400"
         },


'''
