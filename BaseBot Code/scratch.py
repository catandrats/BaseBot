import tkinter as tk
import NoSqlBuilder
import os
import json
import time
def getdatapath():
    datapath = os.getenv('APPDATA')
    #print(datapath)
    return datapath
#Filters out duplicate nodes
def filterDuplicateNodes(nodelist):#nodelist is to be a list of lists decribing sequences
    mappingdictionary = dict()
    currentnodelistindex = 0
    notincludedlists = []
    for list in nodelist:# iterate over list in list of lists
        print('list')
        print(list)
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

                print(currentnodelistindex)
                break
        print('notincluded')
        print(notincludedlists)
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
def reasonOutputValidation(database, stringlist, yescount):# validate hypothesis
    lists = convertStringReason2List(stringlist)
    success = []
    for list in lists:
        if '#' in list[0]:
            continue
        else:
            Obj = NoSqlBuilder.godClassicallyHateDinos(list, database)
            if Obj.returndictionary['yes'] == yescount and Obj.returndictionary['no'] == 0:
                success.append(list)
    returnstring = ''
    for validlist in success:
        returnstring = returnstring + convertListReason2String(validlist)
    return returnstring
def convertStringReason2List(string):#convert list remembered as a string back into a list
    returnlist = []
    if '][' in string:
        listsubstrings = string.split('][')
        for ls in listsubstrings:
            lls = ls.replace(']', '')
            rls = lls.replace('[', '')
            listadd = rls.split(', ')
            returnlist.append(listadd)
    else:
        rightstring = string.replace(']', '')
        leftstring = rightstring.replace('[', '')
        newlist = leftstring.split(', ')
        returnlist.append(newlist)
    return returnlist
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
def verifycharacter(char):# Used for input validation
    listvalidchar = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    if char in listvalidchar:
        return True
    else:
        return False
def orderSequence4User(sequences):# This is ment to prettify output data a low priority atm
    sequencedictionary = dict()
    sequenceid = 1
    for sequence in sequences:
        sequencedictionary[sequenceid] = dict()
        sequencedictionary[sequenceid]['exactorder'] = dict()# I am perplexed as to what this was for
        sequenceindexlist = []
        lastletterunspecified = False
        newstring = ''
        currentindex = 0
        for x in sequence:
            if '#' not in x and len(sequenceindexlist):
                sequenceindexlist.append(0)
                sequencedictionary[sequenceid][currentindex] = x
            elif '#' in x and len(x) > 3:
                spliter = x.split('#')
                currentindex = currentindex + int(x.split[1])
                sequenceindexlist.append(int(spliter[1]))
                sequencedictionary[sequenceid][currentindex] = x
            elif '#' in x and len(x) == 3:
                if '-' in x:
                    edit = sequenceindexlist[-1]
                    newindex = edit - 1
                    sequenceindexlist.append(edit)
                elif '+' in x:
                    edit = sequenceindexlist[-1]
                    newindex = edit + 1
                    sequenceindexlist.append(edit)
        loopcontrol = len(sequenceindexlist) - 1
        current = 0
def convertSinglet2DatabaseFormat(stringData, outcome):#This converts single data points into the form inwhich training data is remembered and stored
    returndictionary = dict()
    returndictionary[1] = dict()
    returndictionary[1]['string'] = dict()
    indexcount = 0
    for x in stringData:
        indexcount = indexcount + 1
        returndictionary[1]['string'][indexcount] = x
    returndictionary[1]['outcome'] = outcome
    return returndictionary
class buildtree:# This starts the decisiontree building process from the GUI
    def __init__(self, database):
        decisiontree = NoSqlBuilder.TreeBuild(database)
        self.tree = decisiontree.decisiontree
        self.yesids = decisiontree.yesids
        self.projectEntropy = decisiontree.projectEntropy
        self.yesoutcomes = decisiontree.terminalnodes.terminalyes
        self.nooutcomes = decisiontree.terminalnodes.terminalno
        self.reasonstring = ''
        self.matchfound = False
        yesdatabase = dict()
        workingsequences = []
        stringsequences = ''
        numberofyes = 0
        for id in self.yesids:# This helps identify
            numberofyes = numberofyes + 1
            yesdatabase[id] = database[id]
        for condition in self.yesoutcomes:
            data = NoSqlBuilder.godClassicallyHateDinos(condition, yesdatabase)
            yesreturns = data.returndictionary['yes']
            if yesreturns == numberofyes:
                workingsequences.append(condition)
                self.matchfound = True
        for x in workingsequences:
            maxindex = len(x)
            currentindex = 0
            while currentindex < maxindex:
                if currentindex == 0:
                    stringsequences = stringsequences + '['
                stringsequences = stringsequences + x[currentindex]
                if currentindex < maxindex - 1:
                    stringsequences = stringsequences + ', '
                currentindex = currentindex + 1
                if currentindex == maxindex:
                    stringsequences = stringsequences + ']'
        self.workingsequences = workingsequences
        self.reasonstring = stringsequences
def convertJsontoIntdic(dictionary):#convert string dictionary to proper data
    newdictionary = dict()
    for x in dictionary:
        appentiondiction = dict()
        for y in dictionary[x]['string']:
            appentiondiction[int(y)] = dictionary[x]['string'][y]
        newdictionary[int(x)] = dict()
        newdictionary[int(x)]['string'] = appentiondiction
        newdictionary[int(x)]['outcome'] = dictionary[x]['outcome']
        newdictionary[int(x)]['hypothesis'] = dictionary[x]['hypothesis']
    return newdictionary
def findProjects():#will be changed for any linux
    datapath = getdatapath()
    list = os.listdir(datapath+"\\BaseBot")
    print(list)
    return list
def createDirectory():
    datapath = getdatapath()
    os.system('mkdir "'+datapath+'\\BaseBot"')
class lastkey:
    def __init__(self, key):
        self.lastkey = key
storeObj = lastkey('')
class dictionaryconstruct:#This stores event descriptions assigned to each character
    def __init__(self):
        letterdictionary = dict()
        letterdictionary['a'] = ''
        letterdictionary['b'] = ''
        letterdictionary['c'] = ''
        letterdictionary['d'] = ''
        letterdictionary['e'] = ''
        letterdictionary['f'] = ''
        letterdictionary['g'] = ''
        letterdictionary['h'] = ''
        letterdictionary['i'] = ''
        letterdictionary['j'] = ''
        letterdictionary['k'] = ''
        letterdictionary['l'] = ''
        letterdictionary['m'] = ''
        letterdictionary['n'] = ''
        letterdictionary['o'] = ''
        letterdictionary['p'] = ''
        letterdictionary['q'] = ''
        letterdictionary['r'] = ''
        letterdictionary['s'] = ''
        letterdictionary['t'] = ''
        letterdictionary['u'] = ''
        letterdictionary['v'] = ''
        letterdictionary['w'] = ''
        letterdictionary['x'] = ''
        letterdictionary['y'] = ''
        letterdictionary['z'] = ''
        self.letterdiction = letterdictionary
    def assignletter(self, letter, assignment):
        self.letterdiction[letter] = assignment
useddictionary = dictionaryconstruct()
class startupdialog:# Dead code written when I had a more complicated idea for the GUi
    def __init__(self):
        self.rootstartmenu = tk.Tk()
        self.framestartmenu = tk.Frame(self.rootstartmenu)
        tk.Label(self.framestartmenu, text="Select option").grid(row=0, column=0)
        self.createnewsetup = tk.Button(self.framestartmenu, text="Create new setup", command = self.creatsetup).grid(row=1, column=0)
        self.useexistingsetup = tk.Button(self.framestartmenu, text="Use existing setup", command = self.existingsetupdialog).grid(row=1, column=2)
        self.framestartmenu.pack(pady=10, padx=10)
        self.rootstartmenu.mainloop()
    def creatsetup(self):
        self.rootstartmenu.destroy()
        createdatasetup()
    def existingsetupdialog(self):
        self.rootstartmenu.destroy()
        selectdatasetup()
class numbercounter:#not sure what this does
    def __init__(self):
        self.integer = 1
        self.skipbutton = 2
    def add(self):
        self.integer = self.integer + 1
        self.skipbutton = self.skipbutton + 1
numberdatasetup = numbercounter()
createDirectory()
class createdatasetup:#dead code might be used later
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Create new question')
        self.frame = tk.Frame(self.root)
        tk.Label(self.frame, text="Assign custom values or skip to use default a,b,c,d,...z values").grid(row=0, column=0)
        value = tk.Entry(self.frame)
        self.value = value
        self.value.grid(row=numberdatasetup.integer, column=0)
        addvalue = tk.Button(self.frame, text="Add value", command=self.destroybuttons)
        self.addvalue = addvalue
        self.addvalue.grid(row=numberdatasetup.integer, column=1)
        skipbutton = tk.Button(self.frame, text="Skip", command=self.skip)
        self.skipbutton = skipbutton
        self.skipbutton.grid(row=numberdatasetup.skipbutton, column=1)
        self.frame.pack()
        self.root.mainloop()
    def destroybuttons(self):
        newvalue = self.value.getvalue()
        #for x in
        self.addvalue.destroy()
        self.value.destroy()
        self.skipbutton.destroy()

    def skip(self):
        self.root.destroy()
