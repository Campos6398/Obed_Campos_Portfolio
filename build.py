from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import shutil
root=Path(__file__).parent
class Check(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.links=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  for key in ['href','src']:
   if key in a:self.links.append(a[key])
c=Check();c.feed((root/'index.html').read_text());assert len(c.ids)==len(set(c.ids)), 'Duplicate IDs'
for link in c.links:
 u=urlsplit(link)
 if u.scheme or u.netloc:continue
 if u.path:assert (root/unquote(u.path)).is_file(),link
 elif u.fragment:assert u.fragment in c.ids,link
out=root/'dist'
if out.exists():shutil.rmtree(out)
out.mkdir()
for name in ['index.html','styles.css','script.js','assets','inventories','project-file-inventory.csv','image-sources.json','file-name-mapping.csv']:
 p=root/name
 if p.is_dir():shutil.copytree(p,out/name)
 else:shutil.copy2(p,out/name)
print('Validated local assets, links, anchor targets and unique IDs; static output ready.')
