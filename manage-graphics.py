#!/usr/bin/env python
import sys,os,os.path
import Image,cv

""" output dimension metric
128 96 64 48 32
"""
dims = {
#  (2048,-1):'2048w',(1024,-1):'1024w',(3000,-1):'3000w',
#  (300,-1):'300w',(200,-1):'200w',(400,-1):'400w',
#  (-1,300):'300h',(-1,200):'200h',(-1,120):'120h',


  (128,128):'128', 	(128,-1):'128w', 	(-1,128):'128h',
  (96,96):'96', 	(96,-1):'96w', 		(-1,96):'96h',
  (64,64):'64', 	(64,-1):'64w', 		(-1,64):'64h',
  (48,48):'48', 	(48,-1):'48w', 		(-1,48):'48h',
  (32,32):'32', 	(32,-1):'32w', 		(-1,32):'32h'
}

def info():
  """ Web graphics management tool <chayapan@gmail.com>
'h' for help, 'q' to exit.
  """
  return info.__doc__

def resizeToDim(file,dim,out_dir):
  """	resize the image file to size specify by dim tuple
	if -1 means that it should be propotional
  """
  im = Image.open(file)
  thumb_dim = []
  # calculate missing dim
  gd = max(im.size[0],im.size[1])
  s = dim
  if(dim[0] <= 0): # width undetermine, calculate from image size
	w = 1.0*dim[1]/im.size[0]*gd
        h = 1.0*dim[1]/im.size[1]*gd
        s = (w,h)
  if(dim[1] <= 0):
	w = 1.0*dim[0]/im.size[1]*gd
        h = 1.0*dim[0]/im.size[0]*gd
        s = (w,h)
  print "file: %s %s dim: %s" % (file,str(im.size),s)
  s = (int(s[0]),int(s[1]))
  im.thumbnail(s,Image.ANTIALIAS)
  global dims
  outname = os.path.join(out_dir,file);
  print outname
  im.save(outname)

def process_files(files,dims,working_dir='.'):
  #dims = [dim for dim in dims]
  for file in files:
    for dim in dims:
      print "dim spec %s" % str(dim)
      print dims[dim]
      out_dir = os.path.join(working_dir,dims[dim])
      resizeToDim(file,dim,out_dir)

def prepare_output_dir(dims,working_dir='.'):
  """	create output folders for scaled dimensions if needed
	in 'working_dir'
  """
  dirs = [dims[dim] for dim in dims]
  print "preparing output dirs.... \n%s" % ",".join(dirs)
  # Enumerating directory list that will be used
  out_dirs = [os.path.join(working_dir,dir) for dir in dirs]
  # If the directory doesn't exist yet, create
  to_create = [dir for dir in out_dirs if not os.path.exists(dir)]
  if (len(to_create) > 0):
    print "creating dir.... \n%s" % ",".join(to_create)
    [os.makedirs(dir) for dir in to_create] 

  depth = 1
  for c,dirs,files in os.walk(working_dir):
    image_files = files
    depth = depth + 1    # only traverse first level, c = working_dir
    if depth > 1: break
  print "processing... " # % image_files
  return image_files
  #for file in image_files:

"""
    for dim in dims:
	print "dir %s " % dims[dim]
	print dim
"""

if __name__ == '__main__':
  print info()
  PROMPT = '>'
  WORKING_DIR = os.path.abspath(os.curdir)
  WORKING_FILES = []
  while True:
    print "working dir: %s" % WORKING_DIR
    WORKING_FILES = prepare_output_dir(dims,WORKING_DIR) # check and create output dirs as necessarily
    print WORKING_FILES
    process_files(WORKING_FILES,dims,WORKING_DIR)
    cmd = raw_input(PROMPT)
    # Commands
    if cmd == 'q': sys.exit(0)