def note(input):
    print(input)
    print('note')
def lastchar(inthis):#this is used to keep input data up to date with current key strokes
    print(inthis)
    stringdecon = str(inthis)
    letter = stringdecon[23: 24]
    print(letter)
class setupdialog:#Accessed by clicking Create new Project or Save when a project has not already been created
    def __init__(self, parent, newsetup):
        def handle():#handles are used to prevent duplicate guis
            parent.createNewSetupGuiPresent = False
            self.root.destroy()
        if parent.createNewSetupGuiPresent == False:
            parent.createNewSetupGuiPresent = True
            ########Passed in Boolean##########
            #storObj = lastkey(self)
            self.newsetup = newsetup
            ###################################
            #######Gui DUPLICATION PROTECTION##############
            self.savePopupGuiNotification = False
            ###############################################
            #useddictionary = dictionaryconstruct()
            self.newsetup = newsetup
            self.parent = parent
            self.currentDatabase = self.parent.currentData
            self.root = tk.Tk()
            self.root.title("Create new question(Do include '?' character in question name)")
            self.frame = tk.Frame(self.root)
            self.loadOptions = findProjects()
            storeObj = lastkey(self)
            if len(self.loadOptions) == 0:
                self.loadOptions = ['No questions exist']
            self.loadOptionVariable = tk.StringVar(self.root)
            self.loadOptionVariable.set('Existing questions')
            tk.Label(self.frame, text="Question name :").grid(row=0, column=1)
            self.entryProject = tk.Entry(self.frame)
            self.entryProject.grid(row=0, column=3)
            tk.Label(self.frame, text="Load existing setup :").grid(row=0, column=5)
            self.selectload = tk.OptionMenu(self.frame, self.loadOptionVariable, *self.loadOptions)
            self.selectload.grid(row=0, column=7)
            self.loadButton = tk.Button(self.frame, text="Load", command=self.loadExistingProjectSet)
            self.loadButton.grid(row=0, column=9)
            self.saveButton = tk.Button(self.frame, text="Save", command=self.saveDialog)
            self.saveButton.grid(row=0, column=11)
            tk.Label(self.frame, text="a =").grid(row=1, column=0)
            self.entryA = tk.Entry(self.frame)
            self.entryA.grid(row=1, column=1)
            tk.Label(self.frame, text="b =").grid(row=1, column=2)
            self.entryB = tk.Entry(self.frame)
            self.entryB.grid(row=1, column=3)
            tk.Label(self.frame, text="c =").grid(row=1, column=4)
            self.entryC = tk.Entry(self.frame)
            self.entryC.grid(row=1, column=5)
            tk.Label(self.frame, text="d =").grid(row=1, column=6)
            self.entryD = tk.Entry(self.frame)
            self.entryD.grid(row=1, column=7)
            tk.Label(self.frame, text="e =").grid(row=1, column=8)
            self.entryE = tk.Entry(self.frame)
            self.entryE.grid(row=1, column=9)
            tk.Label(self.frame, text="f =").grid(row=1, column=10)
            self.entryF = tk.Entry(self.frame)
            self.entryF.grid(row=1, column=11)
            tk.Label(self.frame, text="g =").grid(row=2, column=0)
            self.entryG = tk.Entry(self.frame)
            self.entryG.grid(row=2, column=1)
            tk.Label(self.frame, text="h =").grid(row=2, column=2)
            self.entryH = tk.Entry(self.frame)
            self.entryH.grid(row=2, column=3)
            tk.Label(self.frame, text="i =").grid(row=2, column=4)
            self.entryI = tk.Entry(self.frame)
            self.entryI.grid(row=2, column=5)
            tk.Label(self.frame, text="j =").grid(row=2, column=6)
            self.entryJ = tk.Entry(self.frame)
            self.entryJ.grid(row=2, column=7)
            tk.Label(self.frame, text="k =").grid(row=2, column=8)
            self.entryK = tk.Entry(self.frame)
            self.entryK.grid(row=2, column=9)
            tk.Label(self.frame, text="l =").grid(row=2, column=10)
            self.entryL = tk.Entry(self.frame)
            self.entryL.grid(row=2, column=11)
            tk.Label(self.frame, text="m =").grid(row=3, column=0)
            self.entryM = tk.Entry(self.frame)
            self.entryM.grid(row=3, column=1)
            tk.Label(self.frame, text="n =").grid(row=3, column=2)
            self.entryN = tk.Entry(self.frame)
            self.entryN.grid(row=3, column=3)
            tk.Label(self.frame, text="o =").grid(row=3, column=4)
            self.entryO = tk.Entry(self.frame)
            self.entryO.grid(row=3, column=5)
            tk.Label(self.frame, text="p =").grid(row=3, column=6)
            self.entryP = tk.Entry(self.frame)
            self.entryP.grid(row=3, column=7)
            tk.Label(self.frame, text="q =").grid(row=3, column=8)
            self.entryQ = tk.Entry(self.frame)
            self.entryQ.grid(row=3, column=9)
            tk.Label(self.frame, text="r =").grid(row=3, column=10)
            self.entryR = tk.Entry(self.frame)
            self.entryR.grid(row=3, column=11)
            tk.Label(self.frame, text="s =").grid(row=4, column=0)
            self.entryS = tk.Entry(self.frame)
            self.entryS.grid(row=4, column=1)
            tk.Label(self.frame, text="t =").grid(row=4, column=2)
            self.entryT = tk.Entry(self.frame)
            self.entryT.grid(row=4, column=3)
            tk.Label(self.frame, text="u =").grid(row=4, column=4)
            self.entryU = tk.Entry(self.frame)
            self.entryU.grid(row=4, column=5)
            tk.Label(self.frame, text="v =").grid(row=4, column=6)
            self.entryV = tk.Entry(self.frame)
            self.entryV.grid(row=4, column=7)
            tk.Label(self.frame, text="w =").grid(row=4, column=8)
            self.entryW = tk.Entry(self.frame)
            self.entryW.grid(row=4, column=9)
            tk.Label(self.frame, text="x =").grid(row=4, column=10)
            self.entryX = tk.Entry(self.frame)
            self.entryX.grid(row=4, column=11)
            tk.Label(self.frame, text="y =").grid(row=5, column=0)
            self.entryY = tk.Entry(self.frame)
            self.entryY.grid(row=5, column=1)
            tk.Label(self.frame, text="z =").grid(row=5, column=2)
            self.entryZ = tk.Entry(self.frame)
            self.entryZ.grid(row=5, column=3)
            self.frame.pack()
            self.root.protocol("WM_DELETE_WINDOW", handle)
            self.root.mainloop()
    def saveDialog(self):# save Dialog
        def handle():# used to destroy gui
            self.savePopupGuiNotification = False
            self.saveroot.destroy()
        if self.savePopupGuiNotification == False:
            self.saveroot = tk.Tk()
            self.framesave = tk.Frame(self.saveroot)
            projectname = self.entryProject.get()
            if len(projectname) == 0:
                #projectname
                tk.Label(self.framesave, text="Please enter project name").grid(row=0, column=0)
                tk.Button(self.framesave, text="Okay", command=self.destroySaveDialog).grid(row=1, column=0)
            elif projectname not in self.loadOptions:
                tk.Label(self.framesave, text="Are you sure you want\nto save this setting?").grid(row=0, column=0)
                tk.Button(self.framesave, text="Yes", command=self.saveYesActions).grid(row=1, column=0)
                tk.Button(self.framesave, text="No", command=self.destroySaveDialog).grid(row=2, column=0)
            else:
                tk.Label(self.framesave, text="That project already exists!").grid(row=0, column=0)
                tk.Button(self.framesave, text="Okay", command=self.destroySaveDialog).grid(row=1, column=0)
            self.framesave.pack()
            self.saveroot.protocol("WM_DELETE_WINDOW", handle)
            self.saveroot.mainloop()
    def destroySaveDialog(self):
        self.saveroot.destroy()
        self.savePopupGuiNotification = False
    def loadExistingProjectSet(self):#This uploads data
        projectSetUp = self.loadOptionVariable.get()
        datapath = getdatapath()
        filelocation = datapath + "\\BaseBot\\"+projectSetUp+'\\events.json'
        with open(filelocation) as json_file:
            datadictionary = json.load(json_file)
        print(datadictionary)
        self.entryA.delete(0, tk.END)
        self.entryA.insert(0, datadictionary['a'])
        self.entryB.delete(0, tk.END)
        self.entryB.insert(0, datadictionary['b'])
        self.entryC.delete(0, tk.END)
        self.entryC.insert(0, datadictionary['c'])
        self.entryD.delete(0, tk.END)
        self.entryD.insert(0, datadictionary['d'])
        self.entryE.delete(0, tk.END)
        self.entryE.insert(0, datadictionary['e'])
        self.entryF.delete(0, tk.END)
        self.entryF.insert(0, datadictionary['f'])
        self.entryG.delete(0, tk.END)
        self.entryG.insert(0, datadictionary['g'])
        self.entryH.delete(0, tk.END)
        self.entryH.insert(0, datadictionary['h'])
        self.enterI.delete(0, tk.END)
        self.enterI.insert(0, datadictionary['i'])
        self.enterJ.delete(0, tk.END)
        self.enterJ.insert(0, datadictionary['j'])
        self.enterK.delete(0, tk.END)
        self.enterK.insert(0, datadictionary['k'])
        self.enterL.delete(0, tk.END)
        self.enterL.insert(0, datadictionary['l'])
        self.enterM.delete(0, tk.END)
        self.enterM.insert(0, datadictionary['m'])
        self.enterN.delete(0, tk.END)
        self.enterN.insert(0, datadictionary['n'])
        self.enterO.delete(0, tk.END)
        self.enterO.insert(0, datadictionary['o'])
        self.enterP.delete(0, tk.END)
        self.enterP.insert(0, datadictionary['p'])
        self.enterQ.delete(0, tk.END)
        self.enterQ.insert(0, datadictionary['q'])
        self.enterR.delete(0, tk.END)
        self.enterR.insert(0, datadictionary['r'])
        self.enterS.delete(0, tk.END)
        self.enterS.insert(0, datadictionary['s'])
        self.enterT.delete(0, tk.END)
        self.enterT.insert(0, datadictionary['t'])
        self.enterU.delete(0, tk.END)
        self.enterU.insert(0, datadictionary['u'])
        self.enterV.delete(0, tk.END)
        self.enterV.insert(0, datadictionary['v'])
        self.enterW.delete(0, tk.END)
        self.enterW.insert(0, datadictionary['w'])
        self.enterX.delete(0, tk.END)
        self.enterX.insert(0, datadictionary['x'])
        self.enterY.delete(0, tk.END)
        self.enterY.insert(0, datadictionary['y'])
        self.enterZ.delete(0, tk.END)
        self.enterZ.insert(0, datadictionary['z'])
    def saveYesActions(self):#This action saves the data for later
        datapath = getdatapath()
        project = 'mkdir "'+datapath+'\\BaseBot\\'+str(self.entryProject.get())+'"'
        self.savePopupGuiNotification = False
        os.system(project)
        #useddictionary.letterdiction
        #assign character descriptions
        self.parent.StringProject.set(self.entryProject.get())
        self.parent.StringA.set(str('a = ')+ self.entryA.get())
        useddictionary.assignletter('a', self.entryA.get())
        self.parent.StringB.set(str('b = ') + self.entryB.get())
        useddictionary.assignletter('b', self.entryB.get())
        self.parent.StringC.set(str('c = ') + self.entryC.get())
        useddictionary.assignletter('c', self.entryC.get())
        self.parent.StringD.set(str('d = ') + self.entryD.get())
        useddictionary.assignletter('d', self.entryD.get())
        self.parent.StringE.set(str('e = ') + self.entryE.get())
        useddictionary.assignletter('e', self.entryE.get())
        self.parent.StringF.set(str('f = ') + self.entryF.get())
        useddictionary.assignletter('f', self.entryF.get())
        self.parent.StringG.set(str('g = ') + self.entryG.get())
        useddictionary.assignletter('g', self.entryG.get())
        self.parent.StringH.set(str('h = ') + self.entryH.get())
        useddictionary.assignletter('h', self.entryH.get())
        self.parent.StringI.set(str('i = ') + self.entryI.get())
        useddictionary.assignletter('i', self.entryI.get())
        self.parent.StringJ.set(str('j = ') + self.entryJ.get())
        useddictionary.assignletter('j', self.entryJ.get())
        self.parent.StringK.set(str('k = ') + self.entryK.get())
        useddictionary.assignletter('k', self.entryK.get())
        self.parent.StringL.set(str('l = ') + self.entryL.get())
        useddictionary.assignletter('l', self.entryL.get())
        self.parent.StringM.set(str('m = ') + self.entryM.get())
        useddictionary.assignletter('m', self.entryM.get())
        self.parent.StringN.set(str('n = ') + self.entryN.get())
        useddictionary.assignletter('n', self.entryN.get())
        self.parent.StringO.set(str('o = ') + self.entryO.get())
        useddictionary.assignletter('o', self.entryO.get())
        self.parent.StringP.set(str('p = ') + self.entryP.get())
        useddictionary.assignletter('p', self.entryP.get())
        self.parent.StringQ.set(str('q = ') + self.entryQ.get())
        useddictionary.assignletter('q', self.entryQ.get())
        self.parent.StringR.set(str('r = ') + self.entryR.get())
        useddictionary.assignletter('r', self.entryR.get())
        self.parent.StringS.set(str('s = ') + self.entryS.get())
        useddictionary.assignletter('s', self.entryS.get())
        self.parent.StringT.set(str('t = ') + self.entryT.get())
        useddictionary.assignletter('t', self.entryT.get())
        self.parent.StringU.set(str('u = ') + self.entryU.get())
        useddictionary.assignletter('u', self.entryU.get())
        self.parent.StringV.set(str('v = ') + self.entryV.get())
        useddictionary.assignletter('v', self.entryV.get())
        self.parent.StringW.set(str('w = ') + self.entryW.get())
        useddictionary.assignletter('w', self.entryW.get())
        self.parent.StringX.set(str('x = ') + self.entryX.get())
        useddictionary.assignletter('x', self.entryX.get())
        self.parent.StringY.set(str('y = ') + self.entryY.get())
        useddictionary.assignletter('y', self.entryY.get())
        self.parent.StringZ.set(str('z = ') + self.entryZ.get())
        useddictionary.assignletter('z', self.entryZ.get())
        print(useddictionary.letterdiction)
        datapath = getdatapath()
        eventfile = datapath+'\\BaseBot\\'+str(self.entryProject.get())+'\\events.json'

        ########################################################################
        ###Save database to json use binary statement to descriminate between prompts ify on the binary statement
        if self.newsetup == False:
            databasepath = datapath+'\\BaseBot\\'+str(self.entryProject.get())+'\\database.json'
            with open(databasepath, "w") as outdata:
                json.dump(self.parent.currentData, outdata)
            outdata.close()
        ########################################################################

        with open(eventfile, "w") as outfile:
            json.dump(useddictionary.letterdiction, outfile)
        outfile.close()
        if self.newsetup == True:
            self.parent.currentData = dict()
            self.parent.wipeTrainingListDataGui()
        self.parent.createNewSetupGuiPresent = False
        self.savePopupGuiNotification = False
        self.saveroot.destroy()
        #self.root.mainloop()
        self.root.destroy()
    #def saveCharacters(self):


