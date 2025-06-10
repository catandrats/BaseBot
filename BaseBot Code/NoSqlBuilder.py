import json
import math
import statistics
def convertListReason2String(list):#Converts list to string for display purposes
    returnstring = '['
    lenght = len(list)
    currentindex = 0
    exitcondition = lenght - 1
    while currentindex < lenght:
        if currentindex < exitcondition:
            returnstring = returnstring + str(list[currentindex]) + ', '
        else:
            returnstring = returnstring + str(list[currentindex]) + ']'
        currentindex = currentindex + 1
    return returnstring
#Filters out duplicate nodes
def filterDuplicateNodes(nodelist):#nodelist is to be a list of lists decribing sequences
    mappingdictionary = dict()
    currentnodelistindex = 0
    notincludedlists = []
    for list in nodelist:
        #print('list')
        #print(list)
        mappingdictionary[currentnodelistindex] = dict()
        currentindex = 0
        firstletterassigned = False
        for x in list:
            if '#' not in x and currentindex == 0 and firstletterassigned == False:
                mappingdictionary[currentnodelistindex][currentindex] = x
                firstletterassigned = True
            elif len(x) > 3:
                splitthis = x.split('#')
                currentindex = currentindex + int(splitthis[1])
                mappingdictionary[currentnodelistindex][currentindex] = splitthis[0]
            else:
                notincludedlists.append(list)
                mappingdictionary.pop(currentnodelistindex)

                #print(currentnodelistindex)
                break
        #print('notincluded')
        #print(notincludedlists)
        currentnodelistindex = currentnodelistindex + 1
    dictionaryofsequences = dict()
    for integer in mappingdictionary:
        currentarray = []
        for ind in mappingdictionary[integer]:
            currentarray.append(ind)
        orderedarray = []
        print('currentarray')
        print(currentarray)
        while len(currentarray) > 0:
            currentmin = min(currentarray)
            orderedarray.append(currentmin)
            currentarray.remove(currentmin)
        #constructuseablelist
        print(orderedarray)
        useablelist = []
        previousinx = 0
        for m in orderedarray:
            if m == orderedarray[0]:
                previousinx = m
                character = mappingdictionary[integer][m]
                useablelist.append(character)
            elif m != orderedarray[0]:
                distance = m - previousinx
                previousinx = m
                character = mappingdictionary[integer][m]
                strnew = character + '#+' + str(distance)
                useablelist.append(strnew)
        stringifiedlist = convertListReason2String(useablelist)
        if stringifiedlist not in dictionaryofsequences:
            dictionaryofsequences[stringifiedlist] = useablelist
    returnlists = []
    for x in dictionaryofsequences:
        returnlists.append(dictionaryofsequences[x])
    for y in notincludedlists:
        returnlists.append(y)
    print(mappingdictionary)
    return returnlists
def findThickNodes(database):
    currenttrunks = []
    entries = 0
    selfworkingcharacters = []
    for id in database:
        if database[id]['outcome'] == 'yes':
            if len(selfworkingcharacters) == 0:
                for index in database[id]['string']:
                    if database[id]['string'][index] not in selfworkingcharacters:
                        selfworkingcharacters.append(database[id]['string'][index])
            else:
                charlist = []
                for index in database[id]['string']:
                    if database[id]['string'][index] not in charlist:
                        charlist.append(database[id]['string'][index])
                #print(charlist)
                duplicatelist = selfworkingcharacters
                for char in duplicatelist:
                    #print(char)
                    if char not in charlist:
                        #print(char)
                        selfworkingcharacters.remove(char)
                #print("working")
                #print(selfworkingcharacters)
                for char in selfworkingcharacters:#repeating this seems to get rid of a bug
                    if char not in charlist:
                        selfworkingcharacters.remove(char)
    #for x in selfworkingcharacters:
    #    print(x)
    return selfworkingcharacters
class buildsecoundarytree:
    def __init__(self, conditions, database, parententropy):# Edit this to account for the workingcharacters attribute
        yescount = 0
        self.bestmatches = []
        for id in database:
            if database[id]['outcome'] == 'yes':#count yes cases
                yescount = yescount + 1
        Obj = godClassicallyHateDinos(conditions, database)
        conEntropy = calculateEntropy(Obj.returndictionary)
        currentterminals = secondaryTreeTerminalconditions()#used to remember current terminalnodes
        thickets = findThickNodes(database)
        currentterminals.addworkingcharacters(thickets)
        tree = NodeCharacterData(database, conEntropy, conditions, [], currentterminals)
        for yes in currentterminals.terminalnodes.terminalyes:
            searchresults = godClassicallyHateDinos(yes, database)
            resultingyeses = searchresults.returndictionary['yes']
            #calculateEntropy(searchresult.returndictionary)
            if resultingyeses == yescount:
                self.bestmatches.append(yes)
        if len(self.bestmatches) == 0:
            if len(conditions[-1]) == 3:
                spacebranchterminals = secondaryTreeTerminalconditions()
                spacebranchterminals.addworkingcharacters(thickets)
                distancedictionary = fencespacings(database, conditions, conEntropy, currentterminals)
                ordersplittree = orderspliting(database, conditions, distancedictionary, spacebranchterminals)
                for yes in spacebranchterminals.terminalnodes.terminalyes:
                    results = godClassicallyHateDinos(yes, database)
                    resultyeses = results.returndictionary['yes']
                    if resultyeses == yescount:
                        self.bestmatches.append(yes)
                tree = ordersplittree
        self.tree = tree
        self.bestmatches = filterDuplicateNodes(self.bestmatches)
        self.bestmatchresult = str(self.bestmatches)
        self.yesnodes = currentterminals.terminalnodes.terminalyes


def branchStripper(treeLayer, yesids):#performs pruning before tree builder continues
    newnodelist = []
    charactercoverage = dict()
    nodelist = []
    for mem in treeLayer:
        nodelist.append(mem)
        charactercoverage[mem] = dict()
        charactercoverage[mem]['yesids'] = []
        for id in treeLayer[mem]['ids']:
            if id in yesids:
                charactercoverage[mem]['yesids'].append(id)
    coverageranking = 0
    maxrankcoverage = len(treeLayer)
    rankdictionary = dict()
    while coverageranking < maxrankcoverage:
        coverageranking = coverageranking + 1
        currentmax = 0
        currentmaxcharacter = ''
        for mem in nodelist:
            if len(charactercoverage[mem]['yesids']) > currentmax:
                currentmax = len(charactercoverage[mem]['yesids'])
                currentmaxcharacter = mem
        nodelist.remove(currentmaxcharacter)
        charactercoverage[currentmaxcharacter]['rank'] = coverageranking
        rankdictionary[coverageranking] = currentmaxcharacter
    cycleranks = 0
    coveredyeses = []
    characterstouse = []
    returncharacters = []
    returndictionary = dict()
    usedranks = dict()
    while cycleranks < len(rankdictionary):
        cycleranks = cycleranks + 1
        currentyeses = charactercoverage[rankdictionary[cycleranks]]['yesids']
        usedranks[cycleranks] = currentyeses
        newyeses = []
        addcharacterstatus = False
        for yes in currentyeses:
            if yes not in coveredyeses:
                coveredyeses.append(yes)
                newyeses.append(yes)
        if len(newyeses) > 0:
            addcharacterstatus = True
        if addcharacterstatus == True:
            returncharacters.append(rankdictionary[cycleranks])
        if len(coveredyeses) == len(yesids):
            break
    for char in returncharacters:
        returndictionary[char] = treeLayer[char]
    return returndictionary
class currentterminalconditions:
    def __init__(self):
        self.terminalno = []
        self.terminalyes = []
    def addTerminalYes(self, list):
        self.terminalyes.append(list)
    def addTerminalNo(self, list):
        self.terminalno.append(list)
    def addworkingcharacters(self, list):
        self.workingcharacters = list
class secondaryTreeTerminalconditions: # be sure that the object scheme works fine for use of NodeCharacterData with secondary tree obj
    def __init__(self):
        self.terminalnodes = currentterminalconditions()
    def addworkingcharacters(self, list):
        self.workingcharacters = list
def calculateEntropyFromDatabase(database):
    diction = dict()
    diction['yes'] = 0
    diction['no'] = 0
    #print(database)
    for id in database:
        #print(database[id]['outcome'])
        if database[id]['outcome'] == 'yes':
            diction['yes'] = diction['yes'] + 1
        elif database[id]['outcome'] == 'no':
            diction['no'] = diction['no'] + 1
    returnval = calculateEntropy(diction)
    return returnval
def storejson(dictionary):
    with open('C:\\Users\\12564\\Desktop\\Secratariate\\testdatabase\\dictionary.json', 'w') as outfile:
        json.dump(dictionary, outfile)
