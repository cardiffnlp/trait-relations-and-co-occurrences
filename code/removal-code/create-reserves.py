from argparse import ArgumentParser
import os
import random

def process_file(FILE, filename):
    count = 1
    sentences = []
    for line in FILE:
        if line == "\n":
            continue
        if count % 10000 == 0:
            print("Processed ", count, " lines.")
        sentence = line.strip()
        sentences.append(sentence)
        count += 1
    reserve_count = round(len(sentences)*0.2)
    random.shuffle(sentences)
    reserves = sentences[:reserve_count]
    main = sentences[reserve_count:]
    print(len(sentences), len(main), len(reserves))
    return main, reserves
   
    

def save(sentences, outpath):
    with open(outpath, "w") as o:
        for s in sentences:
            o.write(s)
            o.write("\n")
                                 
if __name__ == "__main__":
    argument_parser = ArgumentParser()
    argument_parser.add_argument("--data_dir", required=True)
    argument_parser.add_argument("--out_dir", required=True)
        
    args = argument_parser.parse_args()
    count = 0
    for filename in os.listdir(args.data_dir):
        if not filename.endswith("txt"):
            continue
        filepath = args.data_dir + os.sep + filename
        main_outpath = args.out_dir + os.sep + "main/" + filename
        reserves_outpath = args.out_dir + os.sep + "reserve/" + filename
        with open(filepath, "r") as f:
            print(filename)
            main, reserves = process_file(f, filename)
            save(main, main_outpath)
            save(reserves, reserves_outpath)
        count += 1
        print("**********\nProcessed", count, " files.\n************")
        
