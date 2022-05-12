import logging, sys
import multiprocessing
from gensim.models import Word2Vec
from time import time
from nltk.tokenize import word_tokenize
import os
from gensim.test.utils import datapath
from gensim import utils

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

st = time()
data = sys.argv[1]
model_name = sys.argv[2]
cores = multiprocessing.cpu_count()

model = Word2Vec(window=10,
                 vector_size=300,
                 workers=cores-1)

t = time()
model.build_vocab(corpus_file=data, progress_per=10000)
print('Time to build vocab: {} mins'.format(round((time() - t) / 60, 2)))
t = time()
model.train(corpus_file=data,
            total_examples=model.corpus_count,
            total_words=model.corpus_total_words,
            epochs=model.epochs,
            report_delay=1)
print('Time to train the model: {} mins'.format(round((time() - t) / 60, 2)))
print('Time to build vocab: {} mins'.format(round((time() - t) / 60, 2)))
print("\n\n**************\n", model.wv.most_similar("banana"))
model.save(model_name)
print("Total time:", time()-st)
