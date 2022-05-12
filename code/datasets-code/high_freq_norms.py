import pandas as pd
from collections import Counter
data = pd.read_csv("norms.csv")#[0:1000]
features = data["feature"]
goodies = []

for f, c in Counter(features).items():
    if c >= 10:
        goodies.append(f)
print(len(set(goodies)))


data = data[data["feature"].isin(goodies)]
print(data)
all_f = set(goodies)
feature2attribute_type = {}
for f in all_f:
    x = input(f)
    if x == "m":
        att_type ="material"
    elif x == "c":
        att_type ="color"
    elif x == "s":
        att_type ="shape_and_size"
    elif x == "t":
        att_type ="tactile"
    elif x == "p":
        att_type ="component"
    else:
        att_type ="VOID"
    feature2attribute_type[f] = att_type
    if x == "N":
        break

attribute_types = []
for i, row in data.iterrows():
    attribute_types.append(feature2attribute_type[row["feature"]])
    
data["attribute type"] = attribute_types

def save_as_csv(data, filename):
    csv = data.to_csv(index=False)
    with open(filename, "w") as o:
        o.write(csv)

save_as_csv(data, "norms-with-attr-type.csv")
'''
data = pd.read_csv("norms-with-attr-type.csv")

goodies = []

#for f, c in Counter(features).items():
  #  if c == 1:
    #    goodies.append(f)
#print(len(set(goodies)))



data = data[data["attribute type"] != "VOID"]
data = data[~data.concept.str.contains("_")]
concepts_auld = set([])
for attr_type in set(data["attribute type"]):
    print("\n------------------------------------")
    print(attr_type,"\n------------------------------------")
    new_data = data[data["attribute type"]==attr_type]
    features = new_data["concept"]
    goodies = []
    for f, c in Counter(features).items():
        if c == 1:
            goodies.append(f)
    new_data = new_data[new_data["concept"].isin(goodies)]            
    print("concepts:", len(set(new_data["concept"])))
    print("features:", len(set(new_data["feature"])))
    #print(len(new_data))
    try:
        att_suffix = "-".join(attr_type.split("_"))
        other_filepath = "mcrae-SL/"+att_suffix + "-attributes.csv"
        other=pd.read_csv(other_filepath)
        
    except:
        other = []
    print("auld", len(set(other["Concept"])))
    print("diff", len(set(other["Concept"]).difference(set(new_data["concept"]))))
    print(list(other["Concept"][:15]))
    print(list(new_data["concept"]))
    concepts_auld.update(list(other["Concept"]))

print("\n--------------------------------------------\n-------------------------------------------------------")
print("auld concept count: ", len(concepts_auld))
print("newy concept count: ", len(set(data["concept"])))
print("difference count:   ", len(set(data["concept"]).difference(concepts_auld)))
'''
