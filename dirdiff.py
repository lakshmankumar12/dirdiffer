from __future__ import print_function
import sys
import argparse
import hashlib

'''
Lets build a collection which is a dictionary of sha1's.
Each value is inturn a GrowingList of lists.
Each index is the directory. And each entry is the collection of pathnames in that directory
that have this sha1

collection = {
   sha1:   [  ['/dir1/path1','/dir1/path2' ] , ['/dir2/path1/', '/dir2/path2/' ] ],
   ...
}

book_keep_info {
  dirs :  { 'dirname1' : dirindex },       #size of book_keep_info[dirs] gives the total dirs so far.

}
'''

# Taken from http://stackoverflow.com/a/4544699/2587153
class GrowingList(list):
  def __setitem__(self, index, value):
    if index >= len(self):
        self.extend([None]*(index + 1 - len(self)))
    list.__setitem__(self, index, value)

def usage():
  print("%s <dir1> <dir2>"%sys.argv[0])
  print("  ")
  print("  dir1 and dir2 will be diffed and it will report file-contents that are")
  print("  presently only in dir1 and dir2")

def parseArgs():
  parser = argparse.ArgumentParser()
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

def walk_dir_and_build_sha(dirname, collection, book_keep_info):

  if dirname not in book_keep_info['dirs']:
    dir_index = len(book_keep_info['dirs'].keys())
    book_keep_info[dirs][dirname] = dir_index
  else:
    dir_index = book_keep_info['dirs'][dirname]

  count = 0
  for root,_,files in os.walk(dirname):
    for f in files:
      fname = os.path.join(root,f)
      if os.path.islink(fname):
        continue
      if os.path.isfile(fname):
        count += 1
        sha1 = sha1offile(fname)
        if sha1 not in collection:
          collection[sha1] = GrowingList()
        collection[sha1][dir_index].append(fname)

  return count

def compare_and_report(collection, book_keep_info):
  no_dirs = len(book_keep_info['dirs'])
  for sha in collection:
    for dircontent in collection[sha]:
      if len(dircontent)


if __name__ == '__main__':
  args = parseArgs()
  collection = {}
  book_keep_info = { 'dirs' : {} }