class dictionarytestlogger:# For testing purposes ONLY!!!!!
    def __init__(self):
        self.diction = dict()
    def storedictionary(self, dic):
        dictionarylength = len(self.diction)
        currentindex = dictionarylength + 1
        self.diction[currentindex] = dic
    def nameddictionary(self, dictionary, name):
        self.diction[name] = dictionary
dictionarystorage = dictionarytestlogger()
class noIndexOrderedObject:#non-unique ordered fetch UPDATE: FINALLY WORKING!!!!!!!!!
    def __init__(self, condition, database):
        self.condition = condition
        self.database = database
        self.outcomedictionary = dict()
        self.casesincluded = []
        returndictionary = {}
        returndictionary["yes"] = 0
        returndictionary["no"] = 0
        countresultyes = 0
        countresultno = 0
        conditionlength = len(condition)
        databaselength =len(database)
        databasecontroll = databaselength + 1
        #print('databaselength ='+str(databaselength))
        #Start for loop over ids
        for id in database:
            #print('current id =' +str(id))
            stringdiction = database[id]["string"]
            #print(stringdiction)
            countmatches = 0
            whilelooplistindexcounter = 0
            #Start for loop over "string" index
            for index in database[id]["string"]:
                #print(index)
                #Start while loop
                while whilelooplistindexcounter < conditionlength:
                    currentdetail = condition[whilelooplistindexcounter]
                    #print(currentdetail)
                    if currentdetail == database[id]["string"][index]:
                        whilelooplistindexcounter = whilelooplistindexcounter + 1
                        countmatches = countmatches + 1
                        break
                    else:
                        break
                #End while loop
            #End for loop over "string" index
            if countmatches == conditionlength:
                idresult = database[id]["outcome"]
                self.casesincluded.append(id)
                if idresult == "yes":
                    returndictionary["yes"] = returndictionary["yes"] + 1
                else:
                    returndictionary["no"] = returndictionary["no"] + 1
        #End for loop over ids
        self.outcomedictionary = returndictionary
    def CalculateGain(self, parentEntropy):
        subentropy = calculateEntropy(self.outcomedictionary)
        self.gain = parentEntropy - subentropy
class characterNodeGenerator:
    def __init__(self, database, cases, conditions, parententropy):
        self.casedatabase = dict()
        for case in cases:
            self.casedatabase[case] = database[case]
        subentropy = CalculateProjectEntropy(self.casedatabase)
        gain = parententropy - subentropy
        self.gain = gain
        self.nodeentropy = subentropy
