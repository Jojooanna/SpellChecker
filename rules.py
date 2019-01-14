from model import *
import timeit
import codecs
import io
from sqlalchemy import func
# -*- coding: utf-8 -*-

def connectToDatabase():
    """
    Connect to our SQLite database and return a Session object
    """
    engine = create_engine('postgresql://postgres:jojo123@localhost:5432/spellcheck')
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

session = connectToDatabase()

start = timeit.default_timer()

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
                        primary += "A"
                        secondary += "A"
                    elif (symbol == "I"):
                        primary += "A"
                        secondary += "A"
                    elif (symbol == "O"):
                        primary += "A"
                        secondary += "A"
                    elif (symbol == "U"):
                        primary += "A"
                        secondary += "A"
                    else:
                        continue
                    current += 1
                    continue
                elif (self.sub(word, current, 2, ["UA"])):
                    primary += ""
                    secondary += "W"
                    current += 2
                    continue
                elif (self.sub(word, current, 2, ["UE"])):
                    primary += ""
                    secondary += "W"
                    current += 2
                    continue
                elif (self.sub(word, current, 2, ["UI"])):
                    primary += ""
                    secondary += "W"
                    current += 2
                    continue
                elif (self.sub(word, current, 2, ["OA"])):
                    primary += ""
                    secondary += "W"
                    current += 2
                    continue
                elif (self.sub(word, current, 2, ["AU"])):
                    primary += ""
                    secondary += "W"
                    current += 2
                    continue
                elif (self.sub(word, current, 2, ["OU"])):
                    primary += ""
                    secondary += "W"
                    current += 2
                    continue
                elif (self.sub(word, current, 2, ["AO"])):
                    primary += ""
                    secondary += "W"
                    current += 2
                    continue
                elif (self.sub(word, current, 2, ["IA"])):
                    primary += ""
                    secondary += "Y"
                    current += 2
                    continue
                elif (self.sub(word, current, 2, ["IE"])):
                    primary += ""
                    secondary += "Y"
                    current += 2
                    continue
                elif (self.sub(word, current, 2, ["IO"])):
                    primary += ""
                    secondary += "Y"
                    current += 2
                    continue
                elif (self.sub(word, current, 2, ["IU"])):
                    primary += ""
                    secondary += "Y"
                    current += 2
                    continue
                elif (self.sub(word, current, 2, ["EA"])):
                    primary += ""
                    secondary += "Y"
                    current += 2
                    continue
                else:
                    current += 1
                continue

            elif (symbol == "B"):
                if (self.sub(word, current, 2, ["BB"])):
                    primary += "B"
                    secondary += "B"
                    current += 2
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
                if (self.sub(word, current, 2, ["CC"])):
                    primary += "C"
                    secondary += "K"
                    current += 2
                elif (self.sub(word, current, 2, ["CH"])):
                    primary += "TS"
                    secondary += "S"
                    current += 2
                    continue
                else:
                    primary += "C"
                    secondary += "K"
                    current += 1
                    continue

            elif (symbol == "D"):
                if (self.sub(word, current, 2, ["DD"])):
                    primary += "D"
                    secondary += "D"
                    current += 2
                elif (self.sub(word, current, 2, ["DY"])):
                    primary += "J"
                    secondary += "J"
                    current += 2
                else:
                    primary += "D"
                    secondary += "D"
                    current += 1
                continue
            elif (symbol == "F"):
                if (self.sub(word, current, 2, ["FF"])):
                    primary += "F"
                    secondary += "F"
                    current += 2
                else:
                    primary += "F"
                    secondary += "P"
                    current += 1
                continue

            elif (symbol == "G"):
                if(self.sub(word, current, 2, ["GG"])):
                    primary += "G"
                    secondary += "G"
                    current += 2
                else:
                    primary += "G"
                    secondary += "G"
                    current += 1
                continue
            elif (symbol == "H"):
                if ((current == 0 or self.isVowel(word, current - 1)) \
                            and self.isVowel(word, current + 1)):
                    primary += "H"
                    secondary += "J"
                    current += 1
                elif(self.sub(word,current, 2, ["HH"])):
                    primary += "H"
                    secondary += "J"
                    current +=2
                else:
                    primary += "H"
                    secondary += "J"
                    current += 1
                continue
            elif (symbol == "J"):
                if (self.sub(word, current, 2, ["JJ"])):
                    primary += "J"
                    secondary += "H"
                    current += 2
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
                    secondary += "K"
                    current += 2
                    continue
                elif (self.sub(word, current, 2, ["KY"])):
                    primary += "Q"
                    secondary += "Q"
                    current += 2
                    continue
                elif(self.sub(word, current, 2, ["KK"])):
                    primary+="Q"
                    secondary+="K"
                    current +=2
                    continue
                else:
                    primary += "Q"
                    secondary += "K"
                    current += 1
                    continue

            elif (symbol == "L"):
                if (self.sub(word, current, 2, ["LL"])):
                    primary += "L"
                    secondary += "L"
                    current += 2
                elif ((self.sub(word, current + 1, 1, ["LY"])) or (self.sub(word, current + 1, 1, ["Y"]))):
                    primary += "L"
                    secondary += "L"
                    current += 2
                    continue
                else:
                    primary += "L"
                    secondary += "L"
                    current += 1
                    continue

            elif (symbol == "M"):
                if (self.sub(word, current, 2, ["MM"])):
                    primary += "M"
                    secondary += "M"
                    current += 2
                else:
                    primary += "M"
                    secondary += "M"
                    current += 1
                continue


            elif (symbol == "N"):
                if (self.sub(word, current, 2, ["NN"])):
                    primary += "N"
                    secondary += "N"
                    current += 2
                else:
                    primary += "N"
                    secondary += "N"
                    current += 1
                continue

            #what if ichange lang natong NG to any ascii symbol para ma-return ang primary ug secondary
            elif (symbol == "NG"):
                if (self.sub(word, current + 1, 2, ["NG"])):
                    current += 2
                else:
                    primary += "NG"
                    secondary += "NG"
                    current += 2
                continue

            elif (symbol == "P"):
                # if (self.sub(word, current + 1, 1, ["H"])):
                #     current += 2
                #     primary += "F"
                #     secondary += "F"
                #     continue
                if (self.sub(word, current, 2, ["PP"])):
                    primary += "P"
                    secondary += "P"
                    current += 1

                elif (self.sub(word, current+1, 1, ["P","N"])):
                    primary += "P"
                    secondary += "F"
                    current += 1
                else:
                    primary += "P"
                    secondary += "F"
                    current += 1
                continue

            elif (symbol == "Q"):
                if (self.sub(word, current, 2, ["QQ"])):
                    primary += "Q"
                    secondary += "K"
                    current += 2
                else:
                    primary += "Q"
                    secondary += "K"
                    current += 1
                continue
            elif (symbol == "R"):
                if (self.sub(word, current, 2, ["RR"])):
                    primary += "R"
                    secondary += "R"
                    current += 2
                else:
                    primary += "R"
                    secondary += "R"
                    current += 1
                continue

            elif (symbol == "S"):
                if (current == 0 and self.sub(word, current, 5, ["SUGAR"])):
                    primary += "X"
                    secondary += "S"
                    current += 1
                    continue

                if (self.sub(word, current, 2, ["SS"])):
                    primary += "S"
                    secondary += "S"
                    current += 2
                    continue
                else:
                    primary += "S"
                    secondary += "S"
                    current +=1
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
                if (self.sub(word, current, 2, ["TT"])):
                    primary += "T"
                    secondary += "T"
                    current += 2
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
                elif (self.sub(word, current, 2, ["VV"])):
                    current +=2
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
                elif(self.sub(word, current, 2, ["WW"])):
                    primary += "W"
                    secondary += "W"
                    current +=2
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
                if (self.sub(word, current+1, 1, ["S"])):
                    primary += "Z"
                    secondary += "S"
                    current += 1
                    continue
                elif (self.sub(word, current, 2, ['ZZ'])):
                    primary += "Z"
                    secondary += "S"
                    current += 2
                else:
                    primary += "Z"
                    secondary += "S"
                    current += 1
                continue
            else:
                current += 1

        primary = primary[0:8]
        secondary = secondary[0:8]
        return primary, secondary

