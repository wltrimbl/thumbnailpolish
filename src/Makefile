# This makefile applies imagemagick to make false-color composites
# of the images in an illumina Thumbnails directory tree

# usage:
#  make configure   
#  make 
SRCDIR = $(dir . )
DESTDIR = $(dir . )
TYPE = $(shell head -n 1 thumbnailpolish.type)

thumbnailpolish.type:
	identifyimagetype.sh
	TYPE = $(shell head -n 1 thumbnailpolish.type)

movie: 
	tileimages.py

# This regular expression finds all the files in the target tree
COLOR := $(subst _A.jpg,_color.gif,$(subst _a.jpg,_color.gif,$(wildcard $(SRCDIR)/*/*/s*_a.jpg $(SRCDIR)/*/*/s*_A.jpg )))

CROP1 := $(subst _color.gif,_crop.gif,$(COLOR)) 
CROP2 := $(subst _color.gif,_crop2.gif,$(COLOR)) 

composite: all
	tileimages.py 

all:  $(COLOR) $(CROP1) $(CROP2)  thumbnailpolish.type

color: $(COLOR) thumbnailpolish.type

crop: $(CROP1) $(CROP2) thumbnailpolish.type

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
ifeq ($(TYPE),HISEQ)
	convert $^   -crop 45x450-0-0 \+repage $@
else ifeq ($(TYPE),HISEQ2)
	convert $^   -crop 90x450-0-0 \+repage $@
else ifeq ($(TYPE),MISEQ)
	convert $^ -crop 300x300-0-0 \+repage  $@ 
else ifeq ($(TYPE),GAII)
	convert $^ -crop 275x300-0-0 \+repage  $@ 
endif

%_crop2.gif : %_color.gif
ifeq ($(TYPE),HISEQ)
	convert $^ -crop 149x149+47+151 +repage $@
else ifeq ($(TYPE),HISEQ2)
	convert $^ -crop 149x149+93+151 +repage $@
else ifeq ($(TYPE),MISEQ)
	convert $^ -crop 99x99+309+101 +repage $@ 
else ifeq ($(TYPE),GAII)
	convert $^ -crop 99x99+277+101 +repage $@
endif

clean:
	rm */C*/*color.gif */C*/*crop2.gif */C*/*crop.gif