class TreeBuild:
    def __init__(self, database):
        self.database = database
        self.workingcharacters = []
        for id in self.database:
            if self.database[id]['outcome'] == 'yes':
                if len(self.workingcharacters) == 0:
                    for index in self.database[id]['string']:
                        self.workingcharacters.append(self.database[id]['string'][index])
                else:
                    charlist = []
                    for index in self.database[id]['string']:
                        if self.database[id]['string'][index] not in charlist:
                            charlist.append(self.database[id]['string'][index])
                    for char in self.workingcharacters:
                        if char not in charlist:
                            self.workingcharacters.remove(char)

        Object = CalculateProjectEntropy(database)
        gaindictionary = dict()
        for mem in self.workingcharacters:
            gaindictionary[mem] = dict()
            currentlist = []
            currentlist.append(mem)
            result = godClassicallyHateDinos(currentlist, self.database)
            entropy = calculateEntropy(result.returndictionary)
            gaindictionary[mem]['gain'] = Object.entropy - entropy
        currentmaxgain = 0.0
        currentrank = 1
        rankedchars = []
        while currentrank <= len(self.workingcharacters):
            currentmaxgain = 0.0
            maxchar = ''
            for mem in gaindictionary:
                print('mem')
                print(mem)
                if gaindictionary[mem]['gain'] <= 0.0 and currentmaxgain == 0.0 and mem not in rankedchars:
                    currentmaxgain = gaindictionary[mem]['gain']
                    maxchar = mem
                    rankedchars.append(mem)
                elif gaindictionary[mem]['gain'] >= currentmaxgain and mem not in rankedchars:
                    currentmaxgain = gaindictionary[mem]['gain']
                    maxchar = mem
                    rankedchars.append(mem)
            if maxchar != '':
                gaindictionary[maxchar]['rank'] = currentrank
                if currentrank == 1:
                    self.fullcoveragetrunk = maxchar
            currentrank = currentrank + 1
        self.fullcoverrankgain = gaindictionary
        self.terminalnodes = currentterminalconditions()
        self.projectEntropy = Object.entropy
        self.totaloutcomes = Object.statistics
        self.yesoutcomes = []
        self.idlist = []
        self.buildfirstlayer()
    def buildfirstlayer(self):
        dictionary = dict()

        self.decisiontree = dict()
        self.characterlist = dict()
        yescount = 0 # count yes for later
        yesids = []
        for id in self.database:
            self.idlist.append(id)
            if self.database[id]["outcome"] == "yes":
                if id not in yesids:
                    self.yesoutcomes.append(id)
                    yesids.append(id)
                yescount = yescount + 1
            #print(self.database)
            for char in self.database[id]["string"]:
                if self.database[id]["string"][char] not in self.characterlist:
                    #print(char)
                    subdictionary = dict()
                    subdictionary["conditions"] = []
                    subdictionary["conditions"].append(str(self.database[id]["string"][char]))
                    subdictionary["firstindex"] = dict()
                    subdictionary["firstindex"][id] = char
                    #subdictionary["mode"] = 0.0
                    #subdictionary["harmonicmean"] = 0.0
                    subdictionary["median"] = 0.0
                    subdictionary["samplestd"] = 0.0
                    subdictionary["mean"] = char
                    subdictionary["total"] = 1
                    subdictionary["indexes"] = []
                    subdictionary["ids"] = []
                    subdictionary["yescount"] = 0
                    if self.database[id]["outcome"] == 'yes':
                        subdictionary["yescount"] = subdictionary["yescount"] + 1
                    subdictionary["nocount"] = 0
                    if self.database[id]["outcome"] == "no":
                        subdictionary["nocount"] = subdictionary["nocount"] + 1
                    subdictionary["ids"].append(id)
                    subdictionary["branchtype"] = "character"
                    subdictionary["branches"] = dict()
                    #print(self.database[id]["string"][char])
                    self.characterlist[self.database[id]["string"][char]] = subdictionary
                    self.characterlist[self.database[id]["string"][char]]["indexes"].append(int(char))
                elif self.database[id]["string"][char] in self.characterlist:
                    if id not in self.characterlist[self.database[id]["string"][char]]["firstindex"]:
                        self.characterlist[self.database[id]["string"][char]]["firstindex"][id] = char
                    characterranktotal = float(self.characterlist[self.database[id]["string"][char]]["mean"])*float(self.characterlist[self.database[id]["string"][char]]["total"])#(current avg)*(# of occurances)
                    characterranktotal = characterranktotal + float(char)
                    if id not in self.characterlist[self.database[id]["string"][char]]["ids"]:
                        self.characterlist[self.database[id]["string"][char]]["ids"].append(id)
                        if self.database[id]["outcome"] == "yes":
                            self.characterlist[self.database[id]["string"][char]]["yescount"] = self.characterlist[self.database[id]["string"][char]]["yescount"] + 1
                        if self.database[id]["outcome"] == "no":
                            self.characterlist[self.database[id]["string"][char]]["nocount"] = self.characterlist[self.database[id]["string"][char]]["nocount"] + 1
                    self.characterlist[self.database[id]["string"][char]]["indexes"].append(int(char))
                    self.characterlist[self.database[id]["string"][char]]["mean"] = characterranktotal/(self.characterlist[self.database[id]["string"][char]]["total"] + 1.0)
                    self.characterlist[self.database[id]["string"][char]]["total"] = self.characterlist[self.database[id]["string"][char]]["total"] + 1
        firstlayerdict = dict()
        for character in self.characterlist:#Calculate character statistics
            sampledata = self.characterlist[character]["indexes"]
            #self.characterlist[character]["mode"] = statistics.mode(sampledata)
            #self.characterlist[character]["harmonicmean"] = statistics.harmonic_mean(sampledata)
            self.characterlist[character]["median"] = statistics.median(sampledata)
            if len(sampledata) == 1 or len(sampledata) == 0:
                self.characterlist[character]["samplestd"] = "invalid"
            else:
                self.characterlist[character]["samplestd"] = statistics.stdev(sampledata)
            self.characterlist[character]["mean"] = statistics.mean(sampledata)
        gaindictionary = dict()
        for x in self.characterlist:#Calculate character gain
            newlist = []
            newlist.append(x)
            currentyesno = dict()
            currentyesno["yes"] = self.characterlist[x]["yescount"]
            currentyesno["no"] = self.characterlist[x]["nocount"]
            gain = rawGainCalculation(self.projectEntropy, currentyesno)
            #gain = CalculateGain(self.projectEntropy, newlist, self.database)
            gaindictionary[x] = gain
            self.characterlist[x]["gain"] = gain
            self.characterlist[x]["entropy"] = calculateEntropy(currentyesno)
        #findnode of maxiumgain
        minindexcharacter = ""
        '''Start comment out'''


        #print(yescount)
        self.yesids = yesids
        yesids = self.yesoutcomes
        '''end comment out'''
        '''for id in yesids:
            if id not in coveredyescases:
                uncoveredyescases.append(id)
        '''
        covered = []
        uncoveredyescases = []
        #find covered yesids
        #for id in self.yesids:
        #    for m in self.decisiontree:
        #        print(m)
        #        if id in self.decisiontree[m]['ids']:
        #            covered.append(id)

        #print('covered')
        #print(covered)
        self.coveredyescases = covered
        #use covered yesids to identify uncovered yes ids
        for id in self.yesids:
            #print('id')
            #print(id)
            if id not in covered:
                uncoveredyescases.append(id)
        #print('uncoveredyescases')
        #print(uncoveredyescases)
        # HERE BE MY ERROR!!!!
        '''assign gain ranks'''
        gainrankdictionary = dict()
        currentrank = 0
        maxrank = len(self.characterlist)
        rankedcharacters = []

        ####Assign gain ranking to characters

        while currentrank < maxrank:
            currentrank = currentrank + 1
            currentmaxgain = 0.0
            currentmaxgaincharacter = ''
            for character in self.characterlist:
                if currentmaxgain == 0.0 and character not in rankedcharacters:
                    currentmaxgain = self.characterlist[character]["gain"]
                    currentmaxgaincharacter = character
                elif currentmaxgain < self.characterlist[character]["gain"] and character not in rankedcharacters:
                    currentmaxgain = self.characterlist[character]["gain"]
                    currentmaxgaincharacter = character
            gainrankdictionary[currentmaxgaincharacter] = currentrank
            rankedcharacters.append(currentmaxgaincharacter)
        for character in self.characterlist:
            self.characterlist[character]['gainrank'] = gainrankdictionary[character]
        #####END ASSIGNMENT OF RANKS#####
        self.uncoveredyescases = uncoveredyescases

        while len(uncoveredyescases) != 0:
            ''''''
            #print('uncoveredloop')
            currentdatabase = dict()
            duplicateuncoveredyeses = []
            for case in uncoveredyescases:
                duplicateuncoveredyeses.append(case)
                currentdatabase[case] = self.database[case]
                uncoveredyescases.remove(case)
            charact = []
            #print(currentdatabase)
            yeslist = dict()
            for id in currentdatabase:
                #print(currentdatabase[id]["string"])
                for index in currentdatabase[id]['string']:
                    if currentdatabase[id]["string"][index] not in charact:
                        charact.append(currentdatabase[id]['string'][index])
            charmaxgain = 0.0
            charmax = ''
            #print('charat')
            #print(charact)
            #print('characterlist')
            #print(self.characterlist)
            maxigain = 0.0
            gainties = []
            '''
            for cha in characterlist:
                if maxigain == 0.0 and characterlist[cha]['gain'] < 0.0:
                    maxigain = characterlist[cha]['gain'] < 0.0
                    gainties.append(cha)
                elif characterlist[cha]['gain'] > maxigain:
                    gainties
            '''
            cyclegainranks = 1  # starts with highest rank and moves down
            usednodes = []
            rankfetchdictionary = dict()
            for member in self.characterlist:
                #print(member)
                rank = self.characterlist[member]['gainrank']
                #print(rank)
                rankfetchdictionary[rank] = member
            rankcontrol = 1
            characterquantity = len(self.characterlist)
            addtodecisiontree = False
            breakloop = False
            #print('rankfetchdictionary')
            #print(rankfetchdictionary)
            rankaccounted = False
            if len(self.workingcharacters) > 0:
                self.decisiontree[self.fullcoveragetrunk] = self.characterlist[self.fullcoveragetrunk]
                rankaccounted = True
            while rankcontrol <= characterquantity and rankaccounted == False:
                currentchar = rankfetchdictionary[rankcontrol]
                charids = self.characterlist[currentchar]['ids']
                #print('currentchar')
                #print(currentchar)
                #print('charids')
                #print(charids)
                charcoverdids = []
                for indxid in charids:
                    if indxid in duplicateuncoveredyeses:
                        charcoverdids.append(indxid)
                if len(charcoverdids) != 0:
                    self.decisiontree[currentchar] = self.characterlist[currentchar]
                    for val in charcoverdids:
                        for m in duplicateuncoveredyeses:
                            if val == m:
                                duplicateuncoveredyeses.remove(m)
                    rankcontrol = rankcontrol + 1
                else:
                    rankcontrol = rankcontrol + 1
            '''
            currentdatabase = dict()
            for case in uncoveredyescases:
                currentdatabase[case] = self.database[case]
                uncoveredyescases.remove(case)
            banking = NodeCharacterData(currentdatabase, self.projectEntropy, [], [])
            for bank in banking:
                self.decisiontree[bank] = self.characterlist[bank]# HERE BE MY SOLUTION?!?!?!?!?!?!?!?!?
            '''
        #redonetree = branchStripper(self.decisiontree, yesids)
        #self.decisiontree = redonetree
        self.yescountse = yesids
        for mem in self.decisiontree:
            datapassin = dict()
            for ID in self.decisiontree[mem]['ids']:
                datapassin[ID] = self.database[ID]
            #print("mem")
            #print(mem)
            if self.decisiontree[mem]["yescount"] != 0 and self.decisiontree[mem]["nocount"] != 0:
                #print("case")
                passinlist = []
                passinlist.append(mem)
                self.decisiontree[mem]["branches"] = NodeCharacterData(datapassin, self.decisiontree[mem]['entropy'], passinlist, self.database, self)
            elif self.decisiontree[mem]["yescount"] != 0 and self.decisiontree[mem]["nocount"] == 0:
                self.decisiontree[mem]["branches"] = "yes"
                rememberconditions = self.decisiontree[mem]['conditions']
                self.terminalnodes.addTerminalYes(rememberconditions)
            elif self.decisiontree[mem]["yescount"] == 0 and self.decisiontree[mem]["nocount"] != 0:
                self.decisiontree[mem]["branches"] = "no"
                rememberconditions = self.decisiontree[mem]['conditions']
                self.terminalnodes.addTerminalNo(rememberconditions)
            elif self.decisiontree[mem]["yescount"] == 0 and self.decisiontree[mem]["nocount"] == 0:
                self.decisiontree[mem]["branches"] = "Baye Leaf"
        print('uncoveredyescases')
        print(self.uncoveredyescases)
        print('coveredyescases')
        print(self.coveredyescases)
        print('database')
        print(self.database)
        print('yesids')
        print(self.yesids)
        print('uncoveredyescases')
        print(self.uncoveredyescases)
        print('terminalyes')
        print(self.terminalnodes.terminalyes)
        print('terminalno')
        print(self.terminalnodes.terminalno)
        print('workingcharacters')
        print(self.workingcharacters)
        print('fullcoveragetrunk')
        try:
            print(self.fullcoveragetrunk)
        except:
            print('notrunk')
def repeatNodeCharacterData(database, jectEntropy, conditionlist, parentdatabase):
    returnvalue = NodeCharacterData(database, jectEntropy, conditionlist)
    return returnvalue
