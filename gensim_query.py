#!/usr/local/bin/python

#coding:-*-utf-8-*-

#*******************************************************************************
# gensim_query.py
#
# 
# Usage: 
#     Parameters: seedcorpus, seedindex, sentence
# 
#                                                Author: dzn    Date: 01-12-2015
#*******************************************************************************

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import os
import jieba
import getopt
import time
import logging
from gensim import corpora, similarities, models
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', level=logging.INFO)

def Txt2Dict(file_name):
    dict_name = {}
    for line in open(file_name) :
        kv = line.strip().split('\t')
        dict_name[kv[0].strip()] = [v for v in kv[1:]]        
    return dict_name

# Read column, and return a list
def ReadColumn(infile, col_index):
    column = {}
    i      = 0
    for text in open(infile):
        text      = text.replace('\n','').split()
        column[i] = text[col_index]
        i        += 1
    return column

def gensimquery(indexpath, corpuspath, sentence, numbest, threshold, run_date):
    
    indexdict    = Txt2Dict(indexpath)
    stopword     = "/home/dzn/Similarity/stopwords.txt"     #stopword dictionary
    punctuation  = "/home/dzn/Similarity/punctuations.txt"  # punctuation dictionary
    Stopwords    = set([word.decode('utf-8') for word in open(stopword).read().split('\n')])      # Reload stopwords.txt
    Punctuations = set([word.decode('utf-8') for word in open(punctuation).read().split('\n')])   # Reload punctuations.txt
    texts        = jieba.cut(sentence)
    texts        = [word.strip() for word in texts if not word in Stopwords]   # texts filtered stopwords
    texts        = [word.strip() for word in texts if not word in Punctuations]   # texts filtered punctuations

    indexlist = ReadColumn(indexpath, 0) # Read Index of Seeds
    # Read Corpus when needed !
    class ReadCorpus(object):
        def __iter__(self):
            for line in open(corpuspath):
                yield line.split()

    corp        = ReadCorpus()  # Read corpus as Corp
    dictionary  = corpora.Dictionary(corp) # Create dictionary
    corpus      = [dictionary.doc2bow(text) for text in corp] # get bag-of-word
    tfidf       =  models.TfidfModel(corpus)   # Create TF-IDF Model
    corpus_tfidf= tfidf[corpus]
    # Calculate Similarities 
    index       = similarities.Similarity(run_date+"/index",corpus,num_features = len(dictionary))
    index.num_best = numbest
    querybow    = dictionary.doc2bow(texts)
    print querybow
    outquery    = dict(index[querybow])
    if len(outquery.values()) >= 1:
        maxvalue    = max(outquery.values())
        outindex    = dict([(key, value) for key, value in outquery.items() if value >= (maxvalue-threshold)])
        print "outquery--------------------"
        print outquery
        print "outindex--------------------"
        print outindex
        print "indexlist-------------------"
        print indexlist
        print "indexdict-------------------"
        print indexdict
        outquery    = open(run_date+"/search.txt", 'w')
        for k1, v1 in outindex.items():
            outquery.write("%s \t" % k1)
            print k1
            outquery.write("%s \t" % outindex[k1])
            tmp = " ".join(str(a) for a in indexdict[indexlist[k1]])
            print tmp
            outquery.writelines(tmp+"\n")
        outquery.close()
    else :
        print "No News Find !"
def validateopts(opts):
	#indexpath   = '/home/aaa/hd/corpus/seedindex.txt'     # Default Seedindex File
	#corpuspath  = '/home/aaa/hd/corpus/seedcorpus.txt'    # Default Seedcorpus File
	threshold    = 0.15                                    # Default similarity threshold = 0.15
	numbest      = 10                                      # Defalut index.num_best = 10
	for option, value in opts:
		if option  in ["-h", "--help"]:
			tips()
		elif option in ["--indexpath", "-i"]:
			indexpath = value
		elif option in ["--sentence", "-s"]:
			sentence  = value
		elif option in ["--corpuspath", "-c"]:
			corpuspath = value
		elif option in ["--threshold", "-t"]:
		    threshold = int(value)
		elif option in ["--numbest", "-n"]:
		    numbest = int(value)
		elif option in ["--run_date", "-r"]:
		    run_date = value		    
		elif option == "-u":
			print "usage -u"
	return indexpath, corpuspath, sentence, numbest, threshold, run_date

def tips():
	"""Display the usage tips"""
	print "Please use: "+sys.argv[0]+" [options]"
	print "usage:%s --indexpath=value --corpuspath=value --sentence=value --numbest=value --threshold=value --run_date=value"
	print "usage:%s -i value -c value -s value -n value -t threshold -r run_date"
	sys.exit(2)

def main():
	global rundate
	try:
		opts,args = getopt.getopt(sys.argv[1:],"hi:c:s:n:t:r:u",["indexpath=","corpuspath=","sentence=","numbest=","threshold=","run_date=","help"])
	except getopt.GetoptError:
		tips()
	if len(opts) >= 4:
		indexpath, corpuspath, sentence, numbest, threshold, run_date = validateopts(opts)
	else:
		print "ErrorMessage: Please Check What Your Input !"
		tips()
		raise SystemExit	

	if not (os.path.isfile(indexpath)):
		print "ErrorMessage: Please Check Your Index_file !"
		raise SystemExit

	if not (os.path.isfile(corpuspath)):
		print "ErrorMessage: Please Check Your Corpus_file !"
		raise SystemExit
			
	print '*****************************************'
	print 'corpuspath = ' + corpuspath
	print 'indexpath  = ' + indexpath
	print 'sentence   = ' + sentence
	print 'numbest    = ' + str(numbest)
	print 'run_date   = ' + run_date
	print '*****************************************'
	
	
	start_CPU = time.clock()
	gensimquery(indexpath, corpuspath, sentence, numbest, threshold, run_date)
	end_CPU = time.clock()
	
	print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
	print("GensimQuery Costs: %f CPU seconds" % (end_CPU - start_CPU))

if __name__ == '__main__':
	main()


             



