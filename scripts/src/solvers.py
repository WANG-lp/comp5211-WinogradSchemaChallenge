from random import randint
import string
import copy
import logging

from input_parse import InputParser
from common import TagProcessor
from nltk_helper import SentenceParser
from kb import WordParser, KB

from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from nltk.corpus import wordnet


# Intput is the unknownword and a word in KB;
def getFeature(UnkownWord, KBWord):
    syns1 = wordnet.synsets(UnkownWord)
    syns2 = wordnet.synsets(KBWord)
    sim_value = 0
    if (len(syns1) == 0 or len(syns2) == 0):
        return 0

    count = 1
    for lemma1 in syns1:
        for lemma2 in syns2:
            if lemma1.wup_similarity(lemma2) is None:
                sim_value = sim_value + 0
            else:
                sim_value = sim_value + lemma1.wup_similarity(lemma2)
                count = count + 1

    return (sim_value / count)


# input the word you want to know and the KB dictionary.
def getWordValue(word, wordList):
    if word in wordList.keys():
        return wordList[word]

    sim_dict = {}
    for kword in wordList.keys():
        sim_value = getFeature(word, kword)
        sim_dict[kword] = sim_value

        # sim_dict is a dict contains the similarity of new words compared with words in KB
    returnK = max(sim_dict, key=sim_dict.get)
    return wordList[returnK]


class SolverBaseClass(object):
    def __init__(self):
        self.tagProcessor = TagProcessor()
        self.sentenceParser = SentenceParser()
        self.vbParser = WordParser()
        kb = KB()
        self.verbKB = kb.getVerbKB()
        self.adjKB = kb.getAdjKB()

        # print self.verbKB
        # print self.adjKB

    def solver(self, question):
        return 'a'

    def returnAns(self, ans):
        if ans > 0:
            return 'a'
        else:
            return 'b'

    def mapAB(self, q):
        question = copy.deepcopy(q)
        question[0]['txt1'] = string.replace(question[0]['txt1'], question[2][0], ' Alice ')
        question[0]['txt1'] = string.replace(question[0]['txt1'], question[2][1], ' Emily ')
        # print question[2][0]
        # print question[2][1]
        # print question[0]['txt1']
        tx1_tags = self.sentenceParser.makeTags(question[0]['txt1'])
        verbIndex = 0
        for i in range(0, len(tx1_tags)):
            if self.tagProcessor.isVerb(tx1_tags[i]):
                verbIndex = i
                break
        s1 = " ".join(x[0] for x in tx1_tags[:verbIndex])
        # s2 = " ".join(x[0] for x in tx1_tags[verbIndex:])

        if s1.find(question[2][0]) != -1:
            return question, 1
        return question, -1

    def listContainsNone(self, aList):
        for x in aList:
            if x is None:
                return True
        return False

    def fixFeature(self, features):
        res = []
        for f in features:
            if f is None:
                res.append(None)
            elif f < 0:
                res.append(-1)
            else:
                res.append(1)
        return res

    def extractFeatures(self, q):
        question, answer_order = self.mapAB(q)
        txt1_tags = self.sentenceParser.makeTags(question[0]['txt1'])
        # print txt1_tags
        txt1_positive = 1
        if self.tagProcessor.isNegativeFromList(txt1_tags):
            txt1_positive = -1

        txt2_tags = self.sentenceParser.makeTags(question[0]['pron'] + " " + question[0]['txt2'])
        # print txt2_tags
        txt2_positive = 1
        if self.tagProcessor.isNegativeFromList(txt2_tags):
            txt2_positive = -1

        txt1_v = ''
        txt1_prop = None
        for v in txt1_tags[::-1]:
            if self.tagProcessor.isVerb(v):
                txt1_v = v[0]
                txt1_prop = getWordValue(txt1_v, self.verbKB)
                break

        txt2_v = ''
        txt2_adj = ''
        txt2_prop = None
        for v in txt2_tags[::-1]:
            if self.tagProcessor.isAdj(v):
                txt2_adj = v[0]
                txt2_prop = getWordValue(txt2_adj, self.adjKB)
                break

        if txt2_prop is None:
            for v in txt2_tags[::-1]:
                if self.tagProcessor.isVerb(v):
                    txt2_v = v[0]
                    txt2_prop = getWordValue(txt2_v, self.verbKB)
                    break

        if txt1_prop is None:
            txt1_prop = 1
        if txt2_prop is None:
            txt2_prop = 1
        return [txt1_positive, txt2_positive, txt1_prop, txt2_prop]


class RandomForestsSolver(SolverBaseClass):
    def train(self, questionList, n_est=6):
        featuresList = []
        targetList = []
        for q in questionList:
            features = self.extractFeatures(q)
            features = self.fixFeature(features)
            if not self.listContainsNone(features):
                featuresList.append(features)
                if q[-1] == 'a':
                    targetList.append(1)
                else:
                    targetList.append(-1)
        self.clf = RandomForestClassifier(n_estimators=n_est)
        self.clf = self.clf.fit(featuresList, targetList)

    def solver(self, question):
        features = self.extractFeatures(question)
        features = self.fixFeature(features)
        if self.listContainsNone(features):
            print features
            print "feature fail"
            return 'N/A'
        else:
            ans = self.clf.predict([features])[0]
            return self.returnAns(ans)


