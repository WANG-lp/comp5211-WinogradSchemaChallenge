from random import randint
import string

from input_parse import InputParser
from common import TagProcessor
from nltk_helper import SentenceParser
from kb import WordParser, KB

from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from nltk.corpus import wordnet


# Intput is the unknownword and a word in KB;
class WordValue:
    def getFeature(UnkownWord, KBWord):
        syns1 = wordnet.synsets(UnkownWord)
        syns2 = wordnet.synsets(KBWord)
        sim_value = None
        for lemma1 in syns1:
            for lemma2 in syns2:
                sim_value += lemma1.wup_similarity(lemma2)

        sim_value = sim_value / (len(syns1) * len(syns2))
        return sim_value

    def getWordValue(word, wordList):
        # def getValue:
        if word in wordList.keys():
            return wordList(word)

        sim_dict = {}
        for kword in wordList.keys():
            sim_value = getFeature(word, kword)
            sim_dict[kword] = sim_value

        # sim_dict is a dict contains the similarity of new words compared with words in KB
        return 0


class SolverBaseClass:
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

    def returnAns(self, ans, par1, par2):
        ans = ans * par1 * par2
        if ans > 0:
            return 'a'
        else:
            return 'b'

    def mapAB(self, question):
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
            return 1
        return -1

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

    def extractFeatures(self, question):
        answer_order = self.mapAB(question)
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
                txt1_prop = self.verbKB[txt1_v]
                break

        txt2_v = ''
        txt2_adj = ''
        txt2_prop = None
        for v in txt2_tags[::-1]:
            if self.tagProcessor.isAdj(v):
                txt2_adj = v[0]
                txt2_prop = self.adjKB[txt2_adj]
                break

        if txt2_prop is None:
            for v in txt2_tags[::-1]:
                if self.tagProcessor.isVerb(v):
                    txt2_v = v[0]
                    txt2_prop = self.verbKB[txt1_v]
                    break
        return [txt1_positive, txt2_positive, txt1_prop, txt2_prop]

class RandomForestsSolver(SolverBaseClass):
    def train(self, questionList, n_est = 6):
        featuresList = []
        targetList = []
        for q in questionList:
            features = self.extractFeatures(q)[2:]
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
        features = self.extractFeatures(question)[2:]
        features = self.fixFeature(features)
        if self.listContainsNone(features):
            print features
            print "feature fail"
            return 'N/A'
        else:
            ans = self.clf.predict([features])[0]
            return self.returnAns(ans, features[0], features[1])
class GussianSolver(SolverBaseClass):
    def train(self, questionList):
        featuresList = []
        targetList = []
        for q in questionList:
            features = self.extractFeatures(q)[2:]
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
        features = self.extractFeatures(question)[2:]
        features = self.fixFeature(features)
        if self.listContainsNone(features):
            print features
            print "feature fail"
            return 'N/A'
        else:
            ans = self.clf.predict([features])[0]
            return self.returnAns(ans, features[0], features[1])

class SVMSolver(SolverBaseClass):
    def train(self, questionList):
        featuresList = []
        targetList = []
        for q in questionList:
            # print q
            features = self.extractFeatures(q)[2:]
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
        features = self.extractFeatures(question)[2:]
        features = self.fixFeature(features)
        if self.listContainsNone(features):
            print features
            print "feature fail"
            return 'N/A'
        else:
            ans = self.clf.predict([features])[0]
            return self.returnAns(ans, features[0], features[1])

class PositiveNegativeSolver(SolverBaseClass):
    def solver(self, question):
        answer_order = self.mapAB(question)
        txt1_tags = self.sentenceParser.makeTags(question[0]['txt1'])
        txt1_positive = 1
        if self.tagProcessor.isNegativeFromList(txt1_tags):
            txt1_positive = -1

        txt2_tags = self.sentenceParser.makeTags(question[0]['pron'] + " " + question[0]['txt2'])
        txt2_positive = 1
        if self.tagProcessor.isNegativeFromList(txt2_tags):
            txt2_positive = -1

        txt1_v = ''
        txt1_prop = None
        for v in txt1_tags[::-1]:
            if self.tagProcessor.isVerb(v):
                txt1_v = v
                txt1_prop = self.vbParser.parserV(txt1_v[0])
                break

        txt2_v = ''
        txt2_adj = ''
        txt2_prop = None
        for v in txt2_tags[::-1]:
            if self.tagProcessor.isAdj(v):
                txt2_adj = v
                txt2_prop = self.vbParser.parserAdj(txt2_adj[0])
                break

        if txt2_prop is None:
            for v in txt2_tags[::-1]:
                if self.tagProcessor.isVerb(v):
                    txt2_v = v
                    txt2_prop = self.vbParser.parserV(txt2_v[0])
                    break

        print txt1_positive, txt2_positive
        print txt1_prop
        print txt2_prop

        if txt1_prop is None or txt2_prop is None:
            return 'n/a'
        if txt1_positive * txt2_positive * txt1_prop['prop'] * txt2_prop['prop'] > 0:
            return 'a'

        return 'b'


class RandomSolver(SolverBaseClass):
    def solver(self, question):
        if randint(0, 1) == 0:
            return 'a'
        else:
            return 'b'
