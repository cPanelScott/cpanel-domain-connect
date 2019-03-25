from flask import Flask
from flask import request
from flask import Response
from DomainConnectApplyZone import DomainConnect
import subprocess
import json
import re
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

def ConvertZoneToDC( domain, zone ):
    dc_zone = list()
    for x in zone:
        rr = dict()
        rr["name"] = re.sub('\.?' + re.escape( domain + '.' ), '', x["name"] ) or "@"
        if x["type"] == "A" or x["type"] == "AAAA":
            rr["type"] = x["type"]
            rr["data"] = x["address"]
            rr["ttl"] = int(x["ttl"])
            dc_zone.append( rr )
        elif x["type"] == "CNAME":
            rr["type"] = x["type"]
            rr["data"] = x["cname"]
            rr["ttl"] = int(x["ttl"])
            dc_zone.append( rr )
        elif x["type"] == "NS":
            rr["type"] = x["type"]
            rr["data"] = x["nsdname"]
            rr["ttl"] = int(x["ttl"])
            dc_zone.append( rr )
        elif x["type"] == "TXT":
            rr["type"] = x["type"]
            rr["data"] = x["txtdata"]
            rr["ttl"] = int(x["ttl"])
            dc_zone.append( rr )
        elif x["type"] == "MX":
            rr["type"] = x["type"]
            rr["data"] = x["exchange"]
            rr["ttl"] = int(x["ttl"])
            rr["priority"] = int(x["preference"])
            dc_zone.append( rr )
        elif x["type"] == "SRV":
            parts = x["name"].split(".", 2)
            if parts[0][0] != '_' or parts[1][0] != '_':
                continue

            rr["type"] = x["type"]
            rr["data"] = x["target"]
            rr["ttl"] = int(x["ttl"])
            rr["priority"] = int(x["priority"])
            rr["protocol"] = parts[1][1:]
            rr["service"] = parts[0][1:]
            rr["weight"] = int(x["weight"])
            rr["port"] = int(x["port"])
            rr["name"] = re.sub('\.?' + re.escape( domain + '.' ), '', parts[2]) or "@"
            dc_zone.append( rr )

    return dc_zone