import random
import logging
import sys

from input_parse import InputParser
from common import TagProcessor
from nltk_helper import SentenceParser
from kb import WordParser
from solvers import RandomSolver, SolverBaseClass, PositiveNegativeSolver, SVMSolver, RandomForestsSolver, GussianSolver, StandfordCorefSolver

def printC(c, total, msg):
    print msg, c , c*100.0/total


if __name__ == "__main__":

    logging.basicConfig(filename='solvers.log', level=logging.DEBUG)
    # root = logging.getLogger()
    # root.setLevel(logging.DEBUG)
    #
    # ch = logging.StreamHandler(sys.stdout)
    # ch.setLevel(logging.DEBUG)
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # ch.setFormatter(formatter)
    # root.addHandler(ch)

    filename = "../../datasets/WSCollection.xml"
    inputParser = InputParser(filename)
    ques =  inputParser.parse()
    sentenceParser = SentenceParser()
    tagT = TagProcessor()
    vbParser = WordParser()

    #naiveSolver = SolverBaseClass()
    #randomSolver = RandomSolver()
    pnSolver= PositiveNegativeSolver()
    svmSolver = SVMSolver()
    rftSolver = RandomForestsSolver()
    gussianSolver = GussianSolver()

    snlpSolver = StandfordCorefSolver("/Users/will/Workspace/stanford-corenlp-full-2016-10-31/")

    total = 0
    correct_pn = 0
    correct_svm = 0
    correct_rft = 0
    correct_guss = 0
    correct_snlp = 0

    #random.shuffle(ques)

    trainSetSize = 50
    svmSolver.train(ques[:trainSetSize])
    rftSolver.train(ques[:trainSetSize], n_est= 6)
    gussianSolver.train(ques[:trainSetSize])

    num = 0
    for q in ques:
        if num >= len(ques):
            break
        q = ques[num]
        print "#" * 6
        print "Question " + str(num) + ':'
        print q[0]['txt1'],'#', q[0]['pron'],'#', q[0]['txt2']
        print q[1]['pron'] + q[1]['quote1'] + " "+ q[1]['quote2']

        total += 1
        ans_snlp = snlpSolver.solver(q)
        if ans_snlp == q[-1]:
            print "Standford correct!"
            correct_snlp += 1

        ans_pn = pnSolver.solver(q)
        if ans_pn == q[-1]:
            print "PN correct!"
            correct_pn += 1


        ans_svm = svmSolver.solver(q)
        if ans_svm == q[-1]:
            print "svm correct!"
            correct_svm += 1

        ans_rft = rftSolver.solver(q)
        if ans_rft == q[-1]:
            print "rft correct!"
            correct_rft += 1

        ans_guss = gussianSolver.solver(q)
        if ans_guss == q[-1]:
            print "guss correct!"
            correct_guss += 1

        print ans_svm, ans_rft, ans_guss, q[-1]

        #print randomSolver.solver(q), q[-1]
        print "#" * 6
        input_t = raw_input("Input any number to continue:")
        #input_t = ''
        if len(input_t) == 0:
            num = num + 1
        else:
            num = int(input)


    printC(correct_pn, total, "PN:")
    printC(correct_svm, total, "svm:")
    printC(correct_guss, total, "gussian:")
    printC(correct_rft, total, "randomForestTree:")
    printC(correct_snlp, total, "Standford Nlp:")