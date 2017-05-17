## Evaluate.py
# evaluates:
# 	- precision
# 	- recall
# inputs:
# 	- relevant: number of documents in dataset relevant to a particular query
# 	- retrieved: number of results returned for a query
#	- relevant_retrieved: number of relevant documents returned by a query

# USE:
# 	- from command line, call the script like this
# 		python evaluate.py relevant retrieved relevant_retrieved
# 					~~~~ EXAMPLE ~~~~
# 		python evaluate.py 15 9 3
# 
# 	- from another python file, simply import 'evaluate' and use the methods
# 		import evaluate;
#		recall = (evaluate.getRecall(15,9,3));

from __future__ import division;
import sys;

def main():
	relevant = (14 if len(sys.argv)<2 else int(sys.argv[1]));
	retrieved = (10 if (len(sys.argv)<3) else int(sys.argv[2]));
	relevant_retrieved = (8 if (len(sys.argv)<4) else int(sys.argv[3]));
	precision = getPrecision(relevant, retrieved, relevant_retrieved);
	recall = getRecall(relevant, retrieved, relevant_retrieved);
	return {"precision":precision, "recall":recall};

# Precision is the number of relevant retrieved documents divided by the number of retrieved documents
def getPrecision(rel, ret, relret):
	pre = (float(relret/ret));
	print ("Precision: "+str(pre));
	return pre;

# Recall is the number of relevant retrieved documents divided by the number of relevant documents
def getRecall(rel, ret, relret):
	rec = (relret/rel);
	print ("Recall: "+str(rec));
	return rec;

if __name__ == "__main__":
	main(); 