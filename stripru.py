from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring
xm = open("PoetryCorpus/datasets/corpus/all.xml").read()
ru = bf.data(fromstring(xm))['items']['item']

result = ''
for val in ru:
    if val['name']:
        result += str(val['name']['$']) + '\n'
    result += str(val['text']['$']) + '\n'
    if val['author'] and val['date_from']:
        result += f"{val['author']['$']}, {val['date_from']['$']}" + '\n'
    result += '\n'
open("data/russian.txt","w").write(result)