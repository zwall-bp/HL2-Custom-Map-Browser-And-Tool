'''
Created on Jul 28, 2020

@author: Zach Wallace (BP)

    Reads and writes .bns files. (Bonus map.)

    CLI allows for .bns/.json conversion
'''


"""
Reads the given file, and turns it into a dictionary.

strFileName: The path to the .bns.
"""
def load(strFileName):
    #Open the file and get its name.
    pFile = open(strFileName, "r")
    strFileName = pFile.name[:pFile.name.rfind("/") + 1]

    #Prepare the dictionary
    dictFile = {}
    strActiveKey = ""

    while (strLine := pFile.readline()):
        """
        In this loop, we are on the highest level of the bns.
        It should only contain the names of the maps, and then their respective keyvals after.

        Format:
        "Map Name"
        {
            Keyvals
        }
        "Another Map"
        {
            Keyvals
        }
        """

        #First check to make sure we have a squirly bracket. They indicate the start of a keyval pair.
        if "{" in strLine:
            #We have a squirly! Start the recursive loop go get all keyvals.
            dictFile[strActiveKey] = getKeyVals(pFile)
            continue

        #If this does end up here, that's actually a problem. We will try and fix it while parsing though.
        if "}" in strLine:
            strLine = pFile.readline()
            continue

        #If we get through all of that, it's safe to assume we only have the name of the map.
        #Get both sides of the name.
        intFirstInstance = strLine.find("\"")
        intSecondInstance = strLine.rfind("\"")

        #Check to make sure we did get both sides.
        if (not intFirstInstance == -1 and not intSecondInstance == -1):
            strActiveKey = strLine[intFirstInstance + 1:intSecondInstance]
        else:
            #Wasn't a key. We may have a problem.
            strActiveKey = strLine

        #Go back through the loop.
        continue

    pFile.close()

    return dictFile

"""
    Take the image file name, and check to see if it needs to be fixed up with either the PATH or ROOT.
"""
def loadImageDir(strFileName, PATH, ROOT):
    #Check to see if it has a relative path.
    if "./" in strFileName:
        strFileName = PATH + strFileName[strFileName.find("/") + 1:]
    #Check to see if it has a root path. (Starts at the mod's root.)
    elif "/" in strFileName:
        strFileName = ROOT + strFileName
    #The image is in the default materials path.
    else:
        strFileName = ROOT + "materials/" + strFileName
    #Now to return the value
    return strFileName

"""
    Returns the image file back to its original path.
"""
def saveImageDir(strFileName: str, bInPack: bool):
    strImageName = strFileName[strFileName.rfind("/") + 1:]
    #Check to see if it's apart of a pack.
    if bInPack:
        strImageName = "./" + strImageName
    #If it's just in a single map, set it from root.
    else:
        strImageName = "maps/" + strImageName
    return strImageName

"""
    Take the map file name, and check to see if it needs to be fixed up with either the PATH or ROOT.
"""
def loadMapDir(strFileName, PATH, ROOT):
    #Check to see if it has a relative path.
    if "./" in strFileName:
        strFileName = PATH + strFileName[strFileName.find("/") + 1:] + ".bsp"
    #Check to see if it has a root path. (Starts at the mod's root.)
    elif "/" in strFileName:
        strFileName = ROOT + strFileName + ".bsp"
    #The image is in the default materials path.
    else:
        strFileName = ROOT + "maps/" + strFileName + ".bsp"
    #Now to return the value
    return strFileName

"""
    Returns the map file back to its original path.

    strFileName: Path to the file.
"""
def saveMapDir(strFileName: str):
    strMapName = strFileName[strFileName.rfind("/") + 1:]

    #Now, remove the .bsp extention.
    strMapName = strMapName[:strMapName.find(".bsp")]

    return strMapName

"""
    While going through a file, iterate over everything inside of the current level of {}
    and return a dictionary of the found keyvals.
"""
def getKeyVals(pFile):
    #When we first enter, pFile should be on the "{". So reading the line should give us the first keyval pair.
    dictKeyVal = {}

    #Get the path to the bns and mod.
    PATH = pFile.name[:pFile.name.rfind("/") + 1]
    ROOT = PATH[:PATH.rfind("maps")]

    while not (strLine := pFile.readline()) in ["}", "}\n"]:
        #Find each pair through their use of quotation marks.
        intFirstInstance = strLine.find("\"")
        intSecondInstance = strLine.find("\"", intFirstInstance + 1)
        strKey = strLine[intFirstInstance + 1 : intSecondInstance]

        intFirstInstance = strLine.find("\"", intSecondInstance + 1)
        intSecondInstance = strLine.find("\"", intFirstInstance + 1)
        dictKeyVal[strKey] = strLine[intFirstInstance + 1 : intSecondInstance]

        #Convert image path to absolute.
        if strKey == "image":
            dictKeyVal[strKey] = loadImageDir(dictKeyVal[strKey], PATH, ROOT)
        elif strKey == "map":
            dictKeyVal[strKey] = loadMapDir(dictKeyVal[strKey], PATH, ROOT)

    #We hit a }! Time to return what we got!
    return dictKeyVal

def save(dictData, pFile):
    """
    pFile: open() instance.
    rData: Array of map info.

    Writes to pFile in .bns format.
    """

    #Clear the file of previous data.
    pFile.seek(0)
    pFile.truncate()

    for mapName, mapData in dictData.items():
        #Pack the map differently if it's in a pack.
        bInPack = mapData.pop("packed", False)

        #Write out the name of the map / pack, and add in the { at the correct place.
        pFile.write("\"" + mapName + "\"\n{\n")

        for key, val in mapData.items():
            if key == "image":
                val = saveImageDir(val, bInPack)
            elif key == "map":
                val = saveMapDir(val)
            pFile.write(f"\t\"{key}\"\t\"{val}\"\n")

        pFile.write("}\n")

if __name__ == "__main__":
    """
        Running the Python script by itself.
        Allow the user to either compile into vdf or json.
    """

    import argparse as ap
    import json as js

    parser = ap.ArgumentParser(description="A .BNS/.JSON converter.\nUsed as a module, allows you to convert .BNS files to dictionaries.")

    parser.add_argument("-b", "--bns", type=str ,help="The file path to a Bonus Map Description file.")
    parser.add_argument("-j", "--json", type=open ,help="The file path to a json file containing bonus map information.")
    parser.add_argument("-o", "--output", type=ap.FileType("w", encoding="utf-8"),help="The file path for where the converted data should go.")
    parser.add_argument("-p", "--print", action="store_true", help="Prints out the contents of the bonus map.")

    args = parser.parse_args()

    #First check to make sure both json and bns are not being used at once.
    if args.bns and args.json:
        print("ERROR: Can't have both --bns and --json flags!")
        exit(1)

    #Now to see if they are inputting in nothing.
    if not (args.bns or args.json):
        parser.print_help()
        exit(1)

    #BNS file.
    if args.bns:
        #Parse BNS
        dictData = load(args.bns)

        #Check to see if the user wants us to print.
        if(args.print):
            print(js.dumps(dictData, indent=4))

        #User wants to output as a json.
        if(args.output):
            js.dump(dictData, args.output, indent=4)

        #Exit out before fucking anything else up.
        exit(0)

    #JSON file.
    if args.json:
        #Parse JSON
        dictData = js.load(args.json)

        #Check to see if the user wants us to print.
        if(args.print):
            print(js.dumps(dictData, indent=4))

        #User wants to output as a json.
        if(args.output):
            save(dictData, args.output)

        #Exits out before fucking anything else up.
        exit(0)
