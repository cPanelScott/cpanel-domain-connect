import os
import json

directory = "/usr/local/cpanel/base/3rdparty/cpanel-domain-connect/Templates"

def get_template( providerid, serviceid ):
  for filename in os.listdir(directory):
    if not filename.endswith(".json"):
      continue

    f = open( directory + "/" + filename )
    template_json = f.read()
    template = Template( template_json )
    if template.template["providerId"] == providerid and template.template["serviceId"] == serviceid:
      return template

class Template:
  def __init__(self, template_json):
    self.template = json.loads( template_json )

  def is_signed_required(self):
    if self.template.has_key("syncPubKeyDomain") and self.template["syncPubKeyDomain"]:
      return True
    else:
      return False

  def groups(self):
    return set( map( lambda x: x['groupId'], self.template["records"]) )
