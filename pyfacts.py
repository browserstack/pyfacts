import json
import os
from types import ModuleType
import sys
import urllib
import urllib2
import datetime

try:
  if os.uname()[0].lower() == 'linux':
    import linux as FactsLib
  elif os.uname()[0].lower() == 'darwin':
    import osx as FactsLib
  elif os.uname()[0].lower() == 'vmkernel':
    import esxi as FactsLib
  else:
    print "OS not supprted"
    sys.exit(0)
except:
  if os.name.lower() == "nt":
    import windows as FactsLib
  else:
    print "OS not supprted"
    sys.exit(0)

facts={}
for method in dir(FactsLib):
  if method[0] != '_' and method[0] != 'profiler_hardware_datatype' and type(getattr(FactsLib,method)) is not ModuleType:
    try:
        facts[str(method)] = getattr(FactsLib,method)()
    except:
        pass
  facts["time"] = str(datetime.datetime.utcnow())
try:
  custom_facts=open('custom_facts')
  for f in custom_facts:
    f = f.split(':')
    facts[f[0]] = f[1].strip('\n')
except:
  pass

try:
  if sys.argv[1]:
    url = sys.argv[1]
    tmp=json.dumps(facts)
    print tmp
    headers = {'Content-Type': 'application/json'}
    req = urllib2.Request(url, data=json.dumps(facts), headers=headers)
    response = urllib2.urlopen(req)
    the_page = response.read()
    print the_page
except Exception as e:
  print e
  print json.dumps(facts)
