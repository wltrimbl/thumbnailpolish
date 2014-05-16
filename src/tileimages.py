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
    try:
        a = int(open("thumbnailpolish.numcycles").read().strip())
        return(a)
    except IOError:
        sys.exit("Can't find config file thumbnailimages.numcycles.") 

def testhiseq(somedir):
    try:
        a = open("thumbnailpolish.tree").read().strip() 
        return(a)
    except IOError:
        sys.exit("Can't find config file thumbnailimages.type") 

TYPE = testhiseq("") 

if TYPE == "HISEQ":  # Hiseq with 8 x 6 tiles
    print "Using HISEQ recipe"
    lane = [ '1', '2', '3', '4', '5', '6', '7', '8' ]
    iter1 = [ '11', '12', '13', '21', '22', '23' ] 
    iter2 = [ '01', '02', '03', '04', '05', '06', '07', '08' ] 
elif TYPE == "HISEQ2":  # HISEQ with 16 x 6 tiles
    print "Using HISEQ2 recipe"
    lane = [ '1', '2', '3', '4', '5', '6', '7', '8' ]
    iter1 = [ '11', '12', '13', '21', '22', '23' ] 
    iter2 = [ '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16' ] 
elif TYPE == "GAII":   # GAII  doesn't count the same way
    print "Using GAII recipe"
    lane = [ '1', '2', '3', '4', '5', '6', '7', '8' ]
    tiles = [ "%d" % i for i in range(1, 51)]
    tiles = [ "%d" % i for i in range(50, 0, -1)]
    tile2 = [ "%d" % i for i in range(100, 50, -1)]
    tile2 = [ "%d" % i for i in range(51, 101)]
    iter1 = [""] 
    iter2 =  [ "%d" % i for i in range(1, 51)]    # we use iter2 to name the intermediates
    gaiitiles = zip(tiles, tile2)
elif TYPE == "MISEQ1" : # MISEQ recipe
    print "Using MISEQ1 recipe"
    lane = [ "1" ]
    iter1 = [""] 
    iter2 = ["1", "2", "3", "4", "5", "6", "7", "8"] 
elif TYPE == "MISEQ2" : # MISEQ2 recipe
    print "Using MISEQ2 recipe"
    lane = [ "1" ]
    iter1 = [ '11', '21']
    iter2 = [ '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14'] 
elif TYPE == "NEXTSEQ" : # NEXTSEQ
    print "Using NEXTSEQ recipe"
    lane = [ "1", "2", "3", "4" ]
    lane = [ "1" ]
    iter1 = [ '11', '12', '13', '21', '22', '23']
    iter2 = [ '101', '106', '112', '201', '206', '212', '301', '306', '312'] # A
    iter2 = [ '101', '201', '301', '106', '206', '306', '112', '212', '312'] # B

else:
    sys.exit("Can't identify format")

NUMCYCLES = howmanycycles("L001")
print "NUMCYCLES" , NUMCYCLES 
CYCLES = range(1, NUMCYCLES+1)
for l1 in lane:
    for j in CYCLES:
        filelist = []
  #     create set of strips "org"
        srcdir = "L00%s/C%s.1" % (l1, j )
        destdir = "L00%s/C%s.1" % (l1, j )
        if TYPE != "GAII" :
            for i2 in iter2:
                filelist = []
                for i1 in iter1:
                    filelist.append(srcdir + "/s_%s_%s%s_crop.gif" % ( l1, i1, i2) )
                tilefileg = destdir + "/org_%02d_%03d.gif" % (int(i2), j )
                if not os.path.isfile( tilefileg ):
                    if os.path.isfile(filelist[0]) :
                        execute( "convert +append " + " ".join(filelist) + " " + tilefileg ) 
                    else:
                        print "skipping creating", tilefileg, "can't find", filelist[0]
                else: 
                    print "skipping creating", tilefileg, "since it already exists"
        else:  # TYPE == "GAII"
            for (counter, pair) in enumerate(gaiitiles):
                filelist = []
                for i1 in pair:
                    filelist.append(srcdir + "/s_%s_%s_crop.gif" % ( l1, i1) )
                tilefileg = destdir + "/org_%02d_%03d.gif" % (counter + 1, j )
                if not os.path.isfile( tilefileg ):
                    if os.path.isfile(filelist[0]) :
                        execute( "convert +append " + " ".join(filelist) + " " + tilefileg )
                    else:
                        print "skipping creating", tilefileg, "can't find", filelist[0]
                else:
                    print "skipping creating", tilefileg, "since it already exists"

  #     create set of strips "orh" in wholeimages
        srcdir = "L00%s/C%s.1" % (l1, j )
        destdir = "wholeimages"
        if not os.path.isdir( destdir ) :
            os.system("mkdir " + destdir ) 
        filelist = []
        for i2 in iter2:
            tilefileg = srcdir + "/org_%02d_%03d.gif" % (int(i2), j )
            filelist.append(tilefileg) 

        tilefileh = destdir + "/orh-%s_%03d.gif" % (l1, j)
        if os.path.isfile( tilefileh ): 
            print "skipping creation of %s since %s already exists" % ( tilefileh, tilefileh )
        elif os.path.isfile( filelist[0] ) and not TYPE :
            execute(    "convert -append " + " ".join(filelist) + " "+ tilefileh )
        elif os.path.isfile( filelist[0] ) and TYPE :
            execute(    "convert -append " + " ".join(filelist) + " "+ tilefileh )
        else:
            print "can't find requisite ", filelist[0] , "needed to build ", tilefileh

