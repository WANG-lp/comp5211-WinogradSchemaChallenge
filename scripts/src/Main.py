from input_parse import InputParser
from common import TagProcessor
from nltk_helper import SentenceParser
from kb import VerbParser
from solvers import RandomSolver, SolverBaseClass, PositiveNegativeSolver

if __name__ == "__main__":

    filename = "../../datasets/WSCollection.xml"
    inputParser = InputParser(filename)
    ques =  inputParser.parse()
    sentenceParser = SentenceParser()
    tagT = TagProcessor()
    vbParser = VerbParser()

    naiveSolver = SolverBaseClass()
    randomSolver = RandomSolver()
    pnSolver= PositiveNegativeSolver()

    total = 0
    correct = 0
    for q in ques:
        q = ques[3]
        print q[0]['txt1'],'#', q[0]['pron'],'#', q[0]['txt2']
        print q[1]['pron'] + q[1]['quote1'] + " "+ q[1]['quote2']
        ans = pnSolver.solver(q)

        total += 1
        print q[-1]
        if ans == q[-1]:
            print "correct!"
            correct += 1

        #print randomSolver.solver(q), q[-1]

        input = raw_input("press any key to continue.")
    print correct * 100.0 / total