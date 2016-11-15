import nltk

from nltk.tokenize import word_tokenize


class SentenceParser:
    def makeTags(self, sentence):
        text = word_tokenize(sentence)
        return nltk.pos_tag(text)

if __name__ == "__main__":
    sParser = SentenceParser()
    print sParser.makeTags("The city councilmen refused the demonstrators a permit because they feared violence.")
