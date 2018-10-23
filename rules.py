from model import *
import timeit
import codecs
import io
# -*- coding: utf-8 -*-

def connectToDatabase():
    """
    Connect to our SQLite database and return a Session object
    """
    engine = create_engine("postgresql://postgres:mvjunetwo@localhost:5432/spell")
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

session = connectToDatabase()

class meta:
    length = 0

    # def __init__(self):
    #	print self.process("schmidt")

    def isSlavoGermanic(self, str):
        for each in ["W", "K", "CZ", "WZ"]:
            if (each in str):
                return 1;
        return 0;

    def isVowel(self, word, start):
        return self.sub(word, start, 1, ['A', 'E', 'I', 'O', 'U'])

    def sub(self, word, start, count, arr):
        if (start < 0 or start >= len(word)):
            return 0
        if (word[start:start + count] in arr):
            return 1
        return 0

    def process(self, word):
        primary, secondary = "", ""
        word = word.upper()
        self.length = len(word)
        current, last = 0, self.length - 1
        word += "    "

        if (word[0:2] in ['GN', 'KN', 'PN', 'WR', 'PS']):
            current += 1

        if (word[0] == 'X'):
            primary += "S"
            secondary += "S"
            current += 1

        while ((len(primary) < 8 or len(secondary) < 8) and current < self.length):
            symbol = word[current]

            if (symbol in ['A', 'E', 'I', 'O', 'U']):
                if (current == 0):
                    if (symbol == 'A'):
                        primary += "A"
                        secondary += "A"
                    elif (symbol == "E"):
                        primary += "E"
                        secondary += "I"
                    elif (symbol == "I"):
                        primary += "I"
                        secondary += "I"
                    elif (symbol == "O"):
                        primary += "O"
                        secondary += "O"
                    elif (symbol == "U"):
                        primary += "U"
                        secondary += "U"
                    else:
                        continue
                    current += 1
                    continue
                elif (self.sub(word, current, 2, ["UA"])):
                    primary += "W"
                    secondary += "W"
                    current += 2
                    continue
                elif (self.sub(word, current, 2, ["UE"])):
                    primary += "W"
                    secondary += "W"
                    current += 2
                    continue
                elif (self.sub(word, current, 2, ["UI"])):
                    primary += "W"
                    secondary += "W"
                    current += 2
                    continue
                elif (self.sub(word, current, 2, ["OA"])):
                    primary += "W"
                    secondary += "W"
                    current += 2
                    continue
                elif (self.sub(word, current, 2, ["AU"])):
                    primary += "W"
                    secondary += "W"
                    current += 2
                    continue
                elif (self.sub(word, current, 2, ["OU"])):
                    primary += "W"
                    secondary += "W"
                    current += 2
                    continue
                elif (self.sub(word, current, 2, ["AO"])):
                    primary += "W"
                    secondary += "W"
                    current += 2
                    continue
                elif (self.sub(word, current, 2, ["IA"])):
                    primary += "Y"
                    secondary += "Y"
                    current += 2
                    continue
                elif (self.sub(word, current, 2, ["IE"])):
                    primary += "Y"
                    secondary += "Y"
                    current += 2
                    continue
                elif (self.sub(word, current, 2, ["IO"])):
                    primary += "Y"
                    secondary += "Y"
                    current += 2
                    continue
                elif (self.sub(word, current, 2, ["IU"])):
                    primary += "Y"
                    secondary += "Y"
                    current += 2
                    continue
                elif (self.sub(word, current, 2, ["EA"])):
                    primary += "Y"
                    secondary += "Y"
                    current += 2
                    continue
                else:
                    current += 1
                continue

            elif (symbol == "B"):
                if (self.sub(word, current + 1, 1, ["B"])):
                    primary += "B"
                    secondary += "V"
                    current += 1

                else:
                    primary += "B"
                    secondary += "V"
                    current += 1
                continue
            elif (symbol == 'C'):
                #	italian 'chianti'
                # else(self.sub(word,current,4,["CHIA"])):
                # 	primary+="K"
                # 	secondary+="K"
                # 	current+=2
                # 	continue
                if (self.sub(word, current, 2, ["CH"])):
                    primary += "TS"
                    secondary += "S"
                    current += 2
                    continue
                else:
                    primary += "K"
                    secondary += "C"
                    current += 1
                    continue

            elif (symbol == "D"):
                if (self.sub(word, current, 2, ["DY"])):
                    primary += "J"
                    secondary += "J"
                    current += 2
                else:
                    primary += "D"
                    secondary += "D"
                    current += 1
                continue
            elif (symbol == "F"):
                if (self.sub(word, current + 1, 1, ["F"])):
                    current += 1
                else:
                    primary += "F"
                    secondary += "P"
                    current += 1
                continue

            elif (symbol == "G"):
                primary += "G"
                secondary += "G"
                if (self.sub(word, current + 1, 1, ["G"])):
                    current += 1
                else:
                    current += 1
                continue
            elif (symbol == "H"):
                if ((current == 0 or self.isVowel(word, current - 1)) \
                            and self.isVowel(word, current + 1)):
                    primary += "H"
                    secondary += "J"
                    current += 1
                else:
                    current += 1
                continue
            elif (symbol == "J"):
                if (self.sub(word, current, 1, ["J"])):
                    primary += "J"
                    secondary += "H"
                    current += 1
                    continue
                else:
                    current += 1
                    continue
            elif (symbol == "K"):
                if (self.sub(word, current, 2, ["KS"])):
                    primary += "X"
                    secondary += "X"
                    current += 2
                    continue
                elif (self.sub(word, current, 2, ["KW"])):
                    primary += "Q"
                    secondary += "Q"
                    current += 2
                    continue
                elif (self.sub(word, current, 2, ["KY"])):
                    primary += "Q"
                    secondary += "Q"
                    current += 2
                    continue
                else:
                    primary += "K"
                    secondary += "K"
                    current += 1
                    continue

            elif (symbol == "L"):
                if (self.sub(word, current + 1, 1, ["L"])):
                    current += 1
                else:
                    current += 1
                primary += "L"
                secondary += "L"
                continue
                if ((self.sub(word, current + 1, 1, ["LY"])) or (self.sub(word, current + 1, 1, ["Y"]))):
                    current += 2
                else:
                    current += 1
                primary += "L"
                secondary += "L"
                continue

            elif (symbol == "M"):
                if (self.sub(word, current + 1, 1, ["M"])):
                    current += 1
                else:
                    current += 1
                primary += "M"
                secondary += "M"
                continue

            elif (symbol == "N"):
                if (self.sub(word, current + 1, 1, ["N"])):
                    primary += "N"
                    secondary += "N"
                    current += 1
                else:
                    primary += "N"
                    secondary += "N"
                    current += 1
                continue

            elif (symbol == "NG"):
                if (self.sub(word, current + 1, 2, ["NG"])):
                    current += 2
                else:
                    primary += "NG"
                    secondary += "NG"
                    current += 2
                continue

            elif (symbol == "P"):
                if (self.sub(word, current + 1, 1, ["H"])):
                    current += 2
                    primary += "F"
                    secondary += "F"
                    continue

                if (self.sub(word, current + 1, 1, ["P", "F"])):
                    current += 2
                else:
                    current += 1

                primary += "P"
                secondary += "F"
                continue

            elif (symbol == "Q"):
                if (self.sub(word, current, 1, ["Q"])):
                    primary += "Q"
                    secondary += "Q"
                    current += 1
                else:
                    current += 1
                continue
            elif (symbol == "R"):
                if (self.sub(word, current, 1, ["R"])):
                    primary += "R"
                    secondary += "R"
                    current += 1
                else:
                    current += 1
                continue

            elif (symbol == "S"):
                if (current == 0 and self.sub(word, current, 5, ["SUGAR"])):
                    primary += "X"
                    secondary += "S"
                    current += 1
                    continue

                if (self.sub(word, current + 1, 1, ["Z"])):
                    primary += "S"
                    secondary += "X"
                    if (self.sub(word, current + 1, 1, ["Z"])):
                        current += 1
                    else:
                        current += 1
                    continue
                if (self.sub(word, current, 2, ["SC"])):
                    if (self.sub(word, current + 2, 1, ["H"])):
                        if (self.sub(word, current + 3, 2, ["OO", "ER", "EN", "UY", "ED", "EM"])):
                            if (self.sub(word, current + 3, 2, ["ER", "EN"])):
                                primary += "X"
                                secondary += "SK"
                            else:

                                primary += "SK"
                                secondary += "SK"
                            current += 2
                            continue
                else:
                    primary += "S"
                    secondary += "S"
                    current += 1
                continue

            elif (symbol == "T"):
                if (self.sub(word, current + 1, 1, ["T"])):
                    primary += "T"
                    secondary += "T"
                    current += 1
                elif (self.sub(word, current, 2, ["TS"])):
                    primary += "TS"
                    secondary += "S"
                    current += 2
                else:
                    primary += "T"
                    secondary += "T"
                    current += 1
                continue
            elif (symbol == "V"):
                if (self.sub(word, current + 1, 1, ["V"])):
                    current += 1
                else:
                    current += 1
                primary += "V"
                secondary += "B"
                continue

            elif (symbol == "W"):
                if (self.sub(word, current, 1, ["W"])):
                    primary += "W"
                    secondary += "W"
                    current += 1
                    continue
                else:
                    current += 1
                continue

            elif (symbol == "X"):
                if (self.sub(word, current + 1, 1, ["X"])):
                    primary += "X"
                    secondary += "X"
                    current += 1
                else:
                    current += 1
                continue

            elif (symbol == "Y"):
                if (self.sub(word, current, 1, ["Y"])):
                    primary += "Y"
                    secondary += "Y"
                    current += 1
                    continue
                else:
                    current += 1
                continue
            elif (symbol == "Z"):
                if (self.sub(word, current + 1, 1, ["S"])):
                    primary += "Z"
                    secondary += "S"
                    current += 1
                    continue
                if (self.sub(word, current + 1, 1, ['Z'])):
                    current += 1
                else:
                    current += 1
                continue
            else:
                current += 1

        primary = primary[0:8]
        secondary = secondary[0:8]
        return primary, secondary

