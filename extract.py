from urllib import request
import lxml.html
from lxml import etree
from collections import defaultdict
import sys

kommun = {'lund' : '12/81', 'svalov' : '12/14', 'eslov':'12/85'}
root = 'https://data.val.se/val/val2018/rostmottagning/vallokal/'

if len(sys.argv) > 1 and sys.argv[1] in kommun:
    target = root + 'kommun/' + kommun[sys.argv[1]] + '/index.html'
    print(sys.argv[1])
else:
    target = root + 'kommun/12/81/index.html'
    print('lund')


open_str = '\nÖppet på valdagen 9 september 2018'

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
        if ps[2] != open_str:
            print(ps)
        return (name, '' if ps[1] == open_str else ps[1], ps[0])
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

urls = get_districts(target)

d = defaultdict(list)
for name, url in urls.items():
    vallokal_url = root + url.replace('../../../../../rostmottagning/vallokal/', '')
    name, addr, entr = get_info(vallokal_url)
    d[name, addr].append(entr)
    print(name)

print('antal valkretsar; namn på vallokal; adress; eventuell beskrivning av vilka rum')
for (name, addr), entrances in sorted(d.items()):
    print('; '.join(map(str,[len(entrances), name, addr] + entrances)))
    

