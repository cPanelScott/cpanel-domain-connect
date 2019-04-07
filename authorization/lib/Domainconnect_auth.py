from flask import Flask
from flask import request
from flask import Response
from DomainConnectApplyZone import DomainConnect
import subprocess
import json
import re
import sys
app = Flask(__name__)

@app.route("/v2/domainTemplates/providers/<string:providerid>/services/<string:serviceid>/apply")
def apply( providerid, serviceid ):
    confirm = request.args.get("confirm")
    dc = DomainConnect( providerid, serviceid )
    #TODO catch the error

    #Validation (how much of this can be handled by dc?

    domain = request.args.get('domain')
    if not domain:
        return "URL is missing required parameters. Please notify Service Provider"
    if not fetchzone_records( domain ):
        #TODO sanitize the domain SECURITY
        return "The domain %s is not on this cPanel account. Please go back to the Service Provider and try again with a different cPanel account" % ( domain )

    host = request.args.get('host') #TODO can this be empty? Currently causing an exception in Apply when it is.
    redirect_uri = request.args.get("redirect_uri")
    state = request.args.get("state")
    providername = request.args.get("providerName")
    groupid = request.args.get("groupId")
    sig = request.args.get("sig")

    if dc.IsSignatureRequired():
        #TODO do
        return "Error: Template requires signature, and this is unimplemented\n"

    if not confirm:
        location_offset = get_index( request.url, '/', 3 )
        confirm_url = (request.url[:location_offset] + ":2083" + request.url[location_offset:]).replace("/.dispatch.py", "") + "&confirm=1"
        return "Are you sure? If so, please go to: %s" % ( confirm_url )
    else:
    #def Apply(self, zone_records, domain, host, params, groupId=None, qs=None, sig=None, key=None):
        records = ConvertcPRecordsToDC( domain, fetchzone_records( domain ) )
        try:
            new = dc.Apply( records, domain, host, list(), groupid )
        #except MissingParameter: Not defind
        #    return "Missing a parameter"
        return "I see the following records\n" + json.dumps( new, sort_keys=True, indent=4, separators=(',', ': ') )

def get_index(input_string, sub_string, ordinal):
    current = -1
    for i in range(ordinal):
        current = input_string.index(sub_string, current + 1)
    return current

def fetchzone_records( domain ):
    zone_json = subprocess.check_output(["cpapi2", "--output=json", "ZoneEdit", "fetchzone_records", "domain=%s" % ( domain )])
    zone = json.loads( zone_json )
    return zone["cpanelresult"]["data"]

def ConvertcPRecordsToDC( domain, cPrecords ):
    dc_zone = list()
    for x in cPrecords:
        rr = dict()
        try:
            rr["name"] = re.sub('\.?' + re.escape( domain + '.' ), '', x["name"] ) or "@"
        except KeyError:
            continue

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
            parts = rr["name"].split(".", 2)
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
            rr["name"] = parts[2] if len(parts) == 3 else "@"
            dc_zone.append( rr )

    return dc_zone
