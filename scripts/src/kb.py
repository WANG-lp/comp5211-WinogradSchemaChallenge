import csv


class VerbParser:
    verbSet = []
    adjSet = []
    def __init__(self):
        with open('../KB/verbs.csv', 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar='#')
            for row in spamreader:
                verb = row[0].split(",")
                gerund = row[1].split(",")
                past = row[2].split(",")
                participle = row[3].split(",")
                prop = int(row[4])
                self.verbSet.append({'verb': verb,
                                     'gerund':gerund,
                                     'past': past,
                                     'participle': participle,
                                     'prop': prop, })

        with open('../KB/adjs.csv', 'rb') as csvfile:
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
                    return {'string':a,
                            'prop':l['prop']}

    def parserV(self, string):
        for l in self.verbSet:
            for v in l['verb']:
                if string == v:
                    return {'isVerb': True,
                            'gerund':False,
                            'prop': l['prop'],
                            'isPast': False,
                            'isParticiple': False,
                            'string':v,
                            }
            for v in l['gerund']:
                if string == v:
                    return {'isVerb': False,
                            'gerund':True,
                            'prop': l['prop'],
                            'isPast': False,
                            'isParticiple': False,
                            'string': v,
                            }
            for v in l['past']:
                if string == v:
                    return {'isVerb': False,
                            'gerund': False,
                            'prop': l['prop'],
                            'isPast': True,
                            'isParticiple': False,
                            'string': v,
                            }
            for v in l['participle']:
                if string == v:
                    return {'isVerb': False,
                            'gerund': False,
                            'prop': l['prop'],
                            'isPast': False,
                            'isParticiple': True,
                            'string': v,
                            }
        print "Word:'" + string + "' was not found in the knowledge database."
        return None

if __name__ == "__main__":
    vParser = VerbParser()
    print vParser.verbSet
