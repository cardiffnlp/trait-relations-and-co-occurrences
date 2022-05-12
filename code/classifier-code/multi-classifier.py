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

def get_concepts_and_relations(data):
    pairs = [(row["Concept"].split("_")[0], row["Feature"].split("_")[-1])
             for i, row in data.iterrows()]
    concept2feature = {c: f for c, f in pairs}
    concepts = [c for c, f in concept2feature.items()]# if c != "orange" and c != "naranja"]
    features = [f for c, f in concept2feature.items()]# if f != "orange" and f != "naranja"]
    return concepts, features

def check_missing_concepts(model, concepts):
    missing = []
    for c in concepts:
        try:
            e = model.wv[c]
        except:
            missing.append(c)
    return missing

def get_concept_embeddings(model, concepts):
    embeddings = []
    for c in concepts:
        e = model.wv[c]
        embeddings.append(np.array(e))
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
args = argparser.parse_args()

data = pd.read_csv(args.relation_csv)
seed=args.seed
np.random.seed(seed)
random.seed(seed)
concepts_, features_ = get_concepts_and_relations(data)
missing = []
for model_name in [args.model_without, args.model_with]:
    model = gensim.models.Word2Vec.load(model_name)
    missing += check_missing_concepts(model, concepts_)
    del model 
missing = set(missing)
concepts, features = [], []

for c, f in zip(concepts_, features_):
    if c not in missing:
        concepts.append(c)
        features.append(f)
output = []
for model_name in [args.model_without, args.model_with]:
    model = gensim.models.Word2Vec.load(model_name)
    embeddings = get_concept_embeddings(model, concepts)
    del model 
    y = numericalise_colours(features)
    id2colour = create_id2colour_dict(features)
    n_concepts = str(len(embeddings))
    clf = svm.SVC(kernel='linear', C=1, class_weight="balanced", random_state=seed)
    cv = StratifiedKFold(3, random_state=seed, shuffle=True)

    scores_micro = cross_val_score(clf, embeddings, y, cv=cv, scoring="f1_micro")

    #print("SVM micro", format(np.mean(scores_micro), ".3f"), "pm", format(np.std(scores_micro), ".3f"))
    micro = str(np.mean(scores_micro))
    micro_std = str(np.std(scores_micro))
    output.append(",".join([str(len(embeddings)),str(len(set(features))),str(micro),str(micro_std)]))
print(":".join(output))
