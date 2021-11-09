import re
from Porter_Stemmer_Python import PorterStemmer


def partOne(stopperFile, paragraphFile):
    porterstemmer = PorterStemmer()
    htmlRex = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    stemmed = []
    finalStem = []
    featureVec = []
    with open(stopperFile) as s:
        stopWords = [x.strip('\n') for x in s]
    with open(paragraphFile) as f:
        for line in f:
            if line.isspace() == False:
                line = re.sub(htmlRex, ' ', line)
                line = re.sub('\s+', ' ', line)
                line = re.sub('^\s', '', line)
                line = re.sub('[^A-Za-z ]', '', line)
                line = line.lower()
                for word in line.split():
                    if word not in stopWords:
                        stemmed.append(porterstemmer.stem(
                            word, 0, len(word)-1))
                finalStem.append(stemmed)
                for word in stemmed:
                    if word not in featureVec:
                        featureVec.append(word)
            # getMostFrequent(stemmed)
            stemmed = []
    # print(finalStem)
    generateTDM(featureVec, finalStem)


def getMostFrequent(stemmed):
    mostFreq = {}

    for elem in stemmed:
        if elem in mostFreq:
            mostFreq[elem] += 1
        else:
            mostFreq[elem] = 1
    mostFreq = {k: v for k, v in mostFreq.items() if v != 1}

    # print("Frequent Repetitive words: ", mostFreq, '\n')


def generateTDM(featureVec, stemmed):
    print(featureVec)
    r = 0
    height = len(stemmed)
    width = len(featureVec)
    TDM = [[0 for x in range(width)] for y in range(height)]
    # print(stemmed)
    for para in stemmed:
        for word in para:
            if word in featureVec:
                j = featureVec.index(word)
                TDM[r][j] += 1
        r += 1
    tdm = open("tdm.csv", "w")
    colA = "Keyword Set,"
    for word in featureVec:
        colA = colA + word + ','
    tdm.write(colA + '\n')
    i = 0
    for x in stemmed:
        paraRow = "Paragraph " + str(i+1)
        c = 0
        for word in featureVec:
            paraRow = paraRow + ',' + str(TDM[i][c])
            c += 1
        i += 1
        tdm.write(paraRow + '\n')
    tdm.close()


stopperFile = "Project4_stop_words.txt"
paragraphFile = "Project4_paragraphs.txt"
partOne(stopperFile, paragraphFile)
