import pandas as pd
import stanza
from nltk.stem import WordNetLemmatizer
from argparse import ArgumentParser
import os
from nltk.tokenize import word_tokenize
import random

PROBLEM_LEMMAS = {"catapultar": "catapulta",
                  "lanzar": "lanza",
                  "cuchara": "cucha",
                  "armónico": "armónica",
                  "azado": "azada",
                  "orejerar": "orejera",
                  "pas": "pasar"}

def get_pairs(data):
    pairs = [(lemmatizer(row["Concept"].split("_")[0]).sentences[0].words[0].lemma,
                  lemmatizer(str(row["Feature"]).split("_")[-1]).sentences[0].words[0].lemma)
                 for i, row in data.iterrows()]
    concept2features = {}
    for c, f in pairs:
        if c in PROBLEM_LEMMAS.keys():
            c = PROBLEM_LEMMAS[c]
        concept2features[c] = []
    for c, f in pairs:
        if c in PROBLEM_LEMMAS.keys():
            c = PROBLEM_LEMMAS[c]
        concept2features[c].append(f)
    return concept2features

def contains_co_occurrence(lemmas):
    concepts_seen = set(concept2features.keys()).intersection(set(lemmas))
    if len(concepts_seen) > 0:
        pairs_ = [(c, f) for c in concepts_seen for f in concept2features[c]]
        
        for concept, feature in pairs_:
            concept_inds = get_indices(lemmas, concept)
            windows = [get_window(i, lemmas) for i in concept_inds]
            for window in windows:
                if feature in window:
                    return True
    return False

def get_indices(array, element):
    return [i for i, e in enumerate(array) if e == element]

def get_window(i, lemmas):
    lower_bound = max(0, i-10)
    upper_bound = min(len(lemmas), i+10)
    return lemmas[lower_bound:upper_bound+1]


def get_replacements(reserve_sentences, k):
    random.shuffle(reserve_sentences)
    replacements = []
    for instance in reserve_sentences:
        sentence_lemmas = instance.split("|/||\|")
        sentence = sentence_lemmas[0]
        lemmas = [l.lower() for l in sentence_lemmas[1].split()]
        if contains_co_occurrence(lemmas):
            continue
        else:
            replacements.append(sentence)
        if len(replacements) == k:
            break
    return replacements

def process_file(FILE, filename, reserve_sentences):
    count = 1
    sentences_without = []
    sentences_with = []
    for line in FILE:
        if line == "\n":
            continue
        if count % 20000 == 0:
            print("Processed ", count, " lines.")
        sentence_lemmas = line.strip().split("|/||\|")
        sentence = sentence_lemmas[0]
        lemmas = [l.lower() for l in sentence_lemmas[1].split()]
        if contains_co_occurrence(lemmas):
            sentences_with.append(sentence)
        else:
            sentences_without.append(sentence)    
        count += 1

    print(len(sentences_with), len(sentences_without))
    sentences_with_all = sentences_with + sentences_without
    random.shuffle(sentences_with_all)
    sentences_without += get_replacements(reserve_sentences, k=len(sentences_with))
    random.shuffle(sentences_without)
    print(len(sentences_with_all), len(sentences_without))
    return sentences_with_all, sentences_without, sentences_with

def read_reserve_file(filepath):
    sentences = []
    with open(filepath, "r") as f:
        for line in f:
            if line != "\n":
                sentences.append(line)
    return sentences

def save(sentences, outpath):
    with open(outpath, "w") as o:
        for s in sentences:
            o.write(s)
            o.write("\n")

def append(sentences, outpath):
    with open(outpath, "a") as o:
        for s in sentences:
            o.write(s)
            o.write("\n")
            
if __name__ == "__main__":
    os.environ['CUDA_VISIBLE_DEVICES'] = "-1"
    argument_parser = ArgumentParser()
    argument_parser.add_argument("--data_dir", required=True)
    argument_parser.add_argument("--out_dir_top", required=True)
    argument_parser.add_argument("--relation_csv", required=True)
    argument_parser.add_argument("--lang", required=True)
    
    args = argument_parser.parse_args()
    attribute_type = args.relation_csv.split(".")[0].split("/")[-1]
    print(attribute_type)
    out_dir = args.out_dir_top + os.sep + attribute_type
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    #################################################
    ### change for LANG to be argument #####################
    lemmatizer = stanza.Pipeline(lang=args.lang,
                                     processors="tokenize,mwt,pos,lemma")
    #################################################
    #################################################
    data = pd.read_csv(args.relation_csv)
    concept2features = get_pairs(data)
    count = 0
    main_data_dir = args.data_dir + os.sep + "main"
    reserves_data_dir = args.data_dir + os.sep + "reserve"
    collocations_outpath = out_dir + os.sep + "collocation-sentences.txt"
    with open(collocations_outpath, "w") as o:
        pass
    for filename in os.listdir(main_data_dir):
        if not filename.endswith("txt"):
            continue
        filepath = main_data_dir + os.sep + filename
        reserve_filepath = reserves_data_dir + os.sep + filename
        without_outdir =out_dir + os.sep + "without/" 
        without_outpath = without_outdir + filename
        if not os.path.exists(without_outdir):
            os.makedirs(without_outdir)
        with_outdir = out_dir + os.sep + "with/" 
        with_outpath = with_outdir + filename
        if not os.path.exists(with_outdir):
            os.makedirs(with_outdir)
        print(filename)
        reserve_sentences = read_reserve_file(reserve_filepath)
        with open(filepath, "r") as f:
            with_co, without, collocations = process_file(f, filename, reserve_sentences)
            save(with_co, with_outpath)
            save(without, without_outpath)
            append(collocations, collocations_outpath)
            count += 1
        print("**********\nProcessed", count, " files.\n************")

