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

    def returnAns(self, ans):
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

        if txt1_prop  is None:
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