x = meta()
# primary, secondary = x.process("nakakapagpabagabag")
# print ("Primary: ", primary)
# print ("Secondary: ", secondary)
#
# dugay kaayong runtime GRABE
# di na ma-save ug balik ang mga words nga naa na sa db

start = timeit.default_timer()

path = 'dictionarytest.txt'
with io.open(path) as fp:
    line = fp.read().splitlines()
    print line

    for i in line:
        primary, secondary = x.process(i)
        print primary
        print secondary
        if primary == secondary:
            #print("{}: {}".format(primary, i))
            data = session.query(Words).filter(Words.code == primary).first()
            if data is None:
                dict = Words(code=primary, words=[i])
                session.add(dict)
                session.commit()
            else:
                if i in data.words:
                    print ("prim",i)
                    # print "hi"
                    # if i == line.strip():
                    #     pass
                    # else:
                    #     data.words = list(data.words)
                    #     data.words.append(i)
                    #     session.merge(data)
                    #     session.commit()
        else:
            dataPri = session.query(Words).filter(Words.code == primary).first()
            if dataPri is None:
                dict = Words(code=primary, words=[i])
                session.add(dict)
                session.commit()
            else:
                if i in dataPri.words:
                    print ("priboth", i)
                    # if i == line.strip():
                    #     pass
                    # else:
                    #     dataPri.words = list(dataPri.words)
                    #     dataPri.words.append(line.strip())
                    #     session.merge(dataPri)
                    #     session.commit()

            dataSec = session.query(Words).filter(Words.code == secondary).first()
            if dataSec is None:
                dict = Words(code=secondary, words=[i])
                session.add(dict)
                session.commit()
            else:
                if i in dataSec.words:
                    print ("secboth", i)
                    # if i == line.strip():
                    #     pass
                    # else:
                    #     dataSec.words = list(dataSec.words)
                    #     dataSec.words.append(line.strip())
                    #     session.merge(dataSec)
                    #     session.commit()