def NodeCharacterData(database, jectEntropy, conditionlist, parentdatabase, terminals):
    dictionary = dict()
    conditionstoopassin = []
    for condition in conditionlist:
        conditionstoopassin.append(condition)
    Dinosaurse = godClassicallyHateDinos(conditionlist, database)
    Dinosaurse.findmappings()
    mappings = Dinosaurse.mappedcharacters
    decisiontree = dict()
    characterlist = dict()
    yescount = 0  # count yes for later
    yesids = []
    for id in database:
        if database[id]["outcome"] == "yes":
            if id not in yesids:
                yesids.append(id)
            yescount = yescount + 1
        #print(database)
        for char in database[id]["string"]:
            if database[id]["string"][char] not in characterlist and database[id]["string"][char] in Dinosaurse.mappings:
                #print(char)
                subdictionary = dict()
                subdictionary["conditions"] = []
                for x in conditionlist:
                    subdictionary["conditions"].append(x)
                subdictionary["conditions"].append(str(database[id]["string"][char]))
                subdictionary["firstindex"] = dict()
                subdictionary["firstindex"][id] = char
                # subdictionary["mode"] = 0.0
                # subdictionary["harmonicmean"] = 0.0
                conditionstatistics = godClassicallyHateDinos(subdictionary["conditions"], database)
                subdictionary["median"] = 0.0
                subdictionary["samplestd"] = 0.0
                subdictionary["mean"] = char
                subdictionary["total"] = conditionstatistics.returndictionary['yes']+conditionstatistics.returndictionary['no']
                subdictionary["indexes"] = []
                subdictionary["ids"] = conditionstatistics.fetchedids
                currentcharacter = database[id]["string"][char]
                subdictionary["yescount"] = conditionstatistics.returndictionary['yes']
                '''if database[id]["outcome"] == 'yes':
                    subdictionary["yescount"] = subdictionary["yescount"] + 1'''
                subdictionary["nocount"] = conditionstatistics.returndictionary['no']
                '''if database[id]["outcome"] == "no":
                    subdictionary["nocount"] = subdictionary["nocount"] + 1'''
                subdictionary["branchtype"] = "character"
                subdictionary["branches"] = dict()
                #print(database[id]["string"][char])
                characterlist[database[id]["string"][char]] = subdictionary
                characterlist[database[id]["string"][char]]["indexes"].append(int(char))
            elif database[id]["string"][char] in characterlist and database[id]["string"][char] in Dinosaurse.mappings:
                if id not in characterlist[database[id]["string"][char]]["firstindex"]:
                    characterlist[database[id]["string"][char]]["firstindex"][id] = char
                characterranktotal = float(characterlist[database[id]["string"][char]]["mean"]) * float(
                    characterlist[database[id]["string"][char]]["total"])  # (current avg)*(# of occurances)
                characterranktotal = characterranktotal + float(char)
                #if id not in characterlist[database[id]["string"][char]]["ids"]:
                #characterlist[database[id]["string"][char]]["ids"].append(id)
                characterlist[database[id]["string"][char]]["indexes"].append(int(char))
                characterlist[database[id]["string"][char]]["mean"] = characterranktotal / (
                            characterlist[database[id]["string"][char]]["total"] + 1.0)
                characterlist[database[id]["string"][char]]["total"] = characterlist[database[id]["string"][char]][
                                                                           "total"] + 1
    firstlayerdict = dict()
    for character in characterlist:  # Calculate character statistics
        #print("characterlist loop for")
        sampledata = characterlist[character]["indexes"]
        # characterlist[character]["mode"] = statistics.mode(sampledata)
        # characterlist[character]["harmonicmean"] = statistics.harmonic_mean(sampledata)
        characterlist[character]["median"] = statistics.median(sampledata)
        if len(sampledata) == 1 or len(sampledata) == 0:
            characterlist[character]["samplestd"] = "invalid"
        else:
            characterlist[character]["samplestd"] = statistics.stdev(sampledata)
        characterlist[character]["mean"] = statistics.mean(sampledata)
    gaindictionary = dict()
    #print("character list")
    #print(characterlist)
    for x in characterlist:  # Calculate character gain
        #print("characterlist x loop")
        newlist = []
        newlist.append(x)
        gain = CalculateGain(jectEntropy, newlist, database)
        gaindictionary[x] = gain
        subentropy = (float(gain) - float(jectEntropy)) * (-1.0)
        characterlist[x]["entropy"] = subentropy
        characterlist[x]["gain"] = jectEntropy - subentropy
    gainrankdictionary = dict()
    ############Rank Character Gains#######################
    currentrank = 0
    maxrank = len(characterlist)
    rankedcharacters = []
    while currentrank < maxrank:
        currentrank = currentrank + 1
        currentmaxgain = 0.0
        currentmaxgaincharacter = ''
        for character in characterlist:
            if currentmaxgain == 0.0 and character not in rankedcharacters:
                currentmaxgain = characterlist[character]["gain"]
                currentmaxgaincharacter = character
            elif currentmaxgain < characterlist[character]["gain"] and character not in rankedcharacters:
                currentmaxgain = characterlist[character]["gain"]
                currentmaxgaincharacter = character
        gainrankdictionary[currentmaxgaincharacter] = currentrank
        rankedcharacters.append(currentmaxgaincharacter)
    for character in characterlist:
        characterlist[character]['gainrank'] = gainrankdictionary[character]
    ##########END CHARACTER GAIN RANKING###################
    '''
    # findnode of maxiumgain
    minindexcharacter = ""
    maxgain = 0.0
    maxgaincharacters = []
    for y in gaindictionary:
        print("gaindictionary loop")
        if gaindictionary[y] > maxgain:
            maxgain = gaindictionary[y]
            maxgaincharacters = []
            maxgaincharacters.append(y)
        elif gaindictionary[y] == maxgain:
            maxgaincharacters.append(y)
    print("gaindictionary loop end")
    notincludedids = []
    maxnodeincludedids = []
    for char in maxgaincharacters:  # this covers all cases of maxgain included
        print("for char in maxgaincharacters")
        for mem in characterlist[char]["ids"]:
            print("for mem in characterlist[char]['ids']")
            if mem not in maxnodeincludedids:
                maxnodeincludedids.append(mem)
    print("End for char in maxgaincharacters:")
    for ids in database:
        if ids not in maxnodeincludedids:
            notincludedids.append(ids)
    print("Id")
    #not sure what this was for
    uncoveredlibrary = dict()
    numnotincluded = len(notincludedids)
    #while numnotincluded != 0:
    #    for id in notincludedids:
    #        uncoveredlibrary[id] = database[id]

    maxyescount = 0
    tiestatus = False
    tieletters = []
    print("start loop for x in maxgaincharacters:")
    for x in maxgaincharacters:
        cases = characterlist[x]["ids"]
        countyeses = 0
        for case in cases:
            if database[case]["outcome"] == "yes":
                countyeses = countyeses + 1
        if countyeses > maxyescount:
            maxyescount = countyeses
            tieletters = []
            tieletters.append(x)
            tiestatus = False
        elif countyeses == maxyescount:
            tieletters.append(x)
            tiestatus = True
    firstindex = 0
    if tiestatus == True:
        characteraverages = dict()
        for x in tieletters:
            firstsightings = characterlist[x]["firstindex"]
            count = 0
            total = 0
            for id in firstsightings:
                total = total + int(firstsightings[id])
                count = count + 1
            characteraverages[x] = float(total) / float(count)
        min = 0.0
        mincharacter = ''
        for av in characteraverages:
            if min == 0.0:
                min = characteraverages[av]
                mincharacter = av
            elif min > characteraverages[av]:
                min = characteraverages[av]
                mincharacter = av
        decisiontree[mincharacter] = characterlist[mincharacter]
    else:
        for letter in tieletters:
            decisiontree[letter] = characterlist[letter]
    charactermasterlist = []
    for x in characterlist:
        charactermasterlist.append(x)
    conditionlist = []
    uncoveredyescases = []
    coveredyescases = []
    for x in decisiontree:
        conditionlist.append(str(x))
        ids = decisiontree[x]["ids"]
        for id in ids:
            if database[id]["outcome"] == "yes":
                coveredyescases.append(id)
        # 3
        # decisiontree[x]["branches"] = buildcharacterbranches(conditionlist, ids, database)
    print(coveredyescases)
    print(yescount)
    '''
    uncoveredyescases = []
    for id in yesids:
        uncoveredyescases.append(id)
    #print(uncoveredyescases)# I beleve that somewhere around here is the lost data issue.
    while len(uncoveredyescases) != 0:
        currentdatabase = dict()
        duplicateuncoveredyeses = []
        for case in uncoveredyescases:
            duplicateuncoveredyeses.append(case)
            currentdatabase[case] = database[case]
            uncoveredyescases.remove(case)
        charact = []
        #print(currentdatabase)
        yeslist = dict()
        for id in currentdatabase:
            #print(currentdatabase[id]["string"])
            for index in currentdatabase[id]['string']:
                if currentdatabase[id]["string"][index] not in charact:
                    charact.append(currentdatabase[id]['string'][index])
        charmaxgain = 0.0
        charmax = ''
        #print('charat')
        #print(charact)
        #print('characterlist')
        #print(characterlist)
        maxigain = 0.0
        gainties = []
        '''
        for cha in characterlist:
            if maxigain == 0.0 and characterlist[cha]['gain'] < 0.0:
                maxigain = characterlist[cha]['gain'] < 0.0
                gainties.append(cha)
            elif characterlist[cha]['gain'] > maxigain:
                gainties
        '''
        cyclegainranks = 1 #starts with highest rank and moves down
        usednodes = []
        rankfetchdictionary = dict()
        for member in characterlist:
            #print(member)
            rank = characterlist[member]['gainrank']
            #print(rank)
            rankfetchdictionary[rank] = member
        rankcontrol = 1
        characterquantity = len(characterlist)
        addtodecisiontree = False
        breakloop = False
        #print(rankfetchdictionary)
        countincludedglobalchars = 0
        while rankcontrol <= characterquantity:
            currentchar = rankfetchdictionary[rankcontrol]
            charids = characterlist[currentchar]['ids']
            charcoverdids = []
            for indxid in charids:
                if indxid in duplicateuncoveredyeses:
                    charcoverdids.append(indxid)
            if len(charcoverdids) != 0:
                decisiontree[currentchar] = characterlist[currentchar]
                for val in charcoverdids:
                    for m in duplicateuncoveredyeses:
                        if val == m:
                            duplicateuncoveredyeses.remove(m)
                rankcontrol = rankcontrol + 1
            else:
                rankcontrol = rankcontrol + 1
        trunkcovered = False
        #add more branches to work
        for character in decisiontree:
            try:#attempt to fix bug encountered
                if character in terminals.workingcharacters:
                    trunkcovered = True
                    break
            except:
                break
        if trunkcovered == False:
            useable = []
            for char in characterlist:
                if char in terminals.workingcharacters:
                    useable.append(char)
                    for c in useable:
                        decisiontree[c] = characterlist[c]




        '''
        for cha in charact:
            gain = jectEntropy - characterlist[cha]['entropy']
            if charmaxgain == 0 and gain <0.0:
                charmaxgain = gain
                charmax = cha
            elif gain > charmaxgain:
                charmaxgain = gain
                charmax = cha
        newdatabase = dict()
        if charmax != '':
            idstosearch = characterlist[charmax]['ids']
            for x in database:
                if x in idstosearch:
                    newdatabase[x] = database[x]
            storejson(newdatabase)
            banking = repeatNodeCharacterData(newdatabase, jectEntropy, conditionstoopassin, database)
            dictionarystorage.storedictionary(currentdatabase)
            dictionarystorage.storedictionary(banking)
            for bank in banking:
                decisiontree[bank] = characterlist[bank]
        '''
    #decisiontree = branchStripper(decisiontree, yesids)

    for mem in decisiontree:
        datapassin = dict()
        for ID in decisiontree[mem]['ids']:#This identifies data that requires further classification
            datapassin[ID] = database[ID]
        #print("mem")
        #print(mem)
        if decisiontree[mem]["yescount"] != 0 and decisiontree[mem]["nocount"] != 0:
            #print("case")
            passinlist = decisiontree[mem]["conditions"]
            dictionarystorage.storedictionary(characterlist)
            decisiontree[mem]["branches"] = fenceordering(datapassin, passinlist, decisiontree[mem]['entropy'], terminals)
        elif decisiontree[mem]["yescount"] != 0 and decisiontree[mem]["nocount"] == 0:
            decisiontree[mem]["branches"] = "yes"
            terminals.terminalnodes.addTerminalYes(decisiontree[mem]['conditions'])
        elif decisiontree[mem]["yescount"] == 0 and decisiontree[mem]["nocount"] != 0:
            decisiontree[mem]["branches"] = "no"
            terminals.terminalnodes.addTerminalNo(decisiontree[mem]['conditions'])
        elif decisiontree[mem]["yescount"] == 0 and decisiontree[mem]["nocount"] == 0:
            decisiontree[mem]["branches"] = "Baye Leaf"
    return decisiontree
