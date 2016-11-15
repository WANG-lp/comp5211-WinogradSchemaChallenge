class TagProcessor:
    VERBS = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
    NEGATION = ["n't", 'not']
    ADJECTIVE = ['JJ', 'JJR', 'JJS']
    DETERMINER = ['DT']

    def isDeter(self, tup):
        for d in self.DETERMINER:
            if tup[1] == d:
                return d
        return False

    def isVerb(self, tup):
        for v in self.VERBS:
            if tup[1] == v:
                return v
        return False

    def isAdj(self, tup):
        for a in self.ADJECTIVE:
            if tup[1] == a:
                return a
        return False

    def isNegativeFromList(self, list_t):
        for t in list_t:
            if self.isNegative(t):
                return True
        return False

    def isNegative(self, tup):
        if tup[1] == 'RB':
            for ne in self.NEGATION:
                if tup[0] == ne:
                    return True
        return False
