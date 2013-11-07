# This makefile applies imagemagick to make false-color composites
# of the images in an illumina Thumbnails directory tree

# usage:
#  make configure   
#  make composite

SRCDIR = $(dir . )
DESTDIR = $(dir . )

TYPE = $(shell head -n 1 thumbnailpolish.type)

ifeq ($(TYPE),HISEQ)
  CROP1DIM=45x450-0-0
  CROP2DIM=149x149+47+151    
else ifeq ($(TYPE),HISEQ2)
  CROP1DIM=90x450-0-0
  CROP2DIM=149x149+93+151
else ifeq ($(TYPE),MISEQ)
  CROP1DIM=300x300-0-0
  CROP2DIM=99x99+309+101
else ifeq ($(TYPE),GAII)
  CROP1DIM=275x300-0-0
  CROP2DIM=99x99+277+101
endif

#ifeq (,$(wildcard thumbnailpolish.type))
#	$(error thumbnailpolish.type does not exist, try running make configure)
#endif

# Spider SRCDIR looking for jpgs to convert
# This regular expression finds all the files in the target tree
COLOR := $(subst _A.jpg,_color.gif,$(subst _a.jpg,_color.gif,$(wildcard $(SRCDIR)/*/*/s*_a.jpg $(SRCDIR)/*/*/s*_A.jpg )))
# This regular expression should find the auxillary files, should you want to colorize them
AUX   := $(subst _A.jpg,_color.gif,$(subst _a.jpg,_color.gif,$(wildcard $(SRCDIR)/*/*/d*_a.jpg $(SRCDIR)/*/*/d*_A.jpg )))
# crop1 contains the image of the tile
CROP1 := $(subst _color.gif,_crop.gif,$(COLOR)) 
# crop2 contains one of the closeup images
CROP2 := $(subst _color.gif,_crop2.gif,$(COLOR)) 

configure:
	identifyimagetype.sh

composite: all
	tileimages.py 

all:  $(COLOR) $(CROP1) $(CROP2)
 
color: $(COLOR) 

aux:   $(AUX)

crop: $(CROP1) $(CROP2)

%_1.gif : 
	$(eval TFILE = $(wildcard $(subst _1.gif,_T.jpg,$@) $(subst _1.gif,_t.jpg,$@)))
	$(eval GFILE = $(wildcard $(subst _1.gif,_G.jpg,$@) $(subst _1.gif,_g.jpg,$@)))
	composite -compose minus $(TFILE) $(GFILE) $@
	
%_2.gif : %_1.gif 
	$(eval AFILE = $(wildcard $(subst _2.gif,_A.jpg,$@) $(subst _2.gif,_a.jpg,$@)))
	composite -compose plus $(AFILE) $^ $@

%_color.gif : %_2.gif 
	$(eval CFILE = $(wildcard $(subst _color.gif,_C.jpg,$@) $(subst _color.gif,_c.jpg,$@)))
	$(eval GFILE = $(wildcard $(subst _color.gif,_G.jpg,$@) $(subst _color.gif,_g.jpg,$@)))
	convert $^  $(CFILE) $(GFILE) -combine $@

%_crop.gif : %_color.gif
	convert $^   -crop $(CROP1DIM) \+repage $@

%_crop2.gif : %_color.gif
	convert $^ -crop $(CROP2DIM) +repage $@

clean:
	rm */C*/*color.gif */C*/*crop2.gif */C*/*crop.gif
