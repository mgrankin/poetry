# poetry bot

http://t.me/NeuroPoetBot

Telegram bot that can write poetry in response to user input - English, Russian or German. Trained on instructions from here https://www.gwern.net/GPT-2 with the addition of the Russian and German poetic corpus. 

```bash
conda env create -f environment.yml
conda activate gpt2
aws s3 sync --no-sign-request s3://models.dobro.ai/tf/gpt2/poet gpt-2/checkpoint
```

1. English corpus 
https://github.com/aparrish/gutenberg-poetry-corpus

2. Russian corpus
https://github.com/IlyaGusev/PoetryCorpus

3. German corpus
https://github.com/thomasnikolaushaider/DLK
