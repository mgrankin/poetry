import re

text = re.sub('<[^<]+>', "\n", open("PoetryCorpus/datasets/corpus/all.xml").read())
with open("data/russian.txt", "w") as f:
    f.write(text)