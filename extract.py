from urllib import request
import lxml.html
from lxml import etree
from collections import defaultdict

root = 'https://data.val.se/val/val2018/rostmottagning/vallokal/'
lund = root + 'kommun/12/81/index.html'

def get_info(url):
    r = request.urlopen(url)
    data = r.read()
    page = lxml.html.fromstring(data.decode('ascii'))
    for name in page.find_class('vallokal'):
        name = name.xpath('h2/text()')[0]
    for info in page.find_class('vallokal_info'):
        ps = []
        for p in info.xpath('p/text()'):
            ps.append(p)
        if ps[2] != '\nÖppet på valdagen 9 september 2018':
            print(ps)
        return (name, ps[1], ps[0])
        #return etree.tostring(info, pretty_print=True, encoding='unicode')
    return None


def get_districts(url):
    r = request.urlopen(url)
    data = r.read()

    page = lxml.html.fromstring(data.decode('ascii'))
    #print(data.decode('ascii').split('</tr>\n<tr'))

    urls = {}
    for vo in page.find_class('valdistrikt'):
        #print(etree.tostring(vo, pretty_print=True, encoding='unicode'))
        s, url = None, None
        for s in vo.xpath("a/text()"):
            break
        for lol in vo.xpath("a"):
            url = (lol.get('href'))
            break
        if s != None and url != None:
            urls[s] = url
            #print(s, url)

    return urls

urls = get_districts(lund)

d = defaultdict(list)
for name, url in urls.items():
    vallokal_url = root + url.replace('../../../../../rostmottagning/vallokal/', '')
    name, addr, entr = get_info(vallokal_url)
    d[name, addr].append(entr)
    print(name)
for (name, addr), entrances in sorted(d.items()):
    print(len(entrances), name, addr, ':', ', '.join(entrances))
    

