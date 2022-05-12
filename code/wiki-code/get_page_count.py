import sys, pandas, os
outfile = "page-view-counts.csv"
c = 0
directory = sys.argv[1]
counts = {}
for filename in os.listdir(directory):
    if filename.endswith("gz") or filename.endswith(".sh"):
        continue
    print(filename)
    filepath = directory + os.sep + filename
    with open(filepath, "r") as f:
        for line in f:
            items = line.split()
            title = items[1]
            try:
                count = int(items[2])
            except:
                print(line)
                continue                
            if title in counts.keys():
                counts[title] += count
            else:
                counts[title] = count
      
with open(outfile, "w") as o:
    o.write("title,count\n")
    for k, c in counts.items():
        o.write(k+"\t"+str(c))
        o.write("\n")
