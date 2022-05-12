#!/bin/bash
python -m wikiextractor.WikiExtractor ../enwiki-20211001-pages-articles-multistream.xml
python -m wikiextractor.WikiExtractor ../simplewiki-20210720-pages-articles-multistream.xml
outdir="../cleanish_wiki_v2/"
for dir in text/*
do
    echo $dir
    base_dir=$(basename $dir)
    if [ -d $outdir$base_dir ]; then
	echo
    else
	mkdir -p $outdir$base_dir
    fi
    for file in $dir/*
    do
	base_file=$(basename $file)
	outpath=$(echo $outdir$base_dir/$base_file)
	if [ -f $outpath ]; then
	   echo "ya esta"
	   continue
	fi
	echo $outpath
	python clean_attardis.py $file ../page-view-counts.csv $outpath
    done
done