class maindialog:
    def __init__ (self):
        def exitProgramDialog():#this Deletes all guis when the main gui is destroyed
            try:#Delete Main Dialog
                self.root.destroy()
            except:
                emptyval = True
            try:#Delete training list GUI
                self.trainingListRoot.destroy()
            except:
                emptyval = True
            try:#Delete deleteExistingProjectGUI
                self.deleteOptionRoot.destroy()
            except:
                emptyval = True
            try:#Delete loadExistingProjectGUI
                self.loadoptionsroot.destroy()
            except:
                emptyval = True
            try:# delete Create new project notification Gui
                self.wipeNoteRoot.destroy()
            except:
                emptyval = True
            try:
                self.setupObject.root.destroy()
            except:
                emptyval = True
            try:
                self.sequenceGuiRoot.destroy()
            except:
                emptyval = True
            try:
                storeObj.lastkey.root.destroy()
            except:
                emptyval = True
        def testbinding(event):
            print(event.char)
            sevent = str(event)
            cursorindex = int(self.enterdata.index(tk.INSERT))
            subs = sevent[23:24]
            secondlet = sevent[24:25]
            print('subs')
            print(subs)
            print('secondlet')
            print(secondlet)
            print('sevent')
            print(sevent)
            self.prediction(event.char, secondlet, cursorindex)
        self.currentincrementmax = 30
        #######GUI DIALOG CONTROL TOOLS###########
        self.listTrainingGuiPresent = False
        self.deleteExistingProjectGuiPresent = False
        self.deleteConfirmationDialogPresent = False
        self.loadExistingProjectGuiPresent = False
        self.createProjectNotificationGuiPresent = False
        self.createNewSetupGuiPresent = False
        self.wipeData4NewProjectNotificationGuiPresent = False
        self.sequenceExplainationGuiPresent = False
        ##########################################
        self.alternativeHypothesises = []
        self.workingsequences = []
        self.stringHypothesisFits = []
        self.previousConclusions = {}
        self.currentYesCount = 0
        self.currentData = dict()
        self.currentTree = dict()
        self.bestmatches = []
        self.terminalYes = []
        self.terminalNo = []
        self.root = tk.Tk()
        self.projectedoutcome = tk.StringVar(self.root)
        self.MainDialogId = tk.StringVar(self.root)#used to check if gui is active
        self.MainDialogId.set('maindialog')
        self.projectedoutcome.set('No')
        self.root.title("BaseBot (Use lowercase letters only!)")
        self.idListDisplay = tk.StringVar(self.root)
        self.idListDisplay.set('')
        self.sequenceListDisplay = tk.StringVar(self.root)
        self.sequenceListDisplay.set('')
        self.outcomeListDisplay = tk.StringVar(self.root)
        self.outcomeListDisplay.set('')
        self.bestHypothesisListDisplay = tk.StringVar(self.root)
        self.bestHypothesisListDisplay.set('')
        self.frame = tk.Frame(self.root)
        self.StringProject = tk.StringVar(self.root)
        self.ProjectLabel = tk.Label(self.frame, textvariable=self.StringProject)
        self.ProjectLabel.grid(row=2, column=4)
        self.SelectModeLabel = tk.Label(self.frame, text="Enter sequence    :")
        self.SelectModeLabel.grid(row=1, column=0)
        self.enterdata = tk.Entry(self.frame)
        self.currentString = tk.StringVar()
        ###This is causing issue
        self.currentString.set('No')

        self.enterdata.grid(row=1, column=1)
        self.enterdata.bind('<Key>', testbinding)
        #self.enterdata.bind('<Key>', lastchar)
        self.predictionnotifier = tk.Label(self.frame, text="Prediction    :")
        self.predictionnotifier.grid(row=1, column=2)
        self.currentprediction = tk.Label(self.frame, textvariable=self.projectedoutcome)
        self.currentprediction.grid(row=1, column=3)
        self.yesbutton = tk.Button(self.frame, text="Yes", command=self.yesPress)
        self.casenotification = tk.Label(self.frame, text="Based on sequence :")
        self.casenotification.grid(row=1, column=4)
        self.reasonvariable = tk.StringVar(self.root)
        self.reasonvariable.set('')
        self.reasondisplay = tk.Label(self.frame, textvariable=self.reasonvariable)
        self.reasondisplay.grid(row=1, column=5)
        self.yesbutton.grid(row=2, column=1)
        self.nobutton = tk.Button(self.frame, text="No", command=self.noPress)
        self.nobutton.grid(row=2, column=2)
        self.currentproject = tk.Label(self.frame, text="Current question :")
        self.currentproject.grid(row=2, column=3)
        self.possibleoutcomes = tk.Label(self.frame, text="Select outcome :")
        self.possibleoutcomes.grid(row=2, column=0)
        self.loadproject = tk.Button(self.frame, text="Load existing question", command=self.loadExistingProject)
        self.loadproject.grid(row=2, column=5)
        self.StringA = tk.StringVar(self.root)
        self.StringA.set("a = (empty description)")
        self.buttonA = tk.Label(self.frame, textvariable=self.StringA)
        self.buttonA.grid(row=3, column=0)
        self.StringB = tk.StringVar(self.root)
        self.StringB.set("b = (empty description)")
        self.buttonB = tk.Label(self.frame, textvariable=self.StringB)
        self.buttonB.grid(row=3, column=1)
        self.StringC = tk.StringVar(self.root)
        self.StringC.set("c = (empty description)")
        self.buttonC = tk.Label(self.frame, textvariable=self.StringC)
        self.buttonC.grid(row=3, column=2)
        self.StringD = tk.StringVar(self.root)
        self.StringD.set("d = (empty description)")
        self.buttonD = tk.Label(self.frame, textvariable=self.StringD)
        self.buttonD.grid(row=3, column=3)
        self.StringE = tk.StringVar(self.root)
        self.StringE.set("e = (empty description)")
        self.buttonE = tk.Label(self.frame, textvariable=self.StringE)
        self.buttonE.grid(row=3, column=4)
        self.StringF = tk.StringVar(self.root)
        self.StringF.set("f = (empty description)")
        self.buttonF = tk.Label(self.frame, textvariable=self.StringF)
        self.buttonF.grid(row=3, column=5)
        self.StringG = tk.StringVar(self.root)
        self.StringG.set("g = (empty description)")
        self.buttonG = tk.Label(self.frame, textvariable=self.StringG)
        self.buttonG.grid(row=4, column=0)
        self.StringH = tk.StringVar(self.root)
        self.StringH.set("h = (empty description)")
        self.buttonH = tk.Label(self.frame, textvariable=self.StringH)
        self.buttonH.grid(row=4, column=1)
        self.StringI = tk.StringVar(self.root)
        self.StringI.set("i = (empty description)")
        self.buttonI = tk.Label(self.frame, textvariable=self.StringI)
        self.buttonI.grid(row=4, column=2)
        self.StringJ = tk.StringVar(self.root)
        self.StringJ.set("j = (empty description)")
        self.buttonJ = tk.Label(self.frame, textvariable=self.StringJ)
        self.buttonJ.grid(row=4, column=3)
        self.StringK = tk.StringVar(self.root)
        self.StringK.set("k = (empty description)")
        self.buttonK = tk.Label(self.frame, textvariable=self.StringK)
        self.buttonK.grid(row=4, column=4)
        self.StringL = tk.StringVar(self.root)
        self.StringL.set("l = (empty description)")
        self.buttonL = tk.Label(self.frame, textvariable=self.StringL)
        self.buttonL.grid(row=4, column=5)
        self.StringM = tk.StringVar(self.root)
        self.StringM.set("m = (empty description)")
        self.buttonM = tk.Label(self.frame, textvariable=self.StringM)
        self.buttonM.grid(row=5, column=0)
        self.StringN = tk.StringVar(self.root)
        self.StringN.set("n = (empty description)")
        self.buttonN = tk.Label(self.frame, textvariable=self.StringN)
        self.buttonN.grid(row=5, column=1)
        self.StringO = tk.StringVar(self.root)
        self.StringO.set("o = (empty description)")
        self.buttonO = tk.Label(self.frame, textvariable=self.StringO)
        self.buttonO.grid(row=5, column=2)
        self.StringP = tk.StringVar(self.root)
        self.StringP.set("p = (empty description)")
        self.buttonP = tk.Label(self.frame, textvariable=self.StringP)
        self.buttonP.grid(row=5, column=3)
        self.StringQ = tk.StringVar(self.root)
        self.StringQ.set("q = (empty description)")
        self.buttonQ = tk.Label(self.frame, textvariable=self.StringQ)
        self.buttonQ.grid(row=5, column=4)
        self.StringR = tk.StringVar(self.root)
        self.StringR.set("r = (empty description)")
        self.buttonR = tk.Label(self.frame, textvariable=self.StringR)
        self.buttonR.grid(row=5, column=5)
        self.StringS = tk.StringVar(self.root)
        self.StringS.set("s = (empty description)")
        self.buttonS = tk.Label(self.frame, textvariable=self.StringS)
        self.buttonS.grid(row=6, column=0)
        self.StringT = tk.StringVar(self.root)
        self.StringT.set("t = (empty description)")
        self.buttonT = tk.Label(self.frame, textvariable=self.StringT)
        self.buttonT.grid(row=6, column=1)
        self.StringU = tk.StringVar(self.root)
        self.StringU.set("u = (empty description)")
        self.buttonU = tk.Label(self.frame, textvariable=self.StringU)
        self.buttonU.grid(row=6, column=2)
        self.StringV = tk.StringVar(self.root)
        self.StringV.set("v = (empty description)")
        self.buttonV = tk.Label(self.frame, textvariable=self.StringV)
        self.buttonV.grid(row=6, column=3)
        self.StringW = tk.StringVar(self.root)
        self.StringW.set("w = (empty description)")
        self.buttonW = tk.Label(self.frame, textvariable=self.StringW)
        self.buttonW.grid(row=6, column=4)
        self.StringX = tk.StringVar(self.root)
        self.StringX.set("x = (empty description)")
        self.buttonX = tk.Label(self.frame, textvariable=self.StringX)
        self.buttonX.grid(row=6, column=5)
        self.StringY = tk.StringVar(self.root)
        self.StringY.set("y = (empty description)")
        self.buttonY = tk.Label(self.frame, textvariable=self.StringY)
        self.buttonY.grid(row=7, column=2)
        self.StringZ = tk.StringVar(self.root)
        self.StringZ.set("z = (empty description)")
        self.buttonZ = tk.Label(self.frame, textvariable=self.StringZ)
        self.buttonZ.grid(row=7, column=3)
        self.resetButton = tk.Button(self.frame, text='Reset data', command=self.resetCurrentData)
        self.resetButton.grid(row=7, column=0)
        self.listSequences = tk.Button(self.frame, text='List training data', command=self.listTrainingDataGui)
        self.listSequences.grid(row=8, column=0)
        self.CreateSetupbutton = tk.Button(self.frame, text="Create new question", command=self.createSetup)#create new project
        self.CreateSetupbutton.grid(row=8, column=1)
        self.savesetup = tk.Button(self.frame, text="Save question", command=self.saveProjectSetUp)
        self.savesetup.grid(row=8, column=4)
        self.explainationbutton = tk.Button(self.frame, text="Sequence explaination", command=self.sequenceformexplaination)
        self.explainationbutton.grid(row=7, column=5)
        self.deleteExistingProject = tk.Button(self.frame, text="Delete existing question", command=self.deleteExistingProject)
        self.deleteExistingProject.grid(row=8, column=5)
        self.frame.pack(padx=10, pady=10)
        self.root.protocol("WM_DELETE_WINDOW", exitProgramDialog)
        self.root.mainloop()
    def add2SequenceDataDisplay(self):#Dead code
        oldIdList = self.idListDisplay.get()
    def resetCurrentData(self):
        self.currentData = dict()
        self.workingsequences = []
        self.reasonstring = ''
        self.reasonvariable.set(self.reasonstring)
        self.wipeTrainingListDataGui()
    def updateTrainingListDataGui(self):#Update training data in GUI
        try:
            self.idDisplay.set(self.idListDisplay.get())
            self.sequenceDisplay.set(self.sequenceListDisplay.get())
            self.outcomeDisplay.set(self.outcomeListDisplay.get())
            self.bestHypothesisDisplay.set(self.bestHypothesisListDisplay.get())
        except:
            nothing = 'nothing'
    def wipeTrainingListDataGui(self):#reset all current project data
        try:
            self.idListDisplay.set('')
            self.sequenceListDisplay.set('')
            self.outcomeListDisplay.set('')
            self.bestHypothesisListDisplay.set('')
            self.updateTrainingListDataGui()
        except:
            nothing = 'nothing'
    def listTrainingDataGui(self):# Gui That lists training data
        self.trainingdictionary = dict()
        self.trainingdictionary[30] = dict()
        self.trainingdictionary[30]['id'] = []
        self.trainingdictionary[30]['sequence'] = []
        self.trainingdictionary[30]['outcome'] = []
        self.trainingdictionary[30]['hypothesis'] = []
        self.currentincrementmax = 30 #30 for 1-30, 60 for 31-60, 90 for 61-90, ect..
        def handle():# Destroy Gui when done
            self.listTrainingGuiPresent = False#makes it possible to bring the gui back after it has been destroyed
            self.trainingListRoot.destroy()
        def add2ListDictionary(id, sequence, outcome, hypothesis):
            if id > self.currentincrementmax:
                self.currentincrementmax = self.currentincrementmax + 30
                self.trainingdictionary[self.currentincrementmax] = dict()
                self.trainingdictionary[self.currentincrementmax]['id'] = []
                self.trainingdictionary[self.currentincrementmax]['sequence'] = []
                self.trainingdictionary[self.currentincrementmax]['outcome'] = []
                self.trainingdictionary[self.currentincrementmax]['hypothesis'] = []
            self.trainingdictionary[self.currentincrementmax]['id'].append(id)
            self.trainingdictionary[self.currentincrementmax]['sequence'].append(sequence)
            self.trainingdictionary[self.currentincrementmax]['outcome'].append(outcome)
            self.trainingdictionary[self.currentincrementmax]['hypothesis'].append(hypothesis)

        if self.listTrainingGuiPresent == False:#Gui is only created if the Gui is not already present
            self.trainingListRoot = tk.Tk()
            self.trainingListRoot.title('Training data')
            self.trainingListFrame = tk.Frame(self.trainingListRoot)
            self.screenDisplay = dict()
            #self.myscrollbar = tk.Scrollbar(self.trainingListFrame, orient='vertical')
            #self.myscrollbar.grid(column=4, row=1, rowspan=1)
            #self.scrollbar = tk.Scrollbar(self.trainingListRoot)
            #self.scrollbar.pack(side = RIGHT, Fill = Y)
            self.listTrainingGuiPresent = True
            self.idDisplay = tk.StringVar(self.trainingListRoot)
            self.idDisplay.set(self.idListDisplay.get())
            self.sequenceDisplay = tk.StringVar(self.trainingListRoot)
            self.sequenceDisplay.set(self.sequenceListDisplay.get())
            self.outcomeDisplay = tk.StringVar(self.trainingListRoot)
            self.outcomeDisplay.set(self.outcomeListDisplay.get())
            self.bestHypothesisDisplay = tk.StringVar(self.trainingListRoot)
            self.bestHypothesisDisplay.set(self.bestHypothesisListDisplay.get())
            self.entryDisplayVariable = tk.StringVar(self.trainingListRoot)
            self.entryDisplayVariable.set('1-20')
            #########scroll data information###################################
            #self.previousButton = tk.Button(self.trainingListFrame, text="<-")
            #self.previousButton.grid(column=0, row =0)
            #tk.Label(self.trainingListFrame, textvariable=self.entryDisplayVariable).grid(column=1, row=0)
            #self.nextButton = tk.Button(self.trainingListFrame, text="->")
            #self.nextButton.grid(column=2, row=0)
            ###################################################################
            tk.Label(self.trainingListFrame, text=" ID ").grid(column=0, row=1)
            tk.Label(self.trainingListFrame, text=" Sequence ").grid(column=1, row=1)
            tk.Label(self.trainingListFrame, text=" Outcome ").grid(column=2, row=1)
            tk.Label(self.trainingListFrame, text=" Best hypothesis ").grid(column=3, row=1)
            tk.Label(self.trainingListFrame, textvariable=self.idDisplay).grid(column=0, row=2)
            tk.Label(self.trainingListFrame, textvariable=self.sequenceDisplay).grid(column=1, row=2)
            tk.Label(self.trainingListFrame, textvariable=self.outcomeDisplay).grid(column=2, row=2)
            tk.Label(self.trainingListFrame, textvariable=self.bestHypothesisDisplay).grid(column=3, row=2)

            self.trainingListFrame.pack(pady=10, padx=50)
            self.trainingListRoot.protocol("WM_DELETE_WINDOW", handle)
            self.trainingListRoot.mainloop()
    def deleteExistingProject(self):# Prompt GUI to delete existing project
        def handle():
            self.deleteExistingProjectGuiPresent = False#makes it possible to bring the gui back after it has been destroyed
            self.deleteOptionRoot.destroy()
        self.loadOpt = findProjects()
        if self.deleteExistingProjectGuiPresent == False:#Gui is only created if the Gui is not already present
            self.deleteExistingProjectGuiPresent = True
            if len(self.loadOpt) == 0:
                self.loadOpt = ['No projects exist']
            self.deleteOptionRoot = tk.Tk()
            self.deleteExistingProjectGuiStat = tk.StringVar(self.deleteOptionRoot)
            self.deleteExistingProjectGuiStat.set('Exist')
            self.deleteOptionFrame = tk.Frame(self.deleteOptionRoot)
            self.strDelProjVar = tk.StringVar(self.deleteOptionRoot)
            self.strDelProjVar.set('Select question')
            tk.Label(self.deleteOptionFrame, text="Select question").grid(row=0, column=0)
            self.delOptionDrop = tk.OptionMenu(self.deleteOptionFrame, self.strDelProjVar, *self.loadOpt)
            self.delOptionDrop.grid(row=1, column=0)
            self.delProjectButton = tk.Button(self.deleteOptionFrame, text="Delete", command=self.deleteConfirmationDialog)
            self.delProjectButton.grid(row=2, column=0)
            self.deleteOptionFrame.pack()
            self.deleteOptionRoot.protocol("WM_DELETE_WINDOW", handle)
            self.deleteOptionRoot.mainloop()
    def deleteConfirmationDialog(self):#happens when you press yes on delete project button
        def handle():
            self.deleteConfirmationDialogPresent = False#makes it possible to bring the gui back after it has been destroyed
            self.delConRoot.destroy()
        if self.deleteConfirmationDialogPresent == False:#Gui is only created if the Gui is not already present
            self.deleteConfirmationDialogPresent = True
            project = self.strDelProjVar.get()
            message = "Are you sure you want\n to delete "+project+"?"
            self.delConRoot = tk.Tk()
            self.delConFrame = tk.Frame(self.delConRoot)
            tk.Label(self.delConFrame, text=message).grid(row=0, column=0)
            tk.Button(self.delConFrame, text="Yes", command=self.deleteProjectAction).grid(row=1, column=0)
            tk.Button(self.delConFrame, text="No", command=self.delConRoot.destroy).grid(row=2, column=0)
            self.delConFrame.pack()
            self.delConRoot.protocol("WM_DELETE_WINDOW", handle)
            self.delConRoot.mainloop()
    def deleteProjectAction(self):# actually deletes said project
        datapath = getdatapath()
        command = datapath+'\\BaseBot\\'+str(self.strDelProjVar.get())
        #This stuff destroys associated GUIs
        self.deleteConfirmationDialogPresent = False
        self.deleteExistingProjectGuiPresent = False
        directory = command.replace('del ', '')
        files = os.listdir(directory)
        for file in files:
            file2remove = datapath+'\\BaseBot\\'+str(self.strDelProjVar.get())+'\\'+file
            os.remove(file2remove)
        os.rmdir(directory)
        self.StringProject.set('')
        self.delConRoot.destroy()
        #self.delConRoot.forget()
        self.deleteOptionRoot.destroy()
        #self.deleteOptionRoot.forget()
    def loadExistingProject(self):#Prompt load Project GUI
        def handle():
            self.loadExistingProjectGuiPresent = False#makes it possible to bring the gui back after it has been destroyed
            self.loadoptionsroot.destroy()
        self.loadOpt = findProjects()
        if self.loadExistingProjectGuiPresent == False:#Gui is only created if the Gui is not already present
            self.loadExistingProjectGuiPresent = True
            print(self.loadOpt)
            if len(self.loadOpt) == 0:
                self.loadOpt = ['No projects exist']
            self.loadoptionsroot = tk.Tk()
            self.loadoptionsframe = tk.Frame(self.loadoptionsroot)
            self.strloadvar = tk.StringVar(self.loadoptionsroot)
            self.strloadvar.set('Select question')
            tk.Label(self.loadoptionsframe, text="Select question").grid(row=0, column=0)
            self.loadoptiondrop = tk.OptionMenu(self.loadoptionsframe, self.strloadvar, *self.loadOpt)
            self.loadoptiondrop.grid(row=1, column=0)
            tk.Button(self.loadoptionsframe, text="Load", command=self.loadExistingProjectAction).grid(row=2, column=0)
            self.loadoptionsframe.pack()
            self.loadoptionsroot.protocol("WM_DELETE_WINDOW", handle)
            self.loadoptionsroot.mainloop()
    def loadExistingProjectAction(self):
        proj = self.strloadvar.get()
        self.loadExistingProjectGuiPresent = False
        self.StringProject.set(proj)
        datapath = getdatapath()
        sequence = datapath + '\\BaseBot\\' + str(self.strloadvar.get()) + '\\sequence.json'
        try:
            with open(sequence) as json_sequence:
                sequencefile = json.load(json_sequence)
            self.reasonvariable.set(sequencefile['sequence'])
        except:
            self.reasonvariable.set('No sequence found')
        datafilelocation = datapath + '\\BaseBot\\' + str(self.strloadvar.get()) + '\\database.json'
        with open(datafilelocation) as json_file:
            datadictionary = json.load(json_file)
        newdiction = convertJsontoIntdic(datadictionary)

        #######
        self.idListDisplay.set('')
        self.sequenceListDisplay.set('')
        self.outcomeListDisplay.set('')
        self.bestHypothesisListDisplay.set('')
        for id in newdiction:
            currentId = id
            currentIdStr = self.idListDisplay.get()
            currentSequenceStr = self.sequenceListDisplay.get()
            currentOutcomeStr = self.outcomeListDisplay.get()
            currentHypothesisStr = self.bestHypothesisListDisplay.get()
            newIdStr = currentIdStr + str(currentId) + '\n'
            sequenceString = ''
            for index in newdiction[id]['string']:
                sequenceString = sequenceString + str(newdiction[id]['string'][index])
            newSequenceStr = currentSequenceStr + sequenceString + '\n'
            newOutcomeStr = currentOutcomeStr + str(newdiction[id]['outcome']) + '\n'
            print(newdiction[id])
            try:
                print(newdiction[id]['hypothesis'])
                newHypothesisStr = currentHypothesisStr + str(newdiction[id]['hypothesis']) + '\n'
                self.bestHypothesisListDisplay.set(newHypothesisStr)
            except:
                exception = 'exists'
            self.sequenceListDisplay.set(newSequenceStr)
            self.idListDisplay.set(newIdStr)
            self.outcomeListDisplay.set(newOutcomeStr)
            self.updateTrainingListDataGui()
        self.currentData = newdiction
        json_file.close()
        datapath = getdatapath()
        eventsfilelocation = datapath + '\\BaseBot\\' + str(self.strloadvar.get()) + '\\events.json'
        with open(eventsfilelocation) as description:
            descriptiondict = json.load(description)
        useddictionary = dictionaryconstruct()
        for x in descriptiondict:
            assignment = descriptiondict[x]
            print(x)
            x = str(x)
            assignment = str(assignment)
            useddictionary.assignletter(str(x), str(assignment))
        #dictionaryconstruct.letterdiction['a']
        self.StringA.set('a = ' + useddictionary.letterdiction['a'])
        self.StringB.set('b = ' + useddictionary.letterdiction['b'])
        self.StringC.set('c = ' + useddictionary.letterdiction['c'])
        self.StringD.set('d = ' + useddictionary.letterdiction['d'])
        self.StringE.set('e = ' + useddictionary.letterdiction['e'])
        self.StringF.set('f = ' + useddictionary.letterdiction['f'])
        self.StringG.set('g = ' + useddictionary.letterdiction['g'])
        self.StringH.set('h = ' + useddictionary.letterdiction['h'])
        self.StringI.set('i = ' + useddictionary.letterdiction['i'])
        self.StringJ.set('j = ' + useddictionary.letterdiction['j'])
        self.StringK.set('k = ' + useddictionary.letterdiction['k'])
        self.StringL.set('l = ' + useddictionary.letterdiction['l'])
        self.StringM.set('m = ' + useddictionary.letterdiction['m'])
        self.StringN.set('n = ' + useddictionary.letterdiction['n'])
        self.StringO.set('o = ' + useddictionary.letterdiction['o'])
        self.StringP.set('p = ' + useddictionary.letterdiction['p'])
        self.StringQ.set('q = ' + useddictionary.letterdiction['q'])
        self.StringR.set('r = ' + useddictionary.letterdiction['r'])
        self.StringS.set('s = ' + useddictionary.letterdiction['s'])
        self.StringT.set('t = ' + useddictionary.letterdiction['t'])
        self.StringU.set('u = ' + useddictionary.letterdiction['u'])
        self.StringV.set('v = ' + useddictionary.letterdiction['v'])
        self.StringW.set('w = ' + useddictionary.letterdiction['w'])
        self.StringX.set('x = ' + useddictionary.letterdiction['x'])
        self.StringY.set('y = ' + useddictionary.letterdiction['y'])
        self.StringZ.set('z = ' + useddictionary.letterdiction['z'])
        self.loadoptionsroot.destroy()
    def yesPress(self):#This is what happens when you press yes
        presentvalue = self.currentString.get()
        currentdatlen = len(self.currentData)
        newindex = len(self.currentData) + 1
        currentIdListDisplay = self.idListDisplay.get()
        newIdListDisplay = currentIdListDisplay + str(newindex) + '\n'
        self.idListDisplay.set(newIdListDisplay)
        currentSequenceListDisplay = self.sequenceListDisplay.get()
        newSequenceListDisplay = currentSequenceListDisplay + str(presentvalue) + '\n'
        self.sequenceListDisplay.set(newSequenceListDisplay)
        currentOutcomeDisplay = self.outcomeListDisplay.get()
        newOutcomeDisplay = currentOutcomeDisplay + 'yes\n'
        self.outcomeListDisplay.set(newOutcomeDisplay)
        self.updateTrainingListDataGui()
        if len(presentvalue) > 0:
            nextindex = currentdatlen + 1
            self.currentData[nextindex] = dict()
            self.currentData[nextindex]['string'] = dict()
            charactercounter = 1
            for x in presentvalue:
                self.currentData[nextindex]['string'][charactercounter] = x
                charactercounter = charactercounter + 1
            self.currentData[nextindex]['outcome'] = 'yes'
            self.enterdata.delete(0, charactercounter)
        self.currentString.set('')
        self.buildTree()
        self.currentData[nextindex]['hypothesis'] = str(self.reasonvariable.get())

        self.outcomeListDisplay.set(newOutcomeDisplay)
        currentHypothesisDisplay = self.bestHypothesisListDisplay.get()
        if len(self.reasonstring) == 0:
            self.fixemptyreasonvariable()
        listlistreasons = convertStringReason2List(self.reasonstring)
        filtered = filterDuplicateNodes(listlistreasons)
        stringreason = ''
        for fil in filtered:
            if len(fil[0]) != 1:
                continue
            th = convertListReason2String(fil)
            stringreason = stringreason + th
        self.reasonstring = stringreason
        if len(self.reasonstring) == 0:
            self.reasonstring = 'Not enough data'
        self.currentData[nextindex]['hypothesis'] = self.reasonstring
        self.reasonvariable.set(self.reasonstring)
        reason = self.reasonstring
        newBestHypothesisListDisplay = currentHypothesisDisplay + self.reasonstring + '\n'
        self.bestHypothesisListDisplay.set(newBestHypothesisListDisplay)
        try:#bug fix
            self.bestHypothesisDisplay.set(self.bestHypothesisListDisplay.get())
        except:
            print('bug fix exception')
        print(self.previousConclusions)

    def noPress(self):#this happens when you press no button
        presentvalue = self.currentString.get()
        currentdatlen = len(self.currentData)
        newindex = len(self.currentData) + 1
        currentIdListDisplay = self.idListDisplay.get()
        newIdListDisplay = currentIdListDisplay + str(newindex) + '\n'
        self.idListDisplay.set(newIdListDisplay)
        currentSequenceListDisplay = self.sequenceListDisplay.get()
        newSequenceListDisplay = currentSequenceListDisplay + str(presentvalue) + '\n'
        self.sequenceListDisplay.set(newSequenceListDisplay)
        currentOutcomeDisplay = self.outcomeListDisplay.get()
        newOutcomeDisplay = currentOutcomeDisplay + 'no\n'
        self.outcomeListDisplay.set(newOutcomeDisplay)
        self.updateTrainingListDataGui()
        if len(presentvalue) > 0:
            nextindex = currentdatlen + 1
            self.currentData[nextindex] = dict()
            self.currentData[nextindex]['string'] = dict()
            charactercounter = 1
            for x in presentvalue:
                self.currentData[nextindex]['string'][charactercounter] = x
                charactercounter = charactercounter + 1
            self.currentData[nextindex]['outcome'] = 'no'
            self.enterdata.delete(0, charactercounter)
        self.currentString.set('')
        self.buildTree()
        if len(self.reasonstring) == 0:
            self.fixemptyreasonvariable()
        listlistreasons = convertStringReason2List(self.reasonstring)
        filtered = filterDuplicateNodes(listlistreasons)
        stringreason = ''
        for fil in filtered:
            if len(fil[0]) != 1:
                continue
            th = convertListReason2String(fil)
            stringreason = stringreason + th
        self.reasonstring = stringreason

        self.currentData[nextindex]['hypothesis'] = str(self.reasonvariable.get())

        self.outcomeListDisplay.set(newOutcomeDisplay)
        currentHypothesisDisplay = self.bestHypothesisListDisplay.get()
        if len(self.reasonstring) == 0:
            self.reasonstring = 'Not enough data'
        self.currentData[nextindex]['hypothesis'] = self.reasonstring
        self.reasonvariable.set(self.reasonstring)
        reason = self.reasonstring
        print('reason ' + self.reasonstring)
        newBestHypothesisListDisplay = currentHypothesisDisplay + self.reasonstring + '\n'
        print('check '+newBestHypothesisListDisplay)
        self.bestHypothesisListDisplay.set(newBestHypothesisListDisplay)
        print('ok '+self.bestHypothesisListDisplay.get())
        try:  # bug fix
            self.bestHypothesisDisplay.set(self.bestHypothesisListDisplay.get())
        except:
            print('bug fix exception')
        print(self.previousConclusions)
        print('reasonstring')
        print(self.reasonstring)
        print('len')
        print(len(self.reasonstring))
        print('workingsequences')
        print(self.workingsequences)

        #print(seeker.yesoutcomes)
        #print(self.currentData)
    def saveData(self):# saves current project data to the hard drive
        if len(str(self.StringProject.get())) == 0:
            self.noteroot = tk.Tk()
            self.noteframe = tk.Frame(self.noteroot)
            tk.Label(self.noteframe, text="Project must have a name to be saved.").grid(row=0, column=0)
            tk.Button(self.noteframe, text='OK', command=self.noteroot.destroy).grid(row=1, column=0)
            self.noteframe.pack()
            self.noteroot.mainloop()
        else:
            datapath = getdatapath()
            saveDataLocation = datapath + '\\BaseBot\\'+str(self.StringProject.get())+'\\database.json'
            saveUniqueSequence = datapath+'\\BaseBot\\'+str(self.StringProject.get())+'\\sequence.json'
            sequencedump = dict()
            sequencedump['sequence'] = self.reasonvariable.get()
            try:
                with open(saveUniqueSequence, 'w') as outsequence:
                    json.dump(sequencedump, outsequence)
            except:
                print('*')
            with open(saveDataLocation, "w") as outfile:
                json.dump(self.currentData, outfile)
            outfile.close()
    def createProjectInstruction(self):
        self.noteroot = tk.TK()
        self.noteframe = tk.Frame(self.noteroot)
        tk.Label(self.noteframe, text="Project must have a name to be saved.")
        tk.Button(self.noteframe, text='OK', command=self.noteroot.destroy)
    def saveProjectSetUp(self):# happens when you press the save button
        if len(self.StringProject.get()) == 0:
            setupdialog(self, False)
            self.setCharDescriptions()
        else:
            self.saveData()
    def createSetup(self):# happens when you press create project
        if self.wipeData4NewProjectNotificationGuiPresent == False and self.createNewSetupGuiPresent == False:
            self.wipeData4NewProjectNotification()
    def wipeData4NewProjectNotification(self):#wipes old data for new project
        def handle():
            self.wipeData4NewProjectNotificationGuiPresent = False
            self.wipeNoteRoot.destroy()
        if self.wipeData4NewProjectNotificationGuiPresent == False:
            self.wipeData4NewProjectNotificationGuiPresent = True
            self.wipeNoteRoot = tk.Tk()
            self.wipeNoteFrame = tk.Frame(self.wipeNoteRoot)
            tk.Label(self.wipeNoteFrame, text='Are you sure you want\nto wipe your current work\nand create a new question?').grid(row=0, column=0)
            tk.Button(self.wipeNoteFrame, text="Yes", command=self.wipeData4newProject).grid(row=1, column=0)
            tk.Button(self.wipeNoteFrame, text="No", command=handle).grid(row=2, column=0)
            self.wipeNoteFrame.pack()
            self.wipeNoteRoot.protocol("WM_DELETE_WINDOW", handle)
            self.wipeNoteRoot.mainloop()
    def wipeData4newProject(self):
        self.wipeData4NewProjectNotificationGuiPresent = False
        self.wipedata = True
        self.wipeNoteRoot.destroy()
        self.workingsequences = [] # clear memory of working sequences
        self.previousConclusions = dict()# reset dictionary
        self.reasonstring = ''
        self.reasonvariable.set(self.reasonstring)
        self.setupObject = setupdialog(self, True)
        self.setCharDescriptions()
    def setCharDescriptions(self):
        #print(useddictionary.letterdiction)
        self.StringA.set(useddictionary.letterdiction['a'])
        #print(self.StringA)
        self.StringB.set(useddictionary.letterdiction['b'])
        self.StringC.set(useddictionary.letterdiction['c'])
        self.StringD.set(useddictionary.letterdiction['d'])
        self.StringE.set(useddictionary.letterdiction['e'])
        self.StringF.set(useddictionary.letterdiction['f'])
        self.StringG.set(useddictionary.letterdiction['g'])
        self.StringH.set(useddictionary.letterdiction['h'])
        self.StringI.set(useddictionary.letterdiction['i'])
        self.StringJ.set(useddictionary.letterdiction['j'])
        self.StringK.set(useddictionary.letterdiction['k'])
        self.StringL.set(useddictionary.letterdiction['l'])
        self.StringM.set(useddictionary.letterdiction['m'])
        self.StringN.set(useddictionary.letterdiction['n'])
        self.StringO.set(useddictionary.letterdiction['o'])
        self.StringP.set(useddictionary.letterdiction['p'])
        self.StringQ.set(useddictionary.letterdiction['q'])
        self.StringR.set(useddictionary.letterdiction['r'])
        self.StringS.set(useddictionary.letterdiction['s'])
        self.StringT.set(useddictionary.letterdiction['t'])
        self.StringU.set(useddictionary.letterdiction['u'])
        self.StringV.set(useddictionary.letterdiction['v'])
        self.StringW.set(useddictionary.letterdiction['w'])
        self.StringX.set(useddictionary.letterdiction['x'])
        self.StringY.set(useddictionary.letterdiction['y'])
        self.StringZ.set(useddictionary.letterdiction['z'])
    def prediction(self, firstKey, secondKey, charindex):#provides current prediction for current string
        new = self.enterdata.get()
        outputsetting = 'No'
        #self.enterdata.bind('<Key>', lastchar)
        print('prediction')
        print(new)
        print('char')
        print(firstKey)
        newstr = new+firstKey
        ###########Not certain what this was for########################################
        '''
        if secondKey == ' ':
            newstr = new[:charindex] + firstKey + new[charindex:]
        elif firstKey == 'B' and secondKey == 'a':
            newstr = self.currentString.get()
            leng = len(newstr)
            min = leng - 1
            newstr = newstr[:min]
        '''
        ####################################################################################
        presentvalue = self.currentString.get()
        currentData = {}
        currentdatlen = len(newstr)
        print(currentdatlen)
        # This is code copied from above

        if len(newstr) > 0:
            nextindex = currentdatlen + 1
            currentData[1] = {}
            currentData[1]['string'] = {}
            charactercounter = 1
            for x in newstr:

                currentData[1]['string'][charactercounter] = x
                charactercounter = charactercounter + 1
            currentData[1]['outcome'] = 'yes'
            #self.enterdata.delete(0, charactercounter)
        yesconditions = []
        yesreason = []
        yesstatus = False
        for list in self.terminalYes:
            results = NoSqlBuilder.godClassicallyHateDinos(list, currentData)
            print('list')
            print(list)
            print('currentData')
            print(currentData)
            dict = results.returndictionary
            print(dict)
            if dict['yes'] > 0:
                yesstatus = True
                yesconditions.append(list)
        matchstat = False
        singlet = convertSinglet2DatabaseFormat(newstr, 'yes')
        if len(self.workingsequences) > 0 and len(newstr) > 0:
            for x in self.workingsequences:
                data = NoSqlBuilder.godClassicallyHateDinos(x, singlet)
                yeses = data.returndictionary['yes']
                if yeses > 0:
                    matchstat = True
        if yesstatus == True and len(self.workingsequences) == 0:
            self.projectedoutcome.set('Yes')
        elif matchstat == True:
            self.projectedoutcome.set('Yes')
        else:
            self.projectedoutcome.set('No')


        #reason = self.reasonvariable.get()
        self.currentString.set('')
        self.currentString.set(newstr)
    def buildTree(self):# A new tree is built every time you assign an outcome to a string of events
        decisiontree = buildtree(self.currentData)
        self.workingsequences = decisiontree.workingsequences
        self.currentTree = decisiontree.tree
        print(decisiontree.tree)
        self.terminalYes = decisiontree.yesoutcomes
        self.terminalNo = decisiontree.nooutcomes
        yescount = 0
        for case in self.currentData:
            if self.currentData[case]['outcome'] == 'yes':
                yescount = yescount + 1
        self.currentYesCount = yescount
        print(decisiontree.yesoutcomes)
        print(decisiontree.nooutcomes)
        print(decisiontree.reasonstring)
        print(decisiontree.workingsequences)
        if decisiontree.reasonstring not in self.previousConclusions and decisiontree.reasonstring != '':
            self.previousConclusions[decisiontree.reasonstring] = {}
            self.previousConclusions[decisiontree.reasonstring]['workinglists'] = decisiontree.workingsequences
            for list in decisiontree.workingsequences:
                stringlist = convertListReason2String(list)
                self.previousConclusions[decisiontree.reasonstring][stringlist] = {}
                self.previousConclusions[decisiontree.reasonstring][stringlist]['list'] = list
                checklist = NoSqlBuilder.godClassicallyHateDinos(list, self.currentData)
                if yescount == checklist.returndictionary['yes'] and yescount != 0:
                    self.previousConclusions[decisiontree.reasonstring][stringlist]['validitystat'] = True
                else:
                    self.previousConclusions[decisiontree.reasonstring][stringlist]['validitystat'] = False
        self.updatePreviousConclusions()
        '''for x in decisiontree.workingsequences:
            secondDecision = NoSqlBuilder.buildsecoundarytree(x, self.currentData, decisiontree.projectEntropy)
            for y in secondDecision.bestmatches:
                self.bestmatches.append(y)'''
        self.reasonstring = decisiontree.reasonstring
        print('previousconclusions')
        print(self.previousConclusions)
        print('workingsequences')
        print(decisiontree.workingsequences)
        print('beststrings')
        print(self.bestmatches)
        print('yesnodes')
        print(self.stringHypothesisFits)
        self.listconvertedstrings = []
        for str in self.stringHypothesisFits:
            conversion = convertStringReason2List(str)
            print('conversion')
            print(conversion)
            for lis in conversion:
                self.listconvertedstrings.append(lis)
        #print(secondDecision.yesnodes)
        if len(decisiontree.reasonstring) == 0:
            nodes2remember = []
            nodestr2remember = []
            for x in self.listconvertedstrings:
                secondDecision = NoSqlBuilder.buildsecoundarytree(x, self.currentData, decisiontree.projectEntropy)
                print('list')
                print(x)
                print('yesnodessecondary')
                print(secondDecision.yesnodes)
                print('tree')
                print(secondDecision.tree)
                for node in secondDecision.bestmatches:
                    strnode = convertListReason2String(node)
                    if strnode not in nodestr2remember:
                        nodes2remember.append(node)
                        nodestr2remember.append(strnode)
            if len(nodes2remember) == 0:
                #if len(self.alternativeHypothesises) == 0:
                self.reasonstring = 'Not enough data'
                self.reasonvariable.set('Not enough data.')
                workinglists = []
                for hypo in self.stringHypothesisFits:
                    convert = convertStringReason2List(hypo)
                    for list in convert:
                        searchObj = NoSqlBuilder.godClassicallyHateDinos(list, self.currentData)
                        if searchObj.returndictionary['yes'] == self.currentYesCount and searchObj.returndictionary['no'] == 0:
                            workinglists.append(list)
                if len(workinglists) > 0:
                    reason = ''
                    for li in workinglists:
                        str = convertListReason2String(li)
                        reason = reason + str
                    self.reasonstring = reason
                    self.reasonstring = reasonOutputValidation(self.currentData, self.reasonstring, self.currentYesCount)
                    self.reasonvariable.set(self.reasonstring)
                    if self.reasonstring == '':
                        self.fixemptyreasonvariable()

            else:
                self.reasonstring = ''
                for str in nodestr2remember:
                    self.reasonstring = self.reasonstring + str
                self.reasonstring = reasonOutputValidation(self.currentData, self.reasonstring, self.currentYesCount)
                self.reasonvariable.set(self.reasonstring)
                if self.reasonstring == '':
                    self.fixemptyreasonvariable()
                #if statement is for blankreason bug
        else:
            self.reasonstring = decisiontree.reasonstring
            validated = reasonOutputValidation(self.currentData, self.reasonstring, self.currentYesCount)
            self.reasonstring = validated
            self.reasonvariable.set(self.reasonstring)
            #self.reasonvariable.set(str(self.bestmatch))
    def fixemptyreasonvariable(self):#self described bug fix
        if len(self.reasonstring) == 0:
            returnthis = ''
            filterlists = filterDuplicateNodes(self.workingsequences)
            for x in filterlists:
                stringedlist = convertListReason2String(x)
                returnthis = returnthis + stringedlist
            self.reasonstring = returnthis
            self.reasonvariable.set(self.reasonstring)

    def fetchdata(self):
        print(self.enterdata.get())
    def sequenceformexplaination(self):
        def handle():# Destroy Gui when done
            self.sequenceExplainationGuiPresent = False#makes it possible to bring the gui back after it has been destroyed
            self.sequenceGuiRoot.destroy()
        if self.sequenceExplainationGuiPresent == False:
            self.sequenceExplainationGuiPresent = True
            self.sequenceGuiRoot = tk.Tk()
            self.sequenceGuiFrame = tk.Frame(self.sequenceGuiRoot)
            textLineOne = '[a, b] sequence contains "a" and "b" like the following sequences: \n\n"cab" "albert" "brain"\n\n"'
            textLineTwo = '[a, b#+1] sequence contains an "a" with a "b" one letter to the right of "a" like sequences\n\n' \
                          '"cabbage" "cab" "dable"\n\n'
            textLineThree = '[a, b#-1] sequence contains an "a" with a "b" one letter to the left of "a" like sequences\n\n' \
                            '"baggage" "back" "bam"\n\n'
            textLineFour = '[a, b#+1, c#-3] sequence contains an "a" with a "b" one letters to the right of "a"\n' \
                           'and a "c" three letters to the left of that "b" like sequences\n\n' \
                           '"cab" "cabbage"\n\n'
            textLineFive = '[k, #-3b] sequence contains a "k" with a "b" three letters to the left of "k" like sequence\n\n' \
                           '"back"'
            textuse = textLineOne + textLineTwo + textLineThree + textLineFour + textLineFive
            self.label = tk.Label(self.sequenceGuiFrame, text=textuse)
            self.label.grid(row=0, column=0)
            self.sequenceGuiFrame.pack(padx=15, pady=15)
            self.sequenceGuiRoot.protocol("WM_DELETE_WINDOW", handle)
            self.sequenceGuiRoot.mainloop()

    def updatePreviousConclusions(self):
        self.stringHypothesisFits = []
        self.alternativeHypothesises = []
        for hypothesis in self.previousConclusions:
            for sub in self.previousConclusions[hypothesis]:
                if 'workinglists' not in sub:
                    currentlist = self.previousConclusions[hypothesis][sub]['list']
                    yesfetch = NoSqlBuilder.godClassicallyHateDinos(currentlist, self.currentData)
                    if yesfetch.returndictionary['yes'] != self.currentYesCount:
                        self.previousConclusions[hypothesis][sub]['validitystat'] = False
                    elif yesfetch.returndictionary['yes'] == self.currentYesCount:
                        self.stringHypothesisFits.append(sub)
                        self.previousConclusions[hypothesis][sub]['validitystat'] = True
                        self.alternativeHypothesises.append(currentlist)





class selectdatasetup:
    def __init__(self):

        self.root = tk.Tk()
        self.frame = tk.Frame(self.root)
        tk.Label(self.frame, text = "Assign custom values or skip to use default a,b,c,d,...z val")
#createDirectory()
#findProjects()
maindialog()
#setupdialog()