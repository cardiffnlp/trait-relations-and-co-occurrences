import spacy, time, sys, os
from spacy.tokenizer import Tokenizer

def save_sentence(sentence, outpath):
    text = sentence.text
    with open(outpath, "a") as o:
        if text != "" and text !="\n":
            lemmas = [token.lemma_.strip() for token in sentence]
            output = text.strip() + "|/||\|" + " ".join(lemmas)
            o.write(output)
            o.write("\n")
            
with open("test.txt", "w") as o:
    pass


directory = sys.argv[1]
outdir = sys.argv[2]
lang = sys.argv[3]


if lang == "en":
    nlp = spacy.load("en_core_web_sm")
elif lang == "es":
    nlp = spacy.load("es_core_news_sm")
else:
    exit("lang should be 'en' or 'es'")
    
file_count = 0
count = 0
for filename in os.listdir(directory):
    if not filename.endswith(".txt"):
        continue
    st = time.time()
    filepath = directory + os.sep + filename
    outpath = outdir + os.sep + filename
    print(filename)
    with open(outpath, "w") as o:
        pass
    with open(filepath, "r") as f:
        texts = [l for l in f.readlines() if l != "\n"]
    docs = nlp.pipe(texts, n_process=1)
    for e, doc in enumerate(docs):
        if e > 0 and e % 1000== 0:
            print("Processed " + str(e) + " paragraphs.")
        for sentence in doc.sents:
            save_sentence(sentence, outpath)
            count += 1
    
    print(format(count/(time.time() - st), ".2f") + " sentences/s")

    file_count += 1
    print("\n**********************\n Processed "+str(file_count) + " files.\n**********************\n")
print(format(count, ".2e") + " sentences.")
