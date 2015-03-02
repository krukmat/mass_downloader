import urllib2
import threading
import Queue
import urllib

threads        = 1
filelist_file  = "./amia.txt" # from SVNDigger
resume         = None
user_agent     = "Mozilla/5.0 (X11; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0"

def file_downloader(urls_queue):
      while not urls_queue.empty():
          url = word_queue.get()
          print "Trying: %s" % (url)
          try:
                webFile = urllib.urlopen(url)
                localFile = open(url.split('/')[-1], 'w')
                localFile.write(webFile.read())
                if len(webFile.read()):
                    print "[%d] => %s" % (webFile.code,url)
                webFile.close()
                localFile.close()
          except urllib2.URLError,e:
                if hasattr(e, 'code') and e.code != 404:
                    print "!!! %d => %s" % (e.code, url)
                else:
                    print e


def build_fileslist(filelist_file):

      # read in the word list
      fd = open(filelist_file,"rb")
      raw_words = fd.readlines()
      fd.close()

      found_resume = False
      words        = Queue.Queue()

      for word in raw_words:

          word = word.rstrip()

          if resume is not None:

              if found_resume:
                  words.put(word)
              else:
                  if word == resume:
                      found_resume = True
                      print "Resuming url from: %s" % resume
          else:
              words.put(word)

      return words

word_queue = build_fileslist(filelist_file)

for i in range(threads):
    t = threading.Thread(target=file_downloader, args=(word_queue,))
    t.start()