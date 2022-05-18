class RgxSSR(object):
    def __init__(self, sSequence, iMinMotif=2, iMaxMotif=6, iRepeats=5):

        assert iMinMotif >= 2
        self.regex = r'(.{%s,%s}?)(\1){%s,}' \
                     % (iMinMotif, iMaxMotif, iRepeats - 1)
        pattern = re.compile(self.regex)  
        liFindAll = pattern.findall(sSequence)
        liSplit = pattern.split(sSequence)
        liGroup = self.__ListGroup_li(pattern, sSequence) 
        liFlank = self.__ListFlank_li(liSplit, liGroup) 
        self.markedUpList = self.__GetMarkedUp_li(liFlank, liGroup)

    def __ListGroup_li(self, pattern, sSequence):
        liTemp = []
        for eachSSR in pattern.finditer(sSequence):
            liTemp.append(eachSSR.group())
        return liTemp

    def __ListFlank_li(self, liSplit, liGroup):
        return [liSplit[i] for i in [x * 3 for x in range(len(liGroup) + 1)]]

    def __GetMarkedUp_li(self, liFlank, liGroup):
        liMarkedUp = []
        sTemp = ''
        for i in range(len(liGroup)):
            if len(set(liGroup[i])) == 1:
                sTemp += liFlank[i] + liGroup[i]
            else:
                liMarkedUp.append(sTemp + liFlank[i])
                liMarkedUp.append(liGroup[i])
                sTemp = ''
        liMarkedUp.append(liFlank[-1])
        return liMarkedUp

    def CountSSR(self):
        return (len(self.markedUpList) - 1) / 2

    def ListSSR(self):
        li = self.markedUpList
        return [li[i] for i in [j * 2 + 1 for j in range(int((len(li) - 1) / 2))]]

    def ListMotif(self):
        liSSR = self.ListSSR()
        liMotif = []
        for eachSSR in liSSR:
            p = re.compile(self.regex)
            liMotif.append(p.findall(eachSSR)[0][0])
        return liMotif

    def GetLeft(self, i):
        li = self.markedUpList
        assert i <= (len(li) - 1) / 2
        return li[(i - 1) * 2]

    def GetRight(self, i):
        li = self.markedUpList
        assert i <= (len(li) - 1) / 2
        return li[i * 2]

    def GetPosition(self, i):
        iEle = i * 2 - 1
        iStart = len(''.join(self.markedUpList[:iEle])) + 1
        iEnd = iStart + len(self.markedUpList[iEle]) - 1
        return (iStart, iEnd)