def buildcharacterbranches(self, conditions, cases, database, characterlist):
    currentcases = dict()
    for case in cases:
        currentcases[case] = self.database[case]
    casecharacters = []
    idlist = []
    for id in currentcases:
        idlist.append(id)
#
def fencespacings(database, conditions, Objectmanipulation, terminals):#find all
    conditionlength = len(conditions)
    conditionalphamaxindex = conditionlength - 1 # max condition index
    conditionbetamaxindex = conditionlength - 2 # 2nd to max condition index
    characterbeta = conditions
    distanceslist = []
    idsbyspacingdict = dict()
    if "-" in conditions[conditionalphamaxindex]:
        splitcon1 = conditions[conditionalphamaxindex].split("#")
        splitcon2 = conditions[conditionbetamaxindex].split("#")
        lastletter = splitcon1[0]
        lastletter2 = splitcon2[0]
        for id in database:
            #print(id)
            lastletterindexlist = []
            secondletterindexlist = []
            for index in database[id]["string"]:
                if lastletter == database[id]["string"][index]:
                    #print('a')
                    lastletterindexlist.append(index)
                if lastletter2 == database[id]["string"][index]:
                    #print('b')
                    secondletterindexlist.append(index)
            for x in lastletterindexlist:
                #print(x)
                for y in secondletterindexlist:
                    #print(y)
                    if y > x:
                        distance = x - y
                        #print(distance)
                        if distance not in idsbyspacingdict:
                            idsbyspacingdict[distance] = []
                            idsbyspacingdict[distance].append(id)
                        elif distance in idsbyspacingdict:
                            if id not in idsbyspacingdict[distance]:
                                idsbyspacingdict[distance].append(id)
            #print(lastletterindexlist)
            #print(secondletterindexlist)
    elif "+" in conditions[conditionalphamaxindex]:
        splitcon1 = conditions[conditionalphamaxindex].split("#")
        splitcon2 = conditions[conditionbetamaxindex].split("#")
        lastletter = splitcon1[0]
        lastletter2 = splitcon2[0]
        for id in database:
            lastletterindexlist = []
            secondletterindexlist = []
            for index in database[id]["string"]:
                if lastletter == database[id]["string"][index]:
                    lastletterindexlist.append(index)
                if lastletter2 == database[id]["string"][index]:
                    secondletterindexlist.append(index)
            for x in lastletterindexlist:
                #print(x)
                for y in secondletterindexlist:
                    #print(y)
                    if y < x:
                        distance = x - y
                        #print(distance)
                        if distance not in idsbyspacingdict:
                            idsbyspacingdict[distance] = []
                            idsbyspacingdict[distance].append(id)
                        elif distance in idsbyspacingdict:
                            if id not in idsbyspacingdict[distance]:
                                idsbyspacingdict[distance].append(id)
    return idsbyspacingdict
    #buildthedictionaries
def orderspliting(database, conditions, spacedictionary, terminals):
    conditionlength = len(conditions)
    lastcondition = conditions[conditionlength-1]
    splitlastcondition = lastcondition.split('#')
    currentletter = splitlastcondition[0]
    usedconditions = []
    indexcounter = 0
    while indexcounter < conditionlength-1:
        usedconditions.append(conditions[indexcounter])
        indexcounter = indexcounter + 1
    parentids = []
    for x in spacedictionary:
        for y in spacedictionary[x]:
            if y not in parentids:
                parentids.append(y)
    newsubset = dict()
    for id in parentids:
        newsubset[id] = database[id]
    countdictionary = dict()
    countdictionary['yes'] = 0
    countdictionary['no'] = 0
    for x in database:
        if database[x]['outcome'] == 'yes':
            countdictionary['yes'] = countdictionary['yes'] + 1
        else:
            countdictionary['no'] = countdictionary['no'] + 1
    parententropy = calculateEntropyFromDatabase(database)
    returndictionary = dict()
    for spacing in spacedictionary:
        yescount = 0
        nocount = 0
        spacingdatabasesubset = dict()
        for x in spacedictionary[spacing]:
            spacingdatabasesubset[x] = database[x]
            if database[x]['outcome'] == 'yes':
                yescount = yescount + 1
            elif database[x]['outcome'] == 'no':
                nocount = nocount + 1
        nodeentropy = calculateEntropyFromDatabase(spacingdatabasesubset)
        returndictionary[spacing] = dict()
        returndictionary[spacing]['entropy'] = nodeentropy
        gain = parententropy-nodeentropy
        returndictionary[spacing]['gain'] = gain
        returndictionary[spacing]['branchtype'] = 'spacing'
        returndictionary[spacing]['ids'] = spacedictionary[spacing]
        returndictionary[spacing]['parententropy'] = parententropy
        returndictionary[spacing]['conditions'] = []
        returndictionary[spacing]['yescount'] = yescount
        returndictionary[spacing]['nocount'] = nocount
        for mem in usedconditions:
            returndictionary[spacing]['conditions'].append(mem)
        if '-' in str(spacing):
            newt = currentletter + "#" + str(spacing)
            returndictionary[spacing]['conditions'].append(newt)
        else:
            newt = currentletter + "#+" + str(spacing)
            returndictionary[spacing]['conditions'].append(newt)
        if yescount > 0 and nocount == 0:
            returndictionary[spacing]['branches'] = 'yes'
            terminals.terminalnodes.addTerminalYes(returndictionary[spacing]['conditions'])
        elif nocount > 0 and yescount == 0:
            returndictionary[spacing]['branches'] = 'no'
            terminals.terminalnodes.addTerminalNo(returndictionary[spacing]['conditions'])
        elif nocount == 0 and yescount == 0:
            returndictionary[spacing]['branches'] = "Baye leaf"
        else:
            passin = returndictionary[spacing]['conditions']
            #print(passin)
            returndictionary[spacing]['branches'] = NodeCharacterData(spacingdatabasesubset, nodeentropy, passin, [], terminals)
    return returndictionary
