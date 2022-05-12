import sys

goodies = set([])#counts = {}
outfile = sys.argv[3]
with open(sys.argv[2], "r") as f:
    for line in f:#
        if line == "title,count\n":
            continue
        items = line.split("\t")
        title = items[0]
        count = int(items[1])
        if count >= 10:
            goodies.add(title.lower())

with open(sys.argv[1], "r") as f:
    with open(outfile, "w") as o:
        for line in f:
            if line.startswith("<doc id="):
                title = line.split('title="')[-1][:-3]
                lookup = "_".join(title.split()).lower()
                continue
            if line.startswith("</doc>"):
                continue
            if line.strip() == title:
                continue
            if lookup not in goodies:
                continue
            o.write(line)