stop = timeit.default_timer()

print('Time: ', stop - start)

# dict = {"hell": [1, 2, 3], "ej": [1, 2], "TSK": ['hello', 'world']}
# # How to use metaphone algorithm
# x = meta()
# # to produce primary and secondary hash just use the following
# word = raw_input('Enter a word: ')
#
# primary, secondary = x.process(word)
# print primary
# print secondary

# dictionary = open("dictionarytest.txt", "r")
#
# if dictionary.mode == 'r':
#     content = dictionary.read()
#
#     x = meta()
#
#     primary, secondary = x.process(content)
#     print (primary, content)
#     print (secondary, content)

# dict = {"HL": ['hala','halo', 'holo'], "JL": ['haja', 'hajo'], "TSK": ['hello', 'world'], "CHK":['choco', 'choko', 'chook']}
# # How to use metaphone algorithm
# x = meta()
# # to produce primary and secondary hash just use the following
# word = raw_input('Enter a word: ')
#
# primary, secondary = x.process(word)
# print primary
# print secondary

# if primary in dict.keys():
#     dict[primary].append(word)
#
# list_name = primary
# vars()[list_name] = []
# print dict[primary]
# print dict
# print dict["hell"]

# words = []
#
# for x in dict[primary]:
#     words.append(x)
#
# if dict[secondary]:
#     for y in dict[secondary]:
#         words.append(y)
#
# print words



# primary, secondary = x.process(raw_input('Enter a word: '))
# suggestions = session.query(Words).filter(Words.code == primary)
# words = []
#
# for x.words in suggestions:
#     words.append(x.words)
#
# print primary, secondary
# print words