x = meta()


# path = 'new dictionary.txt'
# with io.open(path) as fp:
#   line = fp.read().splitlines()
#   for i in line:
    # data = session.query(inputWords).filter(inputWords.word == i).first()
    # if data is None:
    #     data1 = inputWords(word=i)
    #     session.add(data1)
    #     session.commit()
    # else:
    #     print ("Word already exists.")
        
# for i in dictionary:
#     print i

# Adds words to DB
def OnConvert(i):
    primary, secondary = x.process(i)

    if primary == secondary:
        # print("{}: {}".format(primary, i))
        data = session.query(Words).filter(Words.code == primary).first()
        if data is None:
            dict = Words(code=primary, words=[i])
            session.add(dict)
            session.commit()
        else:
            if i in data.words:
                pass
            else:
                data.words = list(data.words)
                data.words.append(i)
                session.merge(data)
                session.commit()
    else:
        dataPri = session.query(Words).filter(Words.code == primary).first()
        if dataPri is None:
            dict = Words(code=primary, words=[i])
            session.add(dict)
            session.commit()
        else:
            if i in dataPri.words:
                pass
            else:
                dataPri.words = list(dataPri.words)
                dataPri.words.append(i)
                session.merge(dataPri)
                session.commit()

        dataSec = session.query(Words).filter(Words.code == secondary).first()
        if dataSec is None:
            dict = Words(code=secondary, words=[i])
            session.add(dict)
            session.commit()
        else:
            if i in dataSec.words:
                pass
            else:
                dataSec.words = list(dataSec.words)
                dataSec.words.append(i)
                session.merge(dataSec)
                session.commit()

# Adding Words to Common DB
def OnConvertCommon(i):
    primary, secondary = x.process(i)

    if primary == secondary:
        # print("{}: {}".format(primary, i))
        data = session.query(Common).filter(Common.code == primary).first()
        if data is None:
            dict = Common(code=primary, words=[i])
            session.add(dict)
            session.commit()
        else:
            if i in data.words:
                pass
            else:
                data.words = list(data.words)
                data.words.append(i)
                session.merge(data)
                session.commit()
    else:
        dataPri = session.query(Common).filter(Common.code == primary).first()
        if dataPri is None:
            dict = Common(code=primary, words=[i])
            session.add(dict)
            session.commit()
        else:
            if i in dataPri.words:
                pass
            else:
                dataPri.words = list(dataPri.words)
                dataPri.words.append(i)
                session.merge(dataPri)
                session.commit()

        dataSec = session.query(Common).filter(Common.code == secondary).first()
        if dataSec is None:
            dict = Common(code=secondary, words=[i])
            session.add(dict)
            session.commit()
        else:
            if i in dataSec.words:
                pass
            else:
                dataSec.words = list(dataSec.words)
                dataSec.words.append(i)
                session.merge(dataSec)
                session.commit()