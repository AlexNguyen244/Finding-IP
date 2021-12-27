import sys

# Authors: Alex Nguyen (ID: 912141552), Michelle Karnadjaja (ID: 917297605)
# To run the program type: python ip2as.py DB_091803.txt IPlist.txt

# Initialize the lines from opening files
DB_091803 = open(sys.argv[1], "r")
DBTemp = DB_091803.readlines()
IPlist = open(sys.argv[2], "r")
IP = IPlist.readlines()

TempLen = len(DBTemp)-1 # The -1 is there due to the space at the end of the text file
IPTextLen = len(IP)

# Deletes the faulty lines in DB and stores it in a new array
def DeleteFaultyDB(DBTemp, TempLen): 
    DBArray = []
    nothing = 0
    for i in range(0, TempLen):
        GetDB = DBTemp[i]
        dot = [i for i, x in enumerate(GetDB) if x == '.']
        space = [i for i, x in enumerate(GetDB) if x == ' ']
        if(dot[0] == dot[1]-1 or dot[1] == dot[2]-1 or dot[2] == space[0]-1):
            nothing = 0
        else:
            DBArray.append(DBTemp[i])
    return DBArray

DB = DeleteFaultyDB(DBTemp, TempLen) # The new DB list without the faulty lines
DBTextLen = len(DB)

# The list of integers is converted to a list of binary
def ValueToBinaryList(values):
    binaryString = []
    string = [str(values) for values in values]
    isString = "".join(string)
    integer = int(isString)
    fullbin = bin(integer)[2:].zfill(16)
    blen = len(fullbin)
    for i in range(0, blen):
        binaryString.append(fullbin[i])
    return binaryString

 # Calculates the first number before the "." into a binary number
def firstNum(line):
    values = []
    for i in line:
        if i != '.':
            values.append(i)
        else:
            break
    for i in range(0, len(values)):
        values[i] = int(values[i])
    binaryString = ValueToBinaryList(values)
    return binaryString

def secondNum(line):
    indices = [i for i, x in enumerate(line) if x == '.']
    index1 = indices[0]+1
    index2 = indices[1]
    values = []
    for v in range(index1, index2):
        values.append(line[v])
    binaryString = ValueToBinaryList(values)
    return binaryString

def thirdNum(line):
    indices = [i for i, x in enumerate(line) if x == '.']
    index1 = indices[1]+1
    index2 = indices[2]
    values = []
    for v in range(index1, index2):
        values.append(line[v])
    binaryString = ValueToBinaryList(values)
    return binaryString  

def fourthNum(line):
    l = len(line)-1
    indices = [i for i, x in enumerate(line) if x == '.']
    index1 = indices[2]+1
    values = []
    for v in range(index1, l):
        values.append(line[v])
    binaryString = ValueToBinaryList(values)
    return binaryString

# Calculate the fourth number in the DB list until it reaches the space
def DBfourthNum(line): 
    indices = [i for i, x in enumerate(line) if x == '.']
    space = [i for i, x in enumerate(line) if x == ' ']
    index1 = indices[2]+1
    values = []
    for v in range(index1, space[0]):
        values.append(line[v])
    binaryString = ValueToBinaryList(values)
    return binaryString

 # Compares a full list of two binary numbers and returns the total match as counter
def CompareBinary(IP, DB, IPIndex, DBIndex):
    IPbin1 = firstNum(IP[IPIndex])
    IPbin2 = secondNum(IP[IPIndex])
    IPbin3 = thirdNum(IP[IPIndex])
    IPbin4 = fourthNum(IP[IPIndex])
    IPList = IPbin1 + IPbin2 + IPbin3 + IPbin4
    IPListlen = len(IPList)-1
    DBbin1 = firstNum(DB[DBIndex])
    DBbin2 = secondNum(DB[DBIndex])
    DBbin3 = thirdNum(DB[DBIndex])
    DBbin4 = DBfourthNum(DB[DBIndex])
    DPList = DBbin1 + DBbin2 + DBbin3 + DBbin4
    counter = 0
    for i in range(0, IPListlen):
        if IPList[i] == DPList[i]:
            counter = counter + 1
        else:
            break
    return counter

def LongestMatch(IP, DB, DBTextLen, IPIndex):
    counter = 0
    for i in range(0, DBTextLen):
        newcounter = CompareBinary(IP, DB, IPIndex, i)
        if newcounter >= counter:
            counter = newcounter
            BestDB = i
    return BestDB

def ASList(IP, DB, DBTextLen):
    BestDBArray = []
    IndexArray = []
    for i in range(0, IPTextLen):
        BestDB = LongestMatch(IP, DB, DBTextLen, i)
        if BestDB in IndexArray:  # If the IP is already used get the next best one
            NextBestDB = LongestMatch(IP, DB, BestDB, i)
            BestDBArray.append(DB[NextBestDB])
        else:
            IndexArray.append(BestDB)
            BestDBArray.append(DB[BestDB])
    return BestDBArray

# Convert the string of values into a single line
def StringtoLine(string): 
    fix = ""
    for i in string:
        fix += i
    return fix

def CreateTextFile(IP, DB, DBTextLen):
    file = open("output.txt", "w+")
    output = ASList(IP, DB, DBTextLen)
    outputLen = len(output)
    for y in range(0, outputLen):
        line = []
        getoutput = output[y]
        getoutlen = len(getoutput)-1
        space = [i for i, x in enumerate(getoutput) if x == ' ']
        space1 = space[0]
        space2 = space[1]
        for i in range(0, space1):
            line.extend(getoutput[i])
        line.extend('/')
        space1 = space1 + 1
        for j in range(space1, space2):
            line.extend(getoutput[j])
        for k in range(space2, getoutlen):
            line.extend(getoutput[k])
        line.extend(' ')
        addIP = IP[y] # Add the IP to the end of the line
        addIPLen = len(addIP)
        for l in range(0, addIPLen):
            line.extend(addIP[l])
        file.write(StringtoLine(line))

CreateTextFile(IP, DB, DBTextLen)
