import nltk, os, sys

from nltk.tokenize import word_tokenize


def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0])) + "/"


nltk.data.path.append(get_script_path() + "../../nltk_data")

class SentenceParser:
    def makeTags(self, sentence):
        text = word_tokenize(sentence)
        return nltk.pos_tag(text)

if __name__ == "__main__":
    sParser = SentenceParser()
    print sParser.makeTags("The city councilmen refused the demonstrators a permit because they feared violence.")
