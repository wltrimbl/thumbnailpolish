#!/bin/bash
# This script runs "identify" from the imagemagick suite and 
# creates a file in the current directory called "type" whose 
# contents are a symbol indicating the image-composite recipe

f=$( ls L001/C1.1/s*[aA].jpg L001/C1.1/s*red.jpg | head -n 1)
if [[ "$( identify $f )" =~ .*608x300.* ]] 
    then 
    echo images in MISEQ format 
    echo MISEQ > thumbnailpolish.type
elif [[ "$( identify $f )" =~ .*496x450.* ]] 
    then 
    echo images in HISEQ format
    echo HISEQ > thumbnailpolish.type
elif [[ "$( identify $f )" =~ .*542x450.* ]] 
    then 
    echo images in HISEQ2 format
    echo HISEQ2 > thumbnailpolish.type
elif [[ "$( identify $f )" =~ .*576x300.* ]] 
    then 
    echo images in GAII format
    echo GAII > thumbnailpolish.type 
elif [[ "$( identify $f )" =~ .*700x300.* ]] 
    then 
    echo images in NEXTSEQ format
    echo NEXTSEQ > thumbnailpolish.type 
fi

if [[ -e "L001/C1.1/s_1_1112_A.jpg" ]] 
    then
    echo tree looks like HISEQ2 
    echo HISEQ2  > thumbnailpolish.tree
elif [[ -e "L001/C1.1/s_1_1101_A.jpg" ]]
    then
    echo tree looks like HISEQ 
    echo HISEQ  > thumbnailpolish.tree
elif [[ -e "L001/C1.1/s_1_99_a.jpg" ]]
    then
    echo tree looks like GAII 
    echo GAII > thumbnailpolish.tree
elif [[ -e "L001/C1.1/s_1_1_a.jpg" ]]
    then
    echo Tree looks like MISEQ1
    echo MISEQ1 > thumbnailpolish.tree
elif [[ -e "L001/C1.1/s_1_1114_a.jpg" ]]
    then
    echo Tree looks like MISEQ2
    echo MISEQ2 > thumbnailpolish.tree
elif [[ -e "L001/C1.1/s_1_11101_red.jpg" ]]
    then
    echo Tree looks like NEXTSEQ
    echo NEXTSEQ > thumbnailpolish.tree
fi

for i in {1..600}
    do
    if [[ ! -d "L001/C$i.1" ]]
        then
        break 
        fi
    done
echo Number of cycles: $i
echo $i > thumbnailpolish.numcycles


