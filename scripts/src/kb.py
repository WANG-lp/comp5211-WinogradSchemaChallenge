import csv


class KB:
    verbKB = {}
    adjKB = {}

    def __init__(self, kb_dir="../KB/"):
        with open(kb_dir + "verb_list.txt") as f:
            spamreader = csv.reader(f, delimiter=' ')
            for row in spamreader:
                self.verbKB[row[0]] = float(row[1])
        with open(kb_dir + "adj_list.txt") as f:
            spamreader = csv.reader(f, delimiter=' ')
            for row in spamreader:
                self.adjKB[row[0]] = float(row[1])

    def getVerbKB(self):
        return self.verbKB

    def getAdjKB(self):
        return self.adjKB


class WordParser:
    verbSet = []
    adjSet = []

    def __init__(self, kb_dir="../KB/"):
        with open(kb_dir + 'verbs.csv', 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar='#')
            for row in spamreader:
                verb = row[0].split(",")
                gerund = row[1].split(",")
                past = row[2].split(",")
                participle = row[3].split(",")
                prop = int(row[4])
                self.verbSet.append({'verb': verb,
                                     'gerund': gerund,
                                     'past': past,
                                     'participle': participle,
                                     'prop': prop, })

        with open(kb_dir + 'adjs.csv', 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar='#')
            for row in spamreader:
                adj = row[0].split(",")
                adjer = row[1].split(",")
                adjest = row[2].split(",")
                prop = int(row[3])
                self.adjSet.append({'adj': adj,
                                    'adjer': adjer,
                                    'adjest': adjest,
                                    'prop': prop, })

    def parserAdj(self, string):
        for l in self.adjSet:
            for a in l['adj']:
                if string == a:
                    return {'string': a,
                            'prop': l['prop']}

    def parserV(self, string):
        isVerb = False
        isGerund = False
        isPast = False
        isParticiple = False
        prop = 1;

        isFound = False

        if not isFound:
            for l in self.verbSet:
                for v in l['verb']:
                    if string == v:
                        prop = l['prop']
                        isVerb = True
                        isFound = True
            if not isFound:
                for l in self.verbSet:
                    for v in l['gerund']:
                        if string == v:
                            prop = l['prop']
                            isGerund = True
                            isFound = True
            if not isFound:
                for v in l['past']:
                    for l in self.verbSet:
                        if string == v:
                            prop = l['prop']
                            isPast = True
                            isFound = True
            if not isFound:
                for l in self.verbSet:
                    for v in l['participle']:
                        if string == v:
                            prop = l['prop']
                            isParticiple = True
                            isFound = True

        if isFound:
            return {'string': string,
                    'isVerb': isVerb,
                    'isGerund': isGerund,
                    'isPast': isPast,
                    'isParticiple': isParticiple,
                    'prop': prop
                    }
        else:
            print "Word:'" + string + "' was not found in the knowledge database."
            return None


if __name__ == "__main__":
    vParser = WordParser()
    print vParser.verbSet
