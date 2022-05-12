import pandas as pd
import sys
from collections import Counter
datafile = sys.argv[1]
data = pd.read_csv(datafile)
concepts_all = [c.split("_")[0] for c in data["Concept"]]
data["Concept"] = concepts_all
print(len(set(concepts_all)))
concept_counts = Counter(concepts_all)
concepts = {c for c, n in concept_counts.items() if n == 1}
print(len(concepts_all), len(concepts))
#print(list(concepts_all))

#for i, row in data.iterrows():
#    if row["Concept"] in concepts:
#        print(i, row["Concept"])


#print(data)

data = data[data["Concept"].isin(list(concepts))]
goodies = []
features = data["Feature"]
print(set(features))
for f, c in Counter(features).items():
    if c >= 10:
        goodies.append(f)
print(goodies)
data = data[data["Feature"].isin(goodies)]
print(len(data))


def save_as_csv(data, filename):
    csv = data.to_csv(index=False)
    with open(filename, "w") as o:
        o.write(csv)


save_as_csv(data, "single-label-attributive-data/"+datafile)
