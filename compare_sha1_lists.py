#!/usr/bin/python

from __future__ import print_function
import sys
import string
import argparse

def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument("-b","--both", help="Print files common in both", action="store_true")
  parser.add_argument("-s","--supress", help="supress sha1 printing", action="store_true")
  parser.add_argument("-w","--writefile", help="write-in-file <file>-dir1 <file>-dir2 <file-both>")
  parser.add_argument("dir1", help="file containing dir1 listing")
  parser.add_argument("dir2", help="file containing dir2 listing")
  args = parser.parse_args()
  return args


def walk_dir_and_build_sha(dirfile, collection, dir_index):

  count = 0
  with open(dirfile, "r") as f:
    for i in f:
      i = i.strip()
      if not i:
        continue
      sha1=i[:40]
      if not all(c in string.hexdigits for c in sha1):
        print("line:%s is not having a good sha"%i)
        sys.exit(1)
      if not i[40:42] == "  ":
        print("line:%s is not having 2 spaces after sha"%i)
        sys.exit(1)
      fname=i[42:]
      count+=1
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
    if args.writefile:
      f=open(args.writefile + 'dir%d'%(i+1), 'w')
    print("Only in %s .. count: %d"%(names[i],len(onlyFiles[i])))
    for sha in onlyFiles[i]:
      if not args.supress:
        print (sha)
      for j in collection[sha][i]:
        print("%s"%j)
        if args.writefile:
          print("%s"%j,file=f)
      print("--")
      if args.writefile:
        print("--",file=f)
    if args.writefile:
      f.close()
    print("----")
  print ("Available in both .. count:%d"%(len(both)))
  if args.both:
    if args.writefile:
      f=open(args.writefile + 'both', 'w')
    for sha in both:
      if not args.supress:
        print(sha)
      for i in range(2):
        for j in collection[sha][i]:
          print ("%s  %s"%(names[i],j))
          if args.writefile:
            print ("%s  %s"%(names[i],j),file=f)
      print("--")
      if args.writefile:
        print("--",file=f)




