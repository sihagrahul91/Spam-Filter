#! /usr/bin/python
# References Article: http://www.cs.ubbcluj.ro/~gabis/DocDiplome/Bayesian/000539771r.pdf
import os
import sys
import getopt
from collections import defaultdict
import time
import math
import argparse
def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-f1',required=True)
    parser.add_argument('-f2',required=True)
    parser.add_argument('-o',required=True)
    args = vars(parser.parse_args())
    train = args['f1']
    test = args['f2']
    output = args['o']

    st = time.time()
    f = open(train)                                         # Take file name as input from command line
    
    ham = defaultdict(int)
    spam = defaultdict(int)
    total = defaultdict(int)
    countSpam = 0
    countHam = 0
    countTotal = 0
    spamTotal = 0
    hamTotal = 0
    alpha = 0.5
    for line in f:
        line = line.rstrip('\n')
        words = line.split(' ')
        emailID = words[0]           #email ID
        emailType = words[1]         #spam/ham
        words = words[2:]
        words = zip(words,words[1:])[::2]

        if emailType=="ham":
            countHam +=1
            for a,b in words:
                ham[a] += 1
                hamTotal+=1
                total[a] += 1

        elif emailType=="spam":
            countSpam +=1
            for a,b in words:
                spam[a] += 1
                spamTotal+=1
                total[a] += 1

    
#    print countSpam,countHam,len(ham),len(spam),len(total) 
#    print ham
#    print time.time()-st
    print "Y:",spamTotal, countSpam,spam
    spamProb = float(countSpam)/float(countSpam)+float(countHam)
    hamProb = float(countHam)/float(countSpam)+float(countHam)
    f = open(test)
    fact1 = math.log(spamProb/hamProb)
    correct = 0
    testTotal = 0
    output_file = open(output,'w')
    for line in f:
        line = line.rstrip('\n')
        words = line.split(' ')
        emailID = words[0]           #email ID
        emailType = words[1]         #spam/ham
        words = words[2:]
        words = zip(words,words[1:])[::2]
        fact2 = 0
        testTotal+=1
        for a,b in words:
          #  try:
             #pWiS = float(spam[a]+alpha)/float(countSpam+alpha*len(total))
             #pWiH = float(ham[a]+alpha)/float(countHam+alpha*len(total))
             pWiS = float(spam[a]+alpha)/float(spamTotal+alpha*len(total))
             pWiH = float(ham[a]+alpha)/float(hamTotal+alpha*len(total))
             #print pWiS,pWiH
             try:
                 fact2+=math.log(pWiS/pWiH)
             except:
                 fact2 += 0
           
             #fact2 += math.log((float(spam[a])/float(countSpam))/(float(ham[a])/float(countHam)))
        #print fact1,fact2,fact1+fact2
        if fact1+fact2>0:
            output_file.write("spam\n")
        else:
            output_file.write("ham\n")
        if fact1+fact2>0 and emailType == "spam":
            correct+=1
        if fact1+fact2<0 and emailType == "ham":
            correct+=1
    print correct,testTotal
    print "Accuracy = ",(float(correct)/float(testTotal))*100
    output_file.close()
    with open(output, 'rb+') as filehandle:
        filehandle.seek(-1, os.SEEK_END)
        filehandle.truncate()
if __name__ == "__main__":
    main()
