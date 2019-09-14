from tendo import singleton
me = singleton.SingleInstance()

import os
os.environ["CUDA_VISIBLE_DEVICES"]="0"

import json
data = json.load(open('config.json'))

from datetime import timedelta
import json, re, random, threading
import numpy as np
import tensorflow as tf

batches_per_sample=1
BATCHES_PER_RUN = 1
batch_size=1

# weird, right?
os.chdir('gpt-2/src')
import sys
sys.path.insert(0, os.getcwd())
import model, sample, encoder
os.chdir('..')

model_name='345M'
run_name='poet_345M'
seed=None
nsamples=batch_size*batches_per_sample
temperature=0.9
top_k=0
top_p=0.9
length=400

"""
Interactively run the model
:model_name=345M : String, which model to use
:seed=None : Integer seed for random number generators, fix seed to reproduce
 results
:nsamples=1 : Number of samples to return total
:batch_size=1 : Number of batches (only affects speed/memory).  Must divide nsamples.
:length=None : Number of tokens in generated text, if None (default), is
 determined by model hyperparameters
:temperature=1 : Float value controlling randomness in boltzmann
 distribution. Lower temperature results in less random completions. As the
 temperature approaches zero, the model will become deterministic and
 repetitive. Higher temperature results in more random completions.
:top_k=40 : Integer value controlling diversity. 1 means only 1 word is
 considered for each step (token), resulting in deterministic completions,
 while 40 means 40 words are considered at each step. 0 (default) is a
 special setting meaning no restrictions. 40 generally is a good value.
:top_p=0.0 : Float value controlling diversity. Implements nucleus sampling,
 overriding top_k if set to a value > 0. A good setting is 0.9.
"""
if batch_size is None:
    batch_size = 1
assert nsamples % batch_size == 0

enc = encoder.get_encoder(model_name)
hparams = model.default_hparams()
with open(os.path.join('models', model_name, 'hparams.json')) as f:
    hparams.override_from_dict(json.load(f))

if length is None:
    length = hparams.n_ctx // 2
elif length > hparams.n_ctx:
    raise ValueError("Can't get samples longer than window size: %s" % hparams.n_ctx)

conf = tf.ConfigProto()
conf.gpu_options.per_process_gpu_memory_fraction=0.5
lock = threading.Lock()

graph=tf.Graph()
sess = tf.compat.v1.Session(graph=graph,config=conf)

with sess.as_default(), graph.as_default():
    context = tf.placeholder(tf.int32, [batch_size, None])
    np.random.seed(seed)
    tf.set_random_seed(seed)
    output = sample.sample_sequence(
        hparams=hparams, length=length,
        context=context,
        batch_size=batch_size,
        temperature=temperature, top_k=top_k, top_p=top_p
    )

    saver = tf.train.Saver()
    ckpt = tf.train.latest_checkpoint(os.path.join('checkpoint', run_name))
    print(ckpt)
    saver.restore(sess, ckpt)

def get_reply(msg_text):
    with sess.as_default(), graph.as_default():
        raw_text = msg_text[-512:]
        context_tokens = enc.encode(raw_text)
        generated = 0
        out = sess.run(output, feed_dict={
                context: [context_tokens for _ in range(batch_size)]
            })[:, len(context_tokens):]
        return enc.decode(out[0]).strip()


import telebot

bot = telebot.TeleBot(data['bot_key'])

from telebot import apihelper

apihelper.proxy = {'https':data['proxy_str']}

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, get_reply(message.text))

@bot.channel_post_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, get_reply(message.text))

bot.polling()