#     create whole-cell images cell-
for j in CYCLES: 
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
    celltinytarget = destdir + "/cell-%03d.tiny.gif" % (j,)
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
            execute( "convert -resize  5% " + "%s %s" % ( celltarget, celltinytarget ))
        else: 
            print "skipping creating", cellsmalltarget, "because requisite", celltarget, "not found"
    else:
        print "skipping creating", cellsmalltarget , "because it already exists"
# create inset
    if not os.path.isfile( cellinsettarget ):
        if os.path.isfile( cellsmalltarget ):
            if TYPE == "HISEQ" or TYPE == "HISEQ2" :
                execute("convert %s  -page +700+200 L001/C%d.1/s_1_%s%s_crop2.gif  -mosaic %s" % (cellsmalltarget, j, iter1[0], iter2[0], cellinsettarget) )
            if TYPE == "MISEQ1" or TYPE == "GAII" or TYPE == "MISEQ2" :
                execute("convert -append %s  L001/C%d.1/s_1_%s%s_crop2.gif  -mosaic %s" % (cellsmalltarget, j, iter1[0], iter2[0], cellinsettarget) )
        else:
            print "skipping creating", cellinsettarget, "because requisite", cellsmalltarget, "is missing"
    else:
        print "skipping creating", cellinsettarget, "because it already exists"

for l1 in lane:
    srcdir = "wholeimages" 
    destdir = "wholeimages"
    bigtile =   destdir + "/tile-lane%s.big.gif" % (l1, )
    smalltile = destdir + "/tile-lane%s.small.gif" % (l1, )
    tinytile =  destdir + "/tile-lane%s.tiny.gif" % (l1, )
    filelist = []
    for j in CYCLES: 
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
        execute("convert -resize 12.5%" + " -border 2 " + " ".join(filelist) + " +append " + tinytile ) 
    else:
        print "skipping creating", smalltile 

largecellmovie = destdir + "/movie-lg.mp4"
smallcellmovie = destdir + "/movie-sm.mp4"
insetcellmovie = destdir + "/movie-in.mp4"
tinycellmovie = destdir + "/movie-ty.mp4"

if not os.path.isfile(largecellmovie):
    execute("avconv -r 5 -i " + destdir + "/cell-%03d.gif  " + largecellmovie )  # default compression ca. -q 31 ok
else:
    print "skipping creating", largecellmovie

if not os.path.isfile(smallcellmovie):
    execute("avconv -r 5 -i " + destdir + "/cell-%03d.small.gif -q 1   " + smallcellmovie ) # high quality / no compression
else:
    print "skipping creating", smallcellmovie 
if not os.path.isfile(insetcellmovie):
    execute("avconv -r 5 -i " + destdir + "/cell-%03d.inset.gif -q 1  " + insetcellmovie )  # high quality / no compression
else:
    print "skipping creating", insetcellmovie
if not os.path.isfile(tinycellmovie):
    execute("avconv -r 5 -i " + destdir + "/cell-%03d.tiny.gif -q 1  " + tinycellmovie )  # high quality / no compression
else:
    print "skipping creating", tinycellmovie

