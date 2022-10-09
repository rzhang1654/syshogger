import psutil
import json
import datetime
import os

def vmsnap():
  return { item : getattr(psutil.virtual_memory(),item) for item in dir(psutil._pslinux.svmem) if not item.startswith('_') and item not in [ 'count', 'index' ] }

def GetMemoryHogger(count=10):
  plist = []
  for proc in psutil.process_iter():
    try:
      ppnu = proc.as_dict(attrs=['pid', 'name', 'username'])
      ppnu['vms'] = proc.memory_info().vms / (1024 * 1024)
      plist.append(ppnu)
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
      pass
  plist = sorted(plist, key=lambda pitem: pitem['vms'], reverse=True)
  return plist[:count]

def DumpToJson(jdict,basedir="/var/tmp/memoryhoggerscan"):
  filen = os.path.join(basedir,datetime.datetime.now().strftime("vm-%Y%m%d%H%M%S"))
  with open(filen,'w') as fh:
    json.dump(jdict,fh)

if __name__ == '__main__':
   memsnapheader = ('global','process')
   jdict = dict(zip(memsnapheader,(vmsnap(),GetMemoryHogger())))
   DumpToJson(jdict)