class GussianSolver(SolverBaseClass):
    def train(self, questionList):
        featuresList = []
        targetList = []
        for q in questionList:
            features = self.extractFeatures(q)
            features = self.fixFeature(features)
            if not self.listContainsNone(features):
                featuresList.append(features)
                if q[-1] == 'a':
                    targetList.append(1)
                else:
                    targetList.append(-1)
        self.clf = GaussianNB()
        self.clf = self.clf.fit(featuresList, targetList)

    def solver(self, question):
        features = self.extractFeatures(question)
        features = self.fixFeature(features)
        if self.listContainsNone(features):
            print features
            print "feature fail"
            return 'N/A'
        else:
            ans = self.clf.predict([features])[0]
            return self.returnAns(ans)


class SVMSolver(SolverBaseClass):
    def train(self, questionList):
        featuresList = []
        targetList = []
        for q in questionList:
            # print q
            features = self.extractFeatures(q)
            features = self.fixFeature(features)
            if not self.listContainsNone(features):
                featuresList.append(features)
                if q[-1] == 'a':
                    targetList.append(1)
                else:
                    targetList.append(-1)
        self.clf = svm.SVC()
        self.clf.fit(featuresList, targetList)
        self.clf.fit(featuresList, targetList)

    def solver(self, question):
        features = self.extractFeatures(question)
        features = self.fixFeature(features)
        if self.listContainsNone(features):
            print features
            print "feature fail"
            return 'N/A'
        else:
            ans = self.clf.predict([features])[0]
            return self.returnAns(ans)


class PositiveNegativeSolver(SolverBaseClass):
    def solver(self, question):
        features = self.extractFeatures(question)
        features = self.fixFeature(features)

        ans = 1
        print features
        for x in features:
            ans = ans * x

        return self.returnAns(ans)


class RandomSolver(SolverBaseClass):
    def solver(self, question):
        if randint(0, 1) == 0:
            return 'a'
        else:
            return 'b'


import os, sys

if os.name == 'posix' and sys.version_info[0] < 3:
    import subprocess32 as subprocess
else:
    import subprocess
from xml.dom import minidom

class StandfordCorefSolver(SolverBaseClass):
    enable = True

    def __init__(self, standford_dir="/csproject/comp5211/stanford-corenlp-full-2015-12-09/"):
        if not standford_dir[-1] == "/":
            standford_dir += '/'
        super(self.__class__, self).__init__()
        print "Checking Standford CoreNlp package..."
        if os.path.isdir(standford_dir):
            self.enable = True
            self.rootPath = standford_dir
            print "Found Standford CoreNlp Package in " + standford_dir
            if not os.path.isdir(standford_dir + "inputs"):
                try:
                    os.mkdir(standford_dir + "inputs")
                except Exception, e:
                    print e.message
                    self.enable = False
        else:
            print "Not found Standford coNlp library in " + standford_dir + " directory"
            print "Please check the standford coNlp library path..."
            self.enable = False
            print "Exiting..."
            exit(-1)

    def solver(self, question):
        if not self.enable:
            return 'N/A'
        try:
            with open(self.rootPath + "question.txt", "wb") as f:
                f.write(question[0]['txt1'] + ' ' + question[0]['pron'] + ' ' + question[0]['txt2'])
                f.write(' ' + question[1]['quote1'] + ' ' + question[1]['pron'] + ' ' + question[1]['quote2'] + '\n')
        except Exception, e:
            print e.message
            print "Cannot create input file for Standford CoNlp...  exit.."
            return 'N/A'

        try:
            logging.info("Invoking Standford CoNlp...")
            subprocess.check_call(['java', '-Xmx5g', '-cp', 'stanford-corenlp-3.7.0.jar:'
                                                            'stanford-corenlp-models-3.7.0.jar:*',
                                   'edu.stanford.nlp.pipeline.StanfordCoreNLP',
                                   '-annotators', 'tokenize,ssplit,pos,lemma,ner,parse,mention,coref',
                                   '-coref.algorithm', 'neural', '-file', './question.txt'],
                                  cwd=self.rootPath, shell=False, stdout=open(os.devnull, 'wb'),
                                  #stderr=open(os.devnull, 'wb')
                                  )
            xmldoc = minidom.parse(self.rootPath+"question.txt.xml")
            mentions = xmldoc.getElementsByTagName("mention")

            ans_txt = ""
            for m in mentions:
                if m.attributes.keys() == u'representative':
                    for v in m.attributes.values():
                        if v.firstChild.data == u'true':
                            ans_txt = m.getElementsByTagName("text")[0].firstChild.data.strip().lower()

            if ans_txt.find(question[2][0]):
                return 'a'
            else:
                return 'b'


        except Exception, e:
            print e.message
            print "Invoke Standford CoNlp library error..."
            print "Exiting..."
            exit(-1)


