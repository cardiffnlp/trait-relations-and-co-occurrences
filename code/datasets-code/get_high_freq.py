import pandas as pd
from collections import Counter
data = pd.read_csv("mcrae.csv")
features = data["Feature"]
goodies = []

#concepts_all = [c.split("_")[0] for c in data["Concept"]]
#data["Concept"] = concepts_all
#concept_counts = Counter(concepts_all)
#concepts = {c for c, n in concept_counts.items() if n == 1}
#data = data[data["Concept"].isin(list(concepts))]
print("blue", Counter(features)["is_blue"])

for f, c in Counter(features).items():
    if c >= 10:
        if f.startswith("a_") or f.startswith("an_"):
            continue
        goodies.append(f)
goodies.remove("clothing")

data = data[data["Feature"].isin(goodies)]    
data = data[data["BR_Label"]!="taxonomic"]
data = data[data["BR_Label"]!="encyclopaedic"]
data = data[data["BR_Label"]!="visual-motion"]
data = data[data["BR_Label"]!="function"]
data = data[data["BR_Label"]!="sound"]
data = data[data["BR_Label"]!="taste"]


material_attributes = data[data["WB_Label"]=="made_of"]
material_attributes = material_attributes[material_attributes["Feature"] != "made_of_material"]

external_component_attributes = data[data["WB_Label"]=="external_component"]
internal_component_attributes = data[data["WB_Label"]=="internal_component"] 
component_attributes = pd.concat([external_component_attributes, internal_component_attributes])
component_attributes.loc[component_attributes['Feature'] == "has_4_legs", 'Feature'] = "has_legs"
component_attributes.loc[component_attributes['Feature'] == "has_4_wheels", 'Feature'] = "has_wheels"
component_attributes = component_attributes[component_attributes['Feature'] != "has_an_inside"]
component_attributes = component_attributes.drop_duplicates(subset=["Concept","Feature"])


colour_attributes = data[data["BR_Label"]=="visual-colour"]
colour_attributes = colour_attributes[colour_attributes["Feature"]!="is_colourful"]
colour_attributes = colour_attributes[colour_attributes["Feature"]!="different_colours"]

shapes_and_sizes = data[data["WB_Label"]=="external_surface_property"]
shapes_and_sizes = shapes_and_sizes[shapes_and_sizes["BR_Label"]!="internal_componet"]
shapes_and_sizes = shapes_and_sizes[shapes_and_sizes["BR_Label"]!="external_componet"]
shapes_and_sizes = shapes_and_sizes[shapes_and_sizes["BR_Label"]!="visual-colour"]
shapes_and_sizes = shapes_and_sizes[shapes_and_sizes["Feature"]!="is_smelly"]
shapes_and_sizes = shapes_and_sizes[shapes_and_sizes["Feature"]!="is_shiny"]
shapes_and_sizes = shapes_and_sizes[shapes_and_sizes["Feature"]!="is_soft"]
shapes_and_sizes = shapes_and_sizes[shapes_and_sizes["Feature"]!="is_hard"]
shapes_and_sizes = shapes_and_sizes[shapes_and_sizes["Feature"]!="is_sharp"]
shapes_and_sizes = shapes_and_sizes[shapes_and_sizes["Feature"]!="has_a_pointed_end"]
shapes_and_sizes = shapes_and_sizes[shapes_and_sizes["Feature"]!="is_furry"]
shapes_and_sizes = shapes_and_sizes[shapes_and_sizes["Feature"]!="different_sizes"]
shapes_and_sizes = shapes_and_sizes[shapes_and_sizes["Feature"]!="is_slimy"]
shapes_and_sizes = shapes_and_sizes[shapes_and_sizes["Feature"]!="is_dirty"]


tactile_attributes = data[data["BR_Label"] == "tactile"]
tactile_attributes = tactile_attributes[tactile_attributes["Feature"] != "is_comfortable"]
tactile_attributes = tactile_attributes[tactile_attributes["Feature"] != "is_warm"]
print(len(tactile_attributes))

SNS = set(shapes_and_sizes["Feature"])
colours = set(colour_attributes["Feature"]) 
materials = set(material_attributes["Feature"])
components = set(component_attributes["Feature"])
tactiles = set(tactile_attributes["Feature"])
used = set.union(SNS, colours, materials, components, tactiles)

all_f = set(data["Feature"])
not_used = all_f.difference(used)

print(not_used)
exit()
def save_as_csv(data, filename):
    csv = data.to_csv(index=False)
    with open(filename, "w") as o:
        o.write(csv)


save_as_csv(colour_attributes, "colour-attributes.csv")
save_as_csv(material_attributes, "material-attributes.csv")
save_as_csv(component_attributes, "component-attributes.csv")
save_as_csv(shapes_and_sizes, "size-and-shape-attributes.csv")
save_as_csv(tactile_attributes, "tactile-attributes.csv")
