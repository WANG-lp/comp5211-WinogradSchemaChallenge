from xml.dom import minidom

from common import TagProcessor
from nltk_helper import SentenceParser

class InputParser:
    def __init__(self, filename):
        self.xmldoc = minidom.parse(filename)
        self.tagProcessor = TagProcessor()
        self.sentenceParser = SentenceParser()

    def parse(self):
        schemas = self.xmldoc.getElementsByTagName('schema')
        return self.toStruct(schemas)

    def getStruct(self, s):
        text = {}
        all_t = s.getElementsByTagName('text')
        text['txt1'] = all_t[0].getElementsByTagName('txt1')[0].firstChild.data.strip().lower()
        text['pron'] = all_t[0].getElementsByTagName('pron')[0].firstChild.data.strip().lower()
        text['txt2'] = all_t[0].getElementsByTagName('txt2')[0].firstChild.data.strip().lower()
        quote = {}
        quote_a = s.getElementsByTagName('quote')
        q1_c = quote_a[0].getElementsByTagName('quote1')
        if len(q1_c) > 0 and q1_c[0].hasChildNodes():
            quote['quote1'] = q1_c[0].firstChild.data.strip().lower()
        else:
            quote['quote1'] = ''

        q2_c = quote_a[0].getElementsByTagName('quote2')
        if len(q2_c) > 0 and q2_c[0].hasChildNodes():
            quote['quote2'] = q2_c[0].firstChild.data.strip().lower()
        else:
            quote['quote2'] = ''
        p_c = quote_a[0].getElementsByTagName('pron')
        if len(p_c) > 0 and p_c[0].hasChildNodes():
            quote['pron'] = p_c[0].firstChild.data.strip().lower()
        else:
            quote['pron'] = ''

        answers = []
        ans_list = s.getElementsByTagName('answers')[0].getElementsByTagName('answer')
        for ans in ans_list:
            a1 = ans.firstChild.data.strip().lower()
            tag1 = self.sentenceParser.makeTags(a1)
            a1 = ""
            for t in tag1:
                if not self.tagProcessor.isDeter(t):
                    a1 += " " + t[0]
            answers.append(a1.strip())

        correct_ans = None
        c_ans = s.getElementsByTagName('correctAnswer')
        if len(c_ans) > 0:
            correct_ans = c_ans[0].firstChild.data.split('.')[0].strip().lower()
        return [text, quote, answers, correct_ans]

    def toStruct(self, schemas):
        questions = []
        for s in schemas:
            questions.append(self.getStruct(s))
        return questions
