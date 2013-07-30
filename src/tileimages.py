#!/usr/bin/env python
'''This script composites color thumbnails into larger images
 representing entire lanes and entire flowcells per image'''

import os, sys
from subprocess import check_call, CalledProcessError

def execute(execstring):
    print execstring
    try:
        check_call(execstring.split())
    except CalledProcessError:
        sys.exit("Freakout!")

def howmanycycles(somedir):
    '''Checks for the existence of directories for cycles, returns int.'''
    for i in range(1, 600):
        testdirname = somedir + "/" + "C%d.1" % i
        print testdirname 
        if not os.path.isdir(testdirname):
            i = i - 1
            break
    return i

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
        destdir = "L00%s/C%d.1" % (l1, j )
        for i2 in iter2:
            filelist = []
            for i1 in iter1:
                targetdir = "L00%s/C%d.1" % (l1, j )
                filelist.append(targetdir + "/s_%s_%s%s_crop.gif" % ( l1, i1, i2) )
            tilefileg = targetdir + "/org_%02d_%03d.gif" % (int(i2), j )  
            if not os.path.isfile( tilefileg ):
                if os.path.isfile(filelist[0]) :
                    execute(    "convert +append " + " ".join(filelist) + " " + tilefileg ) 
                else:
                    print "skipping creating", tilefileg, "can't find", filelist[0]
            else: 
                print "skipping creating", tilefileg, "since it already exists"
  #     create set of strips "orh"
        tilefileh = destdir + "/orh_%03d.gif" % ( j,)
        if os.path.isfile( tilefileh ): 
            print "skipping convert -append org_??_%03d.gif %s since %s already exists" % ( j, tilefileh, tilefileh )
        elif os.path.isfile( destdir + "/org_%02d_%03d.gif" % (int(i2), j) ) and not TYPE :
            execute(    "convert -append " + destdir + "/org_??_%03d.gif %s" % ( j, tilefileh ))
        elif os.path.isfile( destdir + "/org_%02d_%03d.gif" % (int(i2), j) ) and TYPE :
            execute(    "convert -append " + destdir + "/org_??_%03d.gif %s" % ( j, tilefileh ))
        else:
            print "can't find requisite ", destdir+"/org_%02d_%03d.gif" % (int(i2), j ) , "needed to build ", tilefileh

#     create set of strips "orh"
for j in range(1, NUMCYCLES+1):
    filelist = []
    for l1 in lane:
        targetdir = "L00%s/C%d.1" % (l1, j )
        wholedir   = "wholeimages" 
        tilefileh = targetdir + "/orh_%03d.gif" % ( j,)
        filelist.append( tilefileh )
    if not os.path.isdir( wholedir ) :
        os.system("mkdir " + wholedir ) 
    celltarget =  wholedir + "/cell-%03d.gif" % (j,)
    cellsmalltarget = wholedir + "/cell-%03d.small.gif" % (j,)
    cellinsettarget = wholedir + "/cell-%03d.inset.gif" % (j,)
    if not os.path.isfile( celltarget ) and os.path.isfile( filelist[0] ) : 
        execute("convert -border 2 -rotate 90 -append " + " ".join(filelist) + " " + celltarget )
    else:
        print "skipping creating", celltarget

    if not os.path.isfile( cellsmalltarget )  and os.path.isfile( celltarget ) :
        execute( "convert -resize 25% " + "%s %s" % ( celltarget, cellsmalltarget ))
    else:
        print "skipping creating", cellsmalltarget 
    if not os.path.isfile( cellinsettarget ) and os.path.isfile( cellsmalltarget ):
        if TYPE == 1 or TYPE == 2 :
            execute("convert %s  -page +700+200 L001/C%d.1/s_1_%s%s_crop2.gif  -mosaic %s" % (cellsmalltarget, j, iter1[0], iter2[0], cellinsettarget) )
        if TYPE == 0 :
            execute("convert -append %s  L001/C%d.1/s_1_%s%s_crop2.gif  -mosaic %s" % (cellsmalltarget, j, iter1[0], iter2[0], cellinsettarget) )
    else:
        print "skipping creating", cellinsettarget 

for l1 in lane:
    targetdir = "L00%s/colorimages" % (l1, )
    bigtile =  "L00%s/colorimages/bigtile.gif" % (l1, )
    smalltile =  "L00%s/colorimages/smalltile.gif" % (l1, )
    tinytile =  "L00%s/colorimages/tinytile.gif" % (l1, )
    if not os.path.isfile( bigtile ) and os.path.isfile( targetdir + "/orh_001.gif") :
        execute("convert %s/orh_???.gif -border 2 +append %s" % (targetdir, bigtile) ) 
    else:
        print "skipping creating", bigtile 
    if not os.path.isfile( smalltile ) and os.path.isfile( targetdir + "/orh_001.gif") :
        execute("convert -resize 25%" + " -border 3 %s/orh_???.gif +append %s" % ( targetdir, smalltile ) ) 
    else:
        print "skipping creating", smalltile
    if not os.path.isfile( tinytile ) and os.path.isfile( smalltile ) :
        execute("convert -resize 10%" + " -border 2 %s/orh_???.gif +append %s" % ( targetdir, tinytile ) ) 
    else:
        print "skipping creating", smalltile 

largecellmovie = wholedir + "/cell-lg.mp4"
smallcellmovie = wholedir + "/cell-sm.mov"
insetcellmovie = wholedir + "/cell-in.mp4"

if not os.path.isfile(largecellmovie):
    execute("avconv -r 5 -i " + wholedir + "/cell-%03d.gif  " + largecellmovie )
else:
    print "skipping creating", largecellmovie

if not os.path.isfile(smallcellmovie):
    execute("avconv -r 5 -i " + wholedir + "/cell-%03d.small.gif  " + smallcellmovie )
else:
    print "skipping creating", smallcellmovie 

if not os.path.isfile(insetcellmovie):
    execute("avconv -r 5 -i " + wholedir + "/cell-%03d.inset.gif  " + insetcellmovie ) 
else:
    print "skipping creating", insetcellmovie

#print "Not actually running these"
#print "convert -rotate 90 orh_???.gif  +append  GIANTILE.gif "
