import json
de = json.load(open("DLK/deutscher.lyrik.korpus.v2.json", "r"))
de = [item for item in de.values()]
result = ''
for val in de:
    if val['title']:
        result += val['title'] + '\n'
    result += '\n'.join(val['lines']) + '\n'
    if val['author'] and val['year']:
        result += f"{val['author']}, {val['year']}" + '\n'
open("data/deutscher.txt","w").write(result)