def fenceordering(database, conditions, parententropy, terminals):# entropy by what side of the previous character newcharacter is found
    lencondition = len(conditions)
    lastcondition = conditions[lencondition-1]
    newpluscondition = lastcondition + '#+'
    newminuscondition = lastcondition + '#-'
    reduced = []
    for y in conditions:
        reduced.append(y)
    #print(reduced)
    reduced.remove(lastcondition)
    upfence = []
    downfence = []
    for x in reduced:
        upfence.append(x)
        downfence.append(x)
    #print(lastcondition)
    #print(reduced)
    upfence.append(newpluscondition)
    downfence.append(newminuscondition)
    #print("upfence")
    #print(upfence)
    #print(database)
    negativespacings = fencespacings(database, downfence, 0.0, terminals)
    positivespacings = fencespacings(database, upfence, 0.0, terminals)
    plusObj = godClassicallyHateDinos(upfence, database)
    minusObj = godClassicallyHateDinos(downfence, database)
    minusObjEntropy = calculateEntropy(minusObj.returndictionary)
    plusObjEntropy = calculateEntropy(plusObj.returndictionary)
    minussidegain = parententropy - minusObjEntropy
    plussidegain = parententropy - plusObjEntropy
    dictionaryreturn = {}
    plusdictionary = dict()
    plusdictionary['spacings'] = []
    for r in positivespacings:
        plusdictionary['spacings'].append(r)
    plusdictionary['entropy'] = plusObjEntropy
    plusdictionary['gain'] = plussidegain
    plusdictionary['conditions'] = upfence
    plusdictionary['ids'] = plusObj.fetchedids
    plusdictionary['yescount'] = plusObj.returndictionary['yes']
    plusdictionary['nocount'] = plusObj.returndictionary['no']
    plusdictionary['total'] = int(plusObj.returndictionary['yes']) + int(plusObj.returndictionary['no'])
    plusdictionary['branchtype'] = "order"
    if plusObj.returndictionary['yes'] == 0 and plusObj.returndictionary['no'] == 0:
        plusdictionary['branches'] = 'baye leaf'
    elif plusObj.returndictionary['yes'] > 0 and plusObj.returndictionary['no'] == 0:
        plusdictionary['branches'] = 'yes'
        if len(plusdictionary['ids']) > 0:
            terminals.terminalnodes.addTerminalYes(plusdictionary['conditions'])
    elif plusObj.returndictionary['yes'] == 0 and plusObj.returndictionary['no'] > 0:
        if len(plusdictionary['ids']) > 0:
            terminals.terminalnodes.addTerminalNo(plusdictionary['conditions'])
        plusdictionary['branches'] = 'no'
    else:
        distdictionary = dict()
        for this in plusdictionary['ids']:
            distdictionary[this] = database[this]
        dist1dictionary = fencespacings(distdictionary, upfence, plusdictionary['entropy'], terminals)
        plusdictionary['branches'] = orderspliting(distdictionary, upfence, dist1dictionary, terminals)
    negativedictionary = dict()
    negativedictionary['spacings'] = []
    for ele in negativespacings:
        negativedictionary['spacings'].append(ele)
    negativedictionary['entropy'] = minusObjEntropy
    negativedictionary['gain'] = minussidegain
    negativedictionary['conditions'] = downfence
    negativedictionary['ids'] = minusObj.fetchedids
    negativedictionary['yescount'] = minusObj.returndictionary['yes']
    negativedictionary['nocount'] = minusObj.returndictionary['no']
    negativedictionary['total'] = int(minusObj.returndictionary['no']) + int(minusObj.returndictionary['yes'])
    negativedictionary['branchtype'] = "order"
    if minusObj.returndictionary['yes'] == 0 and minusObj.returndictionary['no'] == 0:
        negativedictionary['branches'] = 'baye leaf'
    elif minusObj.returndictionary['yes'] > 0 and minusObj.returndictionary['no'] == 0:
        negativedictionary['branches'] = 'yes'
        terminals.terminalnodes.addTerminalYes(negativedictionary['conditions'])
    elif minusObj.returndictionary['yes'] == 0 and minusObj.returndictionary['no'] > 0:
        negativedictionary['branches'] = 'no'
        terminals.terminalnodes.addTerminalNo(negativedictionary['conditions'])
    else:
        passin = dict()
        for this in negativedictionary['ids']:
            passin[this] = database[this]
        distancedictionary = fencespacings(passin, downfence, negativedictionary['entropy'], terminals)
        negativedictionary['branches'] = orderspliting(passin, downfence, distancedictionary, terminals)
    dictionaryreturn[newpluscondition] = plusdictionary
    dictionaryreturn[newminuscondition] = negativedictionary
    return dictionaryreturn
class storedatapoint:
    def __init__(self, datastored):
        self.data = datastored
def rawGainCalculation(ParentEntropy, data):#Calculate from dictionary
    subentropy = calculateEntropy(data)
    gain = ParentEntropy - subentropy
    return gain
def CalculateGain(ParentEntropy, condition, database):#BAD CODING!!!!!!!!!!! DO NOT USE!!!!!!!
    returngain = 0.0
    subEntropy = 0.0
    if '#' in condition[0]:
        subEntropy = fineOrderedSubcasesEntropy(condition, database)
    else:
        subEntropy = loseOrderedSubcasesEntropy(condition, database)
    returngain = ParentEntropy - subEntropy
    return returngain
def mappingdata(database, databaseentropy, character):# finds characters mapped to current conditions
    alreadyflaggedids = []
    mappedcharacters = []
    for x in database:
        for index in database["string"]:
            if database["string"][index] == character and x in alreadyflaggedids:
                mappedcharacters.append(character)
            elif database["string"][index] == character and x not in alreadyflaggedids:
                alreadyflaggedids.append(x)
            elif database["string"][index] not in mappedcharacters and database["string"][index] != character:
                mappedcharacters.append(character)
    return mappedcharacters


class CalculateProjectEntropy:#CHECK
    def __init__(self, database):
        dictionary = {}
        dictionary["yes"] = 0
        dictionary["no"] = 0
        #print('dictionary created')
        #print(database)
        for id in database:
            if database[id]["outcome"] == "yes":
                dictionary["yes"] = dictionary["yes"] + 1
            elif database[id]["outcome"] == "no":
                dictionary["no"] = dictionary["no"] + 1
        #print(dictionary)
        entropy = calculateEntropy(dictionary)
        self.entropy = entropy
        self.statistics = dictionary
def loseOrderedSubcasesEntropy(condition, database):# I think this is dead code
    data = godHatasDinosaures(condition, database)
    Entropy = calculateEntropy(data)
    return Entropy
def fineOrderedSubcasesEntropy(condition, database):# I think this is dead code
    data = godHatasDinosaures(condition, database)
    entropy = calculateEntropy(data)
    return entropy

class godClassicallyHateDinos:
    def __init__(self, conditions, database):
        self.fetchedids = []
        self.conditionlength = len(conditions)
        self.matchdictionary = dict()
        self.mappings = []
        self.returndictionary = dict()
        self.saveddatabase = database
        self.letterdictionary = dict()
        returndictionary = dict()
        returndictionary["yes"] = 0
        returndictionary["no"] = 0
        countresultyes = 0
        countresultno = 0
        conditionlength = len(conditions)
        #print(database)
        databaselength = len(database)
        databasecontroll = databaselength + 1
        #print('databaselength =' + str(databaselength))
        # Start for loop over ids
        for id in database:
            self.matchdictionary[id] = []
            #print('current id = ' + str(id))
            stringdiction = database[id]["string"]
            #print(stringdiction)
            countmatches = 0
            whilelooplistindexcounter = 0
            # Start for loop over "string" index
            previousindex = 0
            index = 1
            continueindex = True
            maxindex = len(database[id]["string"])
            currentcondition = 0
            conditionslength = len(conditions)
            usedindexes = []
            usedindexesdictionary = dict()
            letterdictionary = {}
            #bugfix
            for con in conditions:
                if '#' in con:
                    splitthis = con.split('#')
                    letterdictionary[splitthis[0]] = []
                else:
                    letterdictionary[con] = []
            conditionloopthrough = 0
            while currentcondition < conditionslength:
                if conditionloopthrough >= conditionlength:
                    break
                conditionloopthrough = conditionloopthrough + 1
                #print('currentconditon')
                #print(conditions[currentcondition])
                #print(currentcondition)
                #print('current id')
                #print(id)
                if '#' in conditions[currentcondition]:
                    startindex = 0
                    splitcondition = conditions[currentcondition].split('#')
                    conditionletter = splitcondition[0]
                    conditiondomain = splitcondition[1]
                    last = ''
                    for index in database[id]["string"]:
                        if database[id]["string"][index] == conditionletter:
                            if conditionletter in letterdictionary:
                                letterdictionary[conditionletter].append(index)
                            elif conditionletter not in letterdictionary:
                                letterdictionary[conditionletter] = []
                                letterdictionary[conditionletter].append(index)
                    currentcondition = currentcondition + 1
                else:
                    conditionletter = conditions[currentcondition]
                    for index in database[id]["string"]:
                        if database[id]["string"][index] == conditions[currentcondition]:
                            if conditionletter in letterdictionary:
                                letterdictionary[conditionletter].append(index)
                            elif conditionletter not in letterdictionary:
                                letterdictionary[conditionletter] = []
                                letterdictionary[conditionletter].append(index)
                    currentcondition = currentcondition + 1
                #print(letterdictionary)
                #print(usedindexes)
            initializedictionary = dict()
            usedconditions = []
            conditionindex = 0
            matchcount = 0
            loopcount = 0
            while conditionindex < self.conditionlength:
                if loopcount > self.conditionlength:# this is to resolve a wired loop problem
                    break
                loopcount = loopcount + 1
                condition = conditions[conditionindex]
                conditionletterfetch = condition
                #print(conditionindex)
                #print(matchcount)
                split4condition = []
                if '#' in condition:
                    split4condition = condition.split('#')
                    conditionletterfetch = split4condition[0]
                #print(letterdictionary)
                if conditionindex == 0 and len(letterdictionary[conditionletterfetch]) > 0:
                    for x in letterdictionary[conditionletterfetch]:
                        newlist = []
                        newlist.append(x)
                        usedconditions.append(newlist)
                    conditionindex = conditionindex + 1
                    matchcount = matchcount + 1
                    #usedconditions.append(newlist)
                elif len(condition) == 1 and conditionindex > 0:
                    #print("single")
                    listindexes = letterdictionary[condition]
                    newconditionlist = []
                    poplist = []
                    matchfound = False
                    for indx in listindexes:
                        currentindex = 0
                        for list in usedconditions:
                            if indx not in list:
                                matchfound = True
                                newlist = []
                                for l in list:
                                    newlist.append(l)
                                newlist.append(indx)
                                if currentindex not in poplist:
                                    poplist.append(currentindex)
                                newconditionlist.append(newlist)
                            currentindex = currentindex + 1
                    if matchfound == True:
                        matchcount = matchcount + 1
                        conditionindex = conditionindex + 1
                        for pip in poplist:
                            try:
                                usedconditions.pop(pip)
                            except:
                                print('*')
                        for lis in newconditionlist:
                            usedconditions.append(lis)
                elif conditionindex > 0 and len(letterdictionary[split4condition[0]]) > 0:
                    if '#' in condition:
                        lettersplit = condition.split('#')
                        editedlist = []
                        conditionindexes = []
                        listindex = 0
                        if len(condition) > 3:
                            integer = int(lettersplit[1])
                            conditionindexincrease = False
                            increasematchcount = False
                            newconditions = [] #too add to usedconditions
                            poplistindexes = [] #pop usedconditions
                            for list in usedconditions:
                                maxindex = len(list) - 1
                                lastcharacter = list[maxindex]
                                newindex = lastcharacter + integer
                                if newindex in letterdictionary[lettersplit[0]] and newindex not in list:
                                    newlist = []
                                    for x in list:
                                        newlist.append(x)
                                    newlist.append(newindex)
                                    conditionindexincrease = True
                                    increasematchcount = True
                                    if listindex not in poplistindexes:
                                        poplistindexes.append(listindex)
                                    newconditions.append(newlist)
                                    listindex = listindex + 1
                                    continue
                                else:
                                    listindex = listindex + 1
                            if conditionindexincrease == True and increasematchcount == True:
                                conditionindex = conditionindex + 1
                                matchcount = matchcount + 1
                                for indx in poplistindexes:
                                    try:
                                        usedconditions.pop(indx)
                                    except:
                                        print('*')
                                for lis in newconditions:
                                    usedconditions.append(lis)
                        elif '-' in condition:
                            matchstatus = False
                            addtoused = []
                            lists2pop = []
                            currentlist = 0
                            for list in usedconditions:
                                if len(list) == matchcount:
                                    max = len(list) - 1
                                    lastcall = list[max]
                                    indxlist = letterdictionary[lettersplit[0]]
                                    sublisttoadd = []
                                    for lis in indxlist:
                                        if lis < lastcall and lis not in list:
                                            sublist = []
                                            for x in list:
                                                sublist.append(x)
                                            sublist.append(lis)
                                            sublisttoadd.append(sublist)
                                            matchstatus = True
                                    for sub in sublisttoadd:
                                        addtoused.append(sub)
                                lists2pop.append(currentlist)
                                currentlist = currentlist + 1
                            for n in lists2pop:
                                try:
                                    usedconditions.pop(n)
                                except:
                                    print('*')
                            for add in addtoused:
                                usedconditions.append(add)
                            if matchstatus == True:
                                matchcount = matchcount + 1
                                conditionindex = conditionindex + 1
                            else:
                                break
                        elif '+' in condition:
                            matchstatus = False
                            addtoused = []
                            lists2pop = []
                            currentlist = 0
                            for list in usedconditions:
                                if len(list) == matchcount:
                                    max = len(list) - 1
                                    lastcall = list[max]
                                    indxlist = letterdictionary[lettersplit[0]]
                                    sublisttoadd = []
                                    for lis in indxlist:
                                        if lis > lastcall and lis not in list:
                                            sublist = []
                                            for x in list:
                                                sublist.append(x)
                                            sublist.append(lis)
                                            sublisttoadd.append(sublist)
                                            matchstatus = True
                                    for sub in sublisttoadd:
                                        addtoused.append(sub)
                                lists2pop.append(currentlist)
                                currentlist = currentlist + 1
                            for n in lists2pop:
                                try:
                                    usedconditions.pop(n)
                                except:
                                    print('*')
                            for add in addtoused:
                                usedconditions.append(add)
                            if matchstatus == True:
                                matchcount = matchcount + 1
                                conditionindex = conditionindex + 1
                            else:
                                break
                    elif len(condition) == 1 and len(letterdictionary[condition]):
                        matchstatus = False
                        newindexes = letterdictionary[condition]
                        newlists = []
                        xlooplist = []
                        listsedited = []
                        for x in newindexes:
                            indxoflist = 0
                            for list in usedindexes:
                                if len(list) == matchcount:
                                    newlist = []
                                    if x not in list:
                                        for y in list:
                                            newlist.append(y)
                                        newlist.append(x)
                                        newlists.append(newlist)
                                        matchstatus = True
                                        if indexoflist not in listsedited:
                                            listsedited.append(indexoflist)
                                indxoflist = indxoflist + 1
                        for idx in listsedited:
                            usedconditions.pop(idx)
                        for dx in newlists:
                            usedconditions.append(dx)
                        if matchstatus == True:
                            matchcount = matchcount + 1
                            conditionindex = conditionindex + 1
                        else:
                            break
                    else:
                        break
                else:
                    break
            #while conditionloop over
            print('id')
            print(id)
            if matchcount == len(conditions):
                self.matchdictionary[id] = usedconditions
                self.fetchedids.append(id)
                if database[id]['outcome'] == 'yes':
                    returndictionary['yes'] = returndictionary['yes'] + 1
                else:
                    returndictionary['no'] = returndictionary['no'] + 1
            self.letterdictionary[id] = letterdictionary
        self.returndictionary = returndictionary
    def findmappings(self):
        print(self.matchdictionary)
        print(self.saveddatabase)
        self.mappedcharacters = []
        for id in self.fetchedids:
            print(id)
            mappedindexes = []
            for list in self.matchdictionary[id]:
                if len(list) == self.conditionlength:
                    for index in self.saveddatabase[id]['string']:
                        print(index)
                        if index not in list:
                            mappedindexes.append(index)
                            currentchar = self.saveddatabase[id]['string'][index]
                            print(currentchar)
                            if currentchar not in self.mappedcharacters:
                                self.mappedcharacters.append(currentchar)
        self.mappings = self.mappedcharacters
