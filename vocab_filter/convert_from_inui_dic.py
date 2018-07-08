import re

vocs = []
fp = open('orig_pn_2008.txt')
for line in fp:
  line = line.strip()
  es = re.split(r'\s{1,}', line)
  voc = es[0]
  pn = es[1]
  if pn == 'n':
    vocs.append(voc)
import json
json.dump(vocs, fp=open('vocs.json','w'), indent=2, ensure_ascii=False)
