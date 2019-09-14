from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring
xm = open("PoetryCorpus/datasets/corpus/all.xml").read()
ru = bf.data(fromstring(xm))['items']['item']

result = ''
for val in ru:
    if val['author']:
        result += val['author']['$'] + '\n'
    if val['name']:
        result += str(val['name']['$']) + '\n'
    result += str(val['text']['$']) + '\n'
    result += '\n'
open("data/russian.txt","w").write(result)