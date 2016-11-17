from random import randint
import string

from input_parse import InputParser
from common import TagProcessor
from nltk_helper import SentenceParser
from kb import WordParser

from nltk.corpus import wordnet

#if a word is not in the knowledge base, we calculate the similarity of this word with other words in KB
#Intput is the unknownword and a word in KB;
class WordFeature:
    def getFeature(UnkownWord, KBWord):
        syns1 = wordnet.synsets(UnkownWord)
        syns2 = wordnet.synsets(KBWord)
        sim_value
        for lemma1 in syns1:
            for lemma2 in syns2:
                sim_value += lemma1.wup_similarity(lemma2)
        
        sim_value = sim_value/(syns1.size() * syns2.size())
        return sim_value

    #def getValue:
    
class SolverBaseClass:
    def __init__(self):
        self.tagProcessor = TagProcessor()
        self.sentenceParser = SentenceParser()
        self.vbParser = WordParser()

    def solver(self, question):
        return 'a'


class PositiveNegativeSolver(SolverBaseClass):
    def mapAB(self, question):
        # question[0]['txt1'] = string.replace(question[0]['txt1'], question[2][0], ' A ')
        # question[0]['txt1'] = string.replace(question[0]['txt1'], question[2][1], ' B ')
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
