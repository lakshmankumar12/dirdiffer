#!/usr/bin/python

from __future__ import print_function
import sys
import os
import argparse
import hashlib

'''
Lets build a collection which is a dictionary of sha1's.
Each value is inturn a list of size 2
Each index is the directory. And each entry is the collection of pathnames in that directory
that have this sha1

collection = {
   sha1:   [  ['/dir1/path1','/dir1/path2' ] , ['/dir2/path1/', '/dir2/path2/' ] ],
   ...
}
'''

def usage():
  print("%s <dir1> <dir2>"%sys.argv[0])
  print("  ")
  print("  dir1 and dir2 will be diffed and it will report file-contents that are")
  print("  presently only in dir1 and dir2")

def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument("-b","--both", help="Print files common in both", action="store_true")
  parser.add_argument("dir1", help="dir1")
  parser.add_argument("dir2", help="dir2")
  args = parser.parse_args()
  return args

def sha1offile(fileName):
  BLOCKSIZE = 65536
  hasher = hashlib.sha1()
  with open(fileName, 'rb') as afile:
      buf = afile.read(BLOCKSIZE)
      while len(buf) > 0:
          hasher.update(buf)
          buf = afile.read(BLOCKSIZE)
  return hasher.hexdigest()

def walk_dir_and_build_sha(dirname, collection, dir_index):

  count = 0
  for root,_,files in os.walk(dirname):
    for f in files:
      fname = os.path.join(root,f)
      if os.path.islink(fname):
        continue
      if os.path.isfile(fname):
        count += 1
        if count % 100 == 0:
          print ("Processed %d files in %s"%(count,dirname))
        sha1 = sha1offile(fname)
        if sha1 not in collection:
          collection[sha1] = [ [], [] ]
        collection[sha1][dir_index].append(fname)

  return count

def compare_and_report(collection):
  onlyOneDirShas = [ [], [] ]
  both = []
  for sha in collection:
    found_both = 1
    for i in range(2):
      if not collection[sha][i]:
        found_both = 0
        onlyOneDirShas[1-i].append(sha)
    if found_both:
      both.append(sha)

  return (onlyOneDirShas, both)


if __name__ == '__main__':
  args = parseArgs()
  collection = {}
  count1 = walk_dir_and_build_sha(args.dir1, collection, 0)
  count2 = walk_dir_and_build_sha(args.dir2, collection, 1)
  onlyFiles, both = compare_and_report(collection)
  print("We found %d files in %s and %d files in %s"%(count1,args.dir1,count2,args.dir2))
  names=[args.dir1,args.dir2]
  for i in range(2):
    print("Only in %s .. count: %d"%(names[i],len(onlyFiles[i])))
    for sha in onlyFiles[i]:
      for j in collection[sha][i]:
        print("%s"%j)
      print("")
    print("")
  print ("Available in both .. count:%d"%(len(both)))
  if args.both:
    for sha in both:
      for i in range(2):
        for j in collection[sha][i]:
          print ("%s"%j)
    print("")




