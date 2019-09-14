# mostly from https://www.gwern.net/GPT-2 2.31/1.95 loss
conda env create -f environment.yml
mkdir data

git clone 'https://github.com/nshepperd/gpt-2.git'
cd gpt-2
conda activate gpt2
python download_model.py 117M
python download_model.py 345M
python download_model.py 774M

cd ../data
wget http://static.decontextualize.com/gutenberg-poetry-v001.ndjson.gz
gunzip gutenberg-poetry-v001.ndjson.gz
cat gutenberg-poetry-v001.ndjson | jq .s | sed -e 's/^.//' -e 's/.$//' -e 's/\\//g' \
    >> gutenberg-poetry-v001.txt ## delete JSON quoting
cd ..

# russian corpus
git clone https://github.com/IlyaGusev/PoetryCorpus.git
python stripru.py

# german corpus
git clone https://github.com/thomasnikolaushaider/DLK.git
python stripde.py

cat data/gutenberg-poetry-v001.txt > data/total.txt
cat data/russian.txt >> data/total.txt
cat data/deutscher.txt >> data/total.txt

shuf data/total.txt | head ## random poetry lines
du -h data/total.txt; wc data/total.txt

PYTHONPATH=src ./encode.py ../data/total.txt ../data/total.npz --model_name 774M

# 117M
conda activate gpt2
export CUDA_VISIBLE_DEVICES=1
PYTHONPATH=src ./train.py --model_name 117M --dataset ../data/total.npz \
    --run_name=poet_117M --batch_size 5 --save_every 10000 --sample_every 1000 --learning_rate=2e-5
# 2.6

PYTHONPATH=src ./train.py --model_name 117M --dataset ../data/total.npz \
    --run_name=poet_117M --batch_size 5 --save_every 10000 --sample_every 1000 --learning_rate=2e-6
# 2.55

# 345M
conda activate gpt2
export CUDA_VISIBLE_DEVICES=2
PYTHONPATH=src ./train.py --model_name 345M --dataset ../data/total.npz \
    --run_name=poet_345M --batch_size 3 --save_every 10000 --sample_every 1000 --learning_rate=2e-5
# 2.6

PYTHONPATH=src ./train.py --model_name 345M --dataset ../data/total.npz \
    --run_name=poet_345M --batch_size 3 --save_every 10000 --sample_every 1000 --learning_rate=2e-6

# 2.52

# 774M
conda activate gpt2
export CUDA_VISIBLE_DEVICES=3
PYTHONPATH=src ./train.py --model_name 774M --dataset ../data/total.npz \
    --run_name=poet2_774M --batch_size 1 --save_every 10000 --sample_every 1000 --learning_rate=2e-4 --optimizer=sgd 
# 3.2

# t.me/NeuroPoetBot

python scheduler.py
