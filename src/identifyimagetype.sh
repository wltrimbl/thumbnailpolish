#!/bin/bash
# This script runs "identify" from the imagemagick suite and 
# creates a file in the current directory called "type" whose 
# contents are a symbol indicating the image-composite recipe

f=$( ls L001/C1.1/s*[aA].jpg | head -n 1)
if [[ "$( identify $f )" =~ .*608x300.* ]] 
    then 
    echo MISEQ match 
    echo MISEQ > type
elif [[ "$( identify $f )" =~ .*496x450.* ]] 
    then 
    echo HISEQ match
    echo HISEQ > type
elif [[ "$( identify $f )" =~ .*542x450.* ]] 
    then 
    echo HISEQ2 match
    echo HISEQ2 > type 
elif [[ "$( identify $f )" =~ .*576x300.* ]] 
    then 
    echo GAII match
    echo GAII > type 
fi