def godHatasDinosaures(conditions, database):
    returndictionary = dict()
    returndictionary["yes"] = 0
    returndictionary["no"] = 0
    countresultyes = 0
    countresultno = 0
    conditionlength = len(conditions)
    databaselength =len(database)
    databasecontroll = databaselength + 1
    #print('databaselength ='+str(databaselength))
    #Start for loop over ids
    for id in database:
        #print('current id = ' +str(id))
        stringdiction = database[id]["string"]
        #print(stringdiction)
        countmatches = 0
        whilelooplistindexcounter = 0
        #Start for loop over "string" index
        previousindex = 0
        index = 1
        continueindex = True
        maxindex = len(database[id]["string"])
        currentcondition = 0
        conditionslength = len(conditions)
        usedindexes = []
        usedindexesdictionary = dict()
        letterdictionary = {}
        conditionloopthrough = 0
        while currentcondition < conditionslength:
            if conditionloopthrough >= conditionlength:
                break
            conditionloopthrough = conditionloopthrough + 1
            print('currentconditon')
            print(conditions[currentcondition])
            print(currentcondition)
            print('current id')
            print(id)
            if '#' in conditions[currentcondition]:
                startindex = 0
                splitcondition = conditions[currentcondition].split('#')
                conditionletter = splitcondition[0]
                conditiondomain = splitcondition[1]
                last = ''
                for index in database[id]["string"]:
                    if database[id]["string"][index] == conditionletter:
                        if conditionletter in letterdictionary:
                                letterdictionary[conditionletter].append(index)
                        elif conditionletter not in letterdictionary:
                                letterdictionary[conditionletter] = []
                                letterdictionary[conditionletter].append(index)
                currentcondition = currentcondition + 1
            else:
                conditionletter = conditions[currentcondition]
                for index in database[id]["string"]:
                    if database[id]["string"][index] == conditions[currentcondition]:
                        if conditionletter in letterdictionary:
                            letterdictionary[conditionletter].append(index)
                        elif conditionletter not in letterdictionary:
                            letterdictionary[conditionletter] = []
                            letterdictionary[conditionletter].append(index)
                currentcondition = currentcondition + 1
            print(letterdictionary)
            print(usedindexes)
        initializedictionary = dict()
        usedconditions = []
        for condition in conditions:
            if len(usedconditions) == 0:
                if len(letterdictionary) == 0:#bugfix
                    break
                print(condition)
                print(conditions)
                print(letterdictionary)
                for num in letterdictionary[condition]:
                    newlist = []
                    newlist.append(num)
                    usedconditions.append(newlist)
            elif '#' in condition:#order matter cases
                conditionsplit = condition.split('#')
                conditionchar = conditionsplit[0]
                if len(conditionsplit[1]) > 1:
                    conditionspacing = int(conditionsplit[1])
                    appendingusedconditions = []
                    for num in letterdictionary[conditionchar]:
                        for list in usedconditions:
                            currentlist = list
                            maxlistindex = len(list) - 1
                            lastindex = list[maxlistindex]
                            next = lastindex + conditionspacing
                            if num == next and next not in currentlist:
                                currentlist.append(num)
                            appendingusedconditions.append(currentlist)
                    usedconditions = appendingusedconditions
                elif len(conditionsplit[1]) == 1:
                    if '-' in conditionsplit[1]:
                        appendingusedconditions = []
                        for num in letterdictionary[conditionchar]:
                            for list in usedconditions:
                                currentlist = list
                                print(list)
                                maxlistindex = len(list) - 1
                                lastindex = list[maxlistindex]
                                if num < lastindex and num not in currentlist:
                                    currentlist.append(num)
                                appendingusedconditions.append(currentlist)
                        usedconditions = appendingusedconditions
                    elif '+' in conditionsplit[1]:
                        appendingusedconditions = []
                        for num in letterdictionary[conditionchar]:
                            for list in usedconditions:
                                currentlist = list
                                maxlistindex = len(list) - 1
                                lastindex = list[maxlistindex]
                                if num > lastindex and num not in currentlist:
                                    currentlist.append(num)
                                appendingusedconditions.append(currentlist)
                        usedconditions = appendingusedconditions
            else: # order doesn't matter
                print("usedconditions")
                print(usedconditions)
                appendingusedconditions = []
                for num in letterdictionary[condition]:
                    print(num)
                    for list in usedconditions:
                        currentlist = list
                        print(list)
                        if num not in currentlist:
                            currentlist.append(num)
                            print(currentlist)
                        appendingusedconditions.append(currentlist)
                usedconditions = appendingusedconditions
        maxlengthmatch = 0
        conditionlength = len(conditions)
        for lis in usedconditions:
            length = len(lis)
            if length > maxlengthmatch:
                maxlengthmatch = length
        #countmatches = len(usedindexes)
        #End while loop over "string" index
        if maxlengthmatch >= conditionlength:
            idresult = database[id]["outcome"]
            if idresult == "yes":
                returndictionary["yes"] = returndictionary["yes"] + 1
            else:
                returndictionary["no"] = returndictionary["no"] + 1
    #End for loop over ids
    return returndictionary
def calculateEntropy(passindict):
    #print(passindict)
    total = passindict["yes"] + passindict["no"]
    #print(total)
    yescount = passindict["yes"]
    nocount = passindict["no"]
    if total == 0:
        yesprobability = 0.0
        noprobability = 0.0
    else:
        yesprobability = float(yescount/total)
        noprobability = float(nocount/total)
    probabilitylist = [yesprobability, noprobability]
    #print(probabilitylist)
    returnvalue = 0.0
    for value in probabilitylist:
        if value > 0.0:
            newvalue = (-1.0) * value * math.log2(value)
            #print(value)
            #print(newvalue)
            returnvalue = returnvalue + newvalue
        else:
            returnvalue = returnvalue + value
    return returnvalue
class seekterminalnodes:
    def __init__(self, dic):
        self.yesoutcomes = []
        self.currentjsonpath = []
        self.terminalconditionpaths = []
        for mem in dic:
            checkbranch = dic[mem]["branches"]
            current = dic[mem]["conditions"]
            if checkbranch == "yes" or checkbranch == "no" or checkbranch == "Baye leaf":
                self.yesoutcomes.append(current)
            else:
                self.duplicatefunction1(checkbranch)


    def duplicatefunction1(self, ff):
        print(ff)
        for mem in ff:
            print(ff[mem])
            checkbranch = ff[mem]["branches"]
            current = ff[mem]["conditions"]
            print("function1")
            if checkbranch == "yes" or checkbranch == "no" or checkbranch == "Baye leaf":
                self.yesoutcomes.append(current)
            else:
                print(current)
                self.duplicatefunction2(current)

    def duplicatefunction2(self, ff):
        for mem in ff:
            checkbranch = ff[mem]["branches"]
            current = ff[mem]["conditions"]
            print("function2")
            if checkbranch == "yes" or checkbranch == "no" or checkbranch == "Baye leaf":
                self.yesoutcomes.append(current)
            else:
                self.duplicatefunction2(current)
class seektarget:
    def __init__(self, dic):
        self.notyesoutcomes = []
        self.yesoutcomes = []
        for mem in dic:
            checkbranch = dic[mem]["branches"]
            current = dic[mem]["conditions"]
            if checkbranch == "yes":
                self.yesoutcomes.append(current)
            elif checkbranch == "no":
                self.notyesoutcomes.append(current)
            else:
                self.duplicatefunction1(checkbranch)
    def duplicatefunction1(self, ff):
        print(ff)
        for mem in ff:
            print(ff[mem])
            checkbranch = ff[mem]["branches"]
            print(checkbranch)
            current = ff[mem]["conditions"]
            print("function1")
            if checkbranch == "yes":
                self.yesoutcomes.append(current)
            elif checkbranch == "no":
                self.notyesoutcomes.append(current)
            else:
                print(current)
                print(checkbranch)
                self.duplicatefunction2(checkbranch)
    def duplicatefunction2(self, ff):
        print('current dictionary')
        print(ff)
        for mem in ff:
            print(ff[mem])
            checkbranch = ff[mem]["branches"]
            print(checkbranch)
            current = ff[mem]["conditions"]
            print("function1")
            if checkbranch == "yes":
                self.yesoutcomes.append(current)
            elif checkbranch == "no":
                self.notyesoutcomes.append(current)
            else:
                print(current)
                print(checkbranch)
                self.duplicatefunction1(checkbranch)
def evaluateSingleData(yeslists, singlecondition):
    submittiondictionary = dict()
    submittiondictionary[1] = dict()
    returndictionary = dict()
    submittiondictionary[1]["string"] = dict()
    submittiondictionary[1]["outcome"] = singlecondition["outcome"]
    matchind = 1
    indexer = 1
    for char in singlecondition["string"]:
        submittiondictionary[1]["string"][indexer] = char
        indexer = indexer + 1
    for list in yeslists:
        result = godClassicallyHateDinos(list, submittiondictionary)
        resultdic = result.returndictionary
        if resultdic['yes'] > 0:
            returndictionary[matchind] = list
    return returndictionary