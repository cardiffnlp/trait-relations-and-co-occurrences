from collections import Counter
import gensim
import sklearn, os
import numpy as np
import random, sys
from sklearn.model_selection import cross_val_score, cross_val_predict, StratifiedKFold
import pandas as pd
from sklearn import svm
from sklearn.metrics import f1_score
import time
from argparse import ArgumentParser
from nltk.corpus import wordnet

def get_negative_samples(vocab_set, concepts, feature_set, lang):
    negative_concepts = []
    negative_features = []
    count = 0
    vocab = tuple(vocab_set)
    vocab = sorted(vocab)
    F = tuple(feature_set)
    while len(negative_concepts) != len(concepts):
        concept = random.choice(vocab)
        count += 1
        #if count % 100 == 0:
        #    print("Tried " + str(count) + " vocab items.")
        uppers = [l for l in concept if l.isupper()]
        if len(uppers) > 0:
            continue
        synet = wordnet.synsets(concept, pos=wordnet.NOUN, lang=lang)
        if len(synet) > 0:
            negative_concepts.append(concept)
            negative_features.append(random.choice(F))
    return negative_concepts, negative_features

def get_vocab(model):
    return set([k for k in model.wv.key_to_index.keys()])

def get_concepts_and_relations(data):
    pairs = [(row["Concept"].split("_")[0], row["Feature"].split("_")[-1])
             for i, row in data.iterrows()]
    concept2feature = {c: f for c, f in pairs}
    concepts = [c for c, f in concept2feature.items() if f != "orange" and f != "naranja"]
    features = [f for c, f in concept2feature.items() if f != "orange" and f != "naranja"]
    return concepts, features

def check_missing_concepts(model, concepts):
    missing = []
    for c in concepts:
        try:
            e = model.wv[c]
        except:
            missing.append(c)
    return missing

def get_embeddings_difference(model, concepts, features):
    embeddings = []
    for c, f in zip(concepts, features):
        e = model.wv[c]
        ef = model.wv[f]
        embeddings.append(np.array(e)-np.array(ef))
    return embeddings

def numericalise_colours(colours):
    c2id = create_colour2id_dict(colours)
    num_colours = [c2id[c] for c in colours]
    return np.array(num_colours)

def create_colour2id_dict(colours):
    c_set = list(set(colours))
    c_set.sort()
    c2id = {c: i for i, c in enumerate(c_set)}
    return c2id

def create_id2colour_dict(colours):
    c_set = list(set(colours))
    c_set.sort()
    id2c = {i: c for i, c in enumerate(c_set)}
    return id2c

def remove_low_freq_features(embeddings, features):
    y_counts = Counter(features)
    goodies = []
    embeddings_new, y_new = [], []
    for y, c in y_counts.items():
        if c > 5:
            goodies.append(y)
    for e, y in zip(embeddings, features):
        if y in goodies:
            embeddings_new.append(e)
            y_new.append(y)
    return embeddings_new, y_new


argparser = ArgumentParser()
argparser.add_argument("--model_with", required=True)
argparser.add_argument("--model_without", required=True)
argparser.add_argument("--relation_csv", required=True)
argparser.add_argument("--seed", type=int, default=33)
argparser.add_argument("--lang", required=True)
args = argparser.parse_args()
if args.lang == "es":
    lang = "spa"
else:
    lang = "eng"
data = pd.read_csv(args.relation_csv)
seed=args.seed
np.random.seed(seed)
random.seed(seed)
concepts_, features_ = get_concepts_and_relations(data)
missing = []
vocab = set([])
for model_name in [args.model_without, args.model_with]:
    model = gensim.models.Word2Vec.load(model_name)
    missing += check_missing_concepts(model, concepts_)
    if len(vocab) > 0:
        vocab = vocab.intersection(get_vocab(model))
    else:
        vocab = get_vocab(model)
    del model

missing = set(missing)
concepts, features = [], []

for c, f in zip(concepts_, features_):
    if f not in vocab:
        continue
    if c not in missing:
        concepts.append(c)
        features.append(f)
negative_concepts, negative_features = get_negative_samples(vocab, concepts, set(features), lang)
del vocab

output = []
for model_name in [args.model_without, args.model_with]:
    model = gensim.models.Word2Vec.load(model_name)
    embeddings = get_embeddings_difference(model, concepts+negative_concepts, features+negative_features)
    del model 
    y = list(np.ones(int(len(embeddings)/2))) + list(np.zeros(int(len(embeddings)/2)))
    clf = svm.SVC(kernel='linear', C=1, class_weight="balanced", random_state=seed)
    cv = StratifiedKFold(3, random_state=seed, shuffle=True)
    scores_micro = cross_val_score(clf, embeddings, y, cv=cv, scoring="f1_micro")
    #print("SVM micro", format(np.mean(scores_micro), ".3f"), "pm", format(np.std(scores_micro), ".3f"))
    micro = str(np.mean(scores_micro))
    micro_std = str(np.std(scores_micro))
    output.append(",".join([str(len(embeddings)),str(len(set(features))),str(micro),str(micro_std)]))
print(":".join(output))
