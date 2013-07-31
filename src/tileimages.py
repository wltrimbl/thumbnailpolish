#!/usr/bin/env python
'''This script composites color thumbnails into larger images
 representing entire lanes and entire flowcells per image'''

import os, sys
from subprocess import check_output, CalledProcessError

def execute(execstring):
    print execstring
    sys.stdout.flush()
    try:
        check_output(execstring.split()) 
    except CalledProcessError, e:
        if e.returncode == 1 :
            print "Warning!  some files not found!"
        else:
            sys.exit("Freakout!")
 
def howmanycycles(somedir):
    '''Checks for the existence of directories for cycles, returns int.'''
    for n in range(1, 600):
        testdirname = somedir + "/" + "C%d.1" % n
        print testdirname 
        if not os.path.isdir(testdirname):
            n = n - 1
            break
    return n

def testhiseq(somedir):
    testmiseq = "L001/C1.1/s_1_1_a.jpg"
    testhiseq = "L001/C1.1/s_1_1101_A.jpg"
    testhisq2 = "L001/C1.1/s_1_1112_A.jpg"
    testgaII = "L001/C1.1/s_1_99_a.jpg"
    if os.path.isfile(testhisq2):
        return(2)
    elif os.path.isfile(testhiseq):
        return(1)
    elif os.path.isfile(testgaII):
        return(4)
    elif os.path.isfile(testmiseq): 
        return(3)
    else:
        return(0)

TYPE = testhiseq("") 

if TYPE == 1:  # Hiseq with 8 x 6 tiles
    print "Using HISEQ recipe"
    lane = [ '1', '2', '3', '4', '5', '6', '7', '8' ]
    iter1 = [ '11', '12', '13', '21', '22', '23' ] 
    iter2 = [ '01', '02', '03', '04', '05', '06', '07', '08' ] 
elif TYPE == 2:  # HISEQ with 16 x 6 tiles
    print "Using HISEQ2 recipe"
    lane = [ '1', '2', '3', '4', '5', '6', '7', '8' ]
    iter1 = [ '11', '12', '13', '21', '22', '23' ] 
    iter2 = [ '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16' ] 
elif TYPE == 4:   # GAII   This needs adjustment
    print "Using GAII recipe"
    lane = [ '1', '2', '3', '4', '5', '6', '7', '8' ]
    iter1 = ["1", "2", "3", "4", "5", "6", "7", "8", "9"] 
    iter2 = ["1", "2", "3", "4", "5", "6", "7", "8", "9"] 
    tiles = [ "%d" % i for i in range(0, 50)]
    tile2 = [ "%d" % i for i in range(100, 50, -1)]
elif TYPE == 3 : # MISEQ recipe
    print "Using MISEQ recipe"
    lane = [ "1" ]
    iter1 = [""] 
    iter2 = ["1", "2", "3", "4", "5", "6", "7", "8"] 
else:
    sys.exit("Can't identify format")

NUMCYCLES = howmanycycles("L001")
print "NUMCYCLES" , NUMCYCLES 

for l1 in lane:
    for j in range(1, NUMCYCLES+1):
        filelist = []
  #     create set of strips "org"
        srcdir = "L00%s/C%s.1" % (l1, j )
        destdir = "L00%s/C%s.1" % (l1, j )
        for i2 in iter2:
            filelist = []
            for i1 in iter1:
                srcdir = "L00%s/C%s.1" % (l1, j )
                filelist.append(srcdir + "/s_%s_%s%s_crop.gif" % ( l1, i1, i2) )
            tilefileg = destdir + "/org_%02d_%03d.gif" % (int(i2), j )  
            if not os.path.isfile( tilefileg ):
                if os.path.isfile(filelist[0]) :
                    execute(    "convert +append " + " ".join(filelist) + " " + tilefileg ) 
                else:
                    print "skipping creating", tilefileg, "can't find", filelist[0]
            else: 
                print "skipping creating", tilefileg, "since it already exists"
for l1 in lane:
    for j in range(1, NUMCYCLES+1):
        srcdir = "L00%s/C%s.1" % (l1, j )
        destdir = "wholeimages"
        filelist = []
        for i2 in iter2:
            tilefileg = srcdir + "/org_%02d_%03d.gif" % (int(i2), j )
            filelist.append(tilefileg) 

  #     create set of strips "orh"
        tilefileh = destdir + "/orh-%s_%03d.gif" % (l1, j)
        if os.path.isfile( tilefileh ): 
            print "skipping creation of %s since %s already exists" % ( tilefileh, tilefileh )
        elif os.path.isfile( filelist[0] ) and not TYPE :
            execute(    "convert -append " + " ".join(filelist) + " "+ tilefileh  )
        elif os.path.isfile( filelist[0]  ) and TYPE :
            execute(    "convert -append " + " ".join(filelist) + " "+ tilefileh  )
        else:
            print "can't find requisite ", filelist[0] , "needed to build ", tilefileh

