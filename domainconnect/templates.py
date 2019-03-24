import os
import json

directory = "/usr/local/cpanel/base/3rdparty/cpanel-domain-connect/Templates"

def get_template( providerid, serviceid ):
  for filename in os.listdir(directory):
    if not filename.endswith(".json"):
      continue

    f = open( directory + "/" + filename )
    template = json.loads( f.read() )
    if template["providerId"] == providerid and template["serviceId"] == serviceid:
      return template