#     create whole-cell images cell-
for j in range(1, NUMCYCLES+1):
    filelist = []
    for l1 in lane:
        srcdir    = "wholeimages" 
        destdir   = "wholeimages" 
        tilefileh = srcdir + "/orh-%s_%03d.gif" % (l1, j)
        filelist.append( tilefileh )
    if not os.path.isdir( destdir ) :
        os.system("mkdir " + destdir ) 
    celltarget =  destdir + "/cell-%03d.gif" % (j,)
    cellsmalltarget = destdir + "/cell-%03d.small.gif" % (j,)
    cellinsettarget = destdir + "/cell-%03d.inset.gif" % (j,)
# create whole cell images
    if not os.path.isfile( celltarget ) : 
        if os.path.isfile( filelist[0] ) : 
            execute("convert -border 2 -rotate 90 -append " + " ".join(filelist) + " " + celltarget )
        else: 
            print "skipping creating", celltarget, "because requisite", filelist[0], "not found" 
    else:
        print "skipping creating", celltarget, "because it already exists"
# create small version
    if not os.path.isfile( cellsmalltarget )  :
        if os.path.isfile( celltarget ) :
            execute( "convert -resize 25% " + "%s %s" % ( celltarget, cellsmalltarget ))
        else: 
            print "skipping creating", cellsmalltarget, "because requisite", celltarget, "not found"
    else:
        print "skipping creating", cellsmalltarget , "because it already exists"
# create inset
    if not os.path.isfile( cellinsettarget ):
        if os.path.isfile( cellsmalltarget ):
            if TYPE == 1 or TYPE == 2 :
                execute("convert %s  -page +700+200 L001/C%d.1/s_1_%s%s_crop2.gif  -mosaic %s" % (cellsmalltarget, j, iter1[0], iter2[0], cellinsettarget) )
            if TYPE == 0  or TYPE > 2 :
                execute("convert -append %s  L001/C%d.1/s_1_%s%s_crop2.gif  -mosaic %s" % (cellsmalltarget, j, iter1[0], iter2[0], cellinsettarget) )
        else:
            print "skipping creating", cellinsettarget, "because requisite", cellsmalltarget, "is missing"
    else:
        print "skipping creating", cellinsettarget, "because it already exists"

for l1 in lane:
    srcdir = "wholeimages" 
    desttdir = "wholeimages"
    bigtile =   destdir + "/tile-lane%s.big.gif" % (l1, )
    smalltile = destdir + "/tile-lane%s.small.gif" % (l1, )
    tinytile =  destdir + "/tile-lane%s.tiny.gif" % (l1, )
    filelist = []
    for j in range(1, NUMCYCLES+1):
        orhfile = srcdir + "/orh-%s_%03d.gif" % (l1, j) 
        filelist.append(orhfile)
    if not os.path.isfile( bigtile ):  
        execute("convert                  -border 2 " + " ".join(filelist) + " +append " + bigtile ) 
    else:
        print "skipping creating", bigtile , "since it already exists"
    if not os.path.isfile( smalltile ) : 
        execute("convert -resize 25%" + " -border 3 " + " ".join(filelist) + " +append " + smalltile ) 
    else:
        print "skipping creating", smalltile, "since it already exists"
    if not os.path.isfile( tinytile ) : 
        execute("convert -resize 10%" + " -border 2 " + " ".join(filelist) + " +append " + tinytile ) 
    else:
        print "skipping creating", smalltile 

largecellmovie = destdir + "/cell-lg.mp4"
smallcellmovie = destdir + "/cell-sm.mov"
insetcellmovie = destdir + "/cell-in.mp4"

if not os.path.isfile(largecellmovie):
    execute("avconv -r 5 -i " + destdir + "/cell-%03d.gif  " + largecellmovie )
else:
    print "skipping creating", largecellmovie

if not os.path.isfile(smallcellmovie):
    execute("avconv -r 5 -i " + destdir + "/cell-%03d.small.gif  " + smallcellmovie )
else:
    print "skipping creating", smallcellmovie 

if not os.path.isfile(insetcellmovie):
    execute("avconv -r 5 -i " + destdir + "/cell-%03d.inset.gif  " + insetcellmovie ) 
else:
    print "skipping creating", insetcellmovie

