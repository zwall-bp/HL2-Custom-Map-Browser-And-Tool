'''
Created on Jul 19, 2020

@author: Zach Wallace (BP)

Half Life 2 Custom Map Compiler.

A tool which helps streamlines the process of creating custom maps/map packs which make use of
the Source Engine's bonus map feature.
'''

import argparse as ap
import json as js
from pathlib import Path
from shutil import copy, rmtree
#Pack Data
from libraries.map import GameMap
from libraries.pack import GamePack
#BNS parser
from libraries import bnsParser as bns

"""
    Takes a map instance, copies all of the files, and exports to
    ./exports/<MAP NAME CLEANED UP>

    The folder could then be drag/dropped into the game's custom folder.
"""
def ExportMap(pMap: GameMap, EXPORT_DIR: str = "./exports"):
    #Get the path for where we will be exporting.
    strAddonName = GetCleanName(pMap.getName())
    strPath = EXPORT_DIR + "/" + strAddonName
    strPathPack = strPath + "/maps"
    pPath = Path(strPath)
    pPathPack = Path(strPathPack)

    #Check to make sure it doesn't exist.
    if(pPath.exists()):
        #The base directory exists, ask the user if they want to quit the operation.
        if not RaiseOverwrite(strAddonName):
            return
        #They are fine with any overwrites. Continue.
        else:
            rmtree(strPath)

    pPathPack.mkdir(parents=True, exist_ok=True)
    #We now copy over the contents of the bns.

    #Map File. (.bsp)
    copy(pMap.getMap(), strPathPack)

    #Thumbnail File (.tga) (Optional)
    if pMap.hasImage():
        #Now check to see if it's only a given path.
        if not pMap.usingPIL():
            #Just a thumbnail image given, copy over to the export.
            copy(pMap.getThumbnail(), strPathPack)
        #We've got a custom image. Time to compile and export it!
        else:
            #Set the name of the thumbnail to the addon name.
            pMap.compileCustomImage(strPathPack + "/" + strAddonName + ".tga")

    #BNS File. (.bns)
    bns.save(pMap.compileInstance(), open(strPathPack + "/" + strAddonName + ".bns", "w"))

    return

"""
    Takes a pack instance, copies all of the files, and exports to
    ./exports/<PACK NAME CLEANED UP>
"""
def ExportPack(pPack: GamePack, EXPORT_DIR: str = "./exports"):
    #Get the path for where we will be exporting.
    strAddonName = GetCleanName(pPack.getName())
    strPath = EXPORT_DIR + "/" + strAddonName
    strPathMap = strPath + "/maps/"
    strPathPack = strPathMap + strAddonName
    pPath = Path(strPath)
    pPathPack = Path(strPathPack)

    #Check to make sure it doesn't exist.
    if(pPath.exists()):
        #The base directory exists, ask the user if they want to quit the operation.
        if not RaiseOverwrite(strAddonName):
            return
        #They are fine with any overwrites. Continue.
        else:
            rmtree(strPath)

    pPathPack.mkdir(parents=True, exist_ok=True)
    #We now copy over the maps first.
    #Go over each instance, and do the same thing we see in a normal map export.
    for pMap in pPack.getMaps():
        #Map File. (.bsp)
        copy(pMap.getMap(), strPathMap)

        #Thumbnail File (.tga) (Optional)
        if pMap.hasImage():
            #Now check to see if it's only a given path.
            if not pMap.usingPIL():
                #Just a thumbnail image given, copy over to the export.
                copy(pMap.getThumbnail(), strPathPack)
            #We've got a custom image. Time to compile and export it!
            else:
                #Set the name of the thumbnail to the addon name.
                pMap.compileCustomImage(strPathPack + "/" + GetCleanName(pMap.getName()) + ".tga")

    #BNS File. (.bns)
    bns.save(pPack.compileMaps(), open(strPathPack + "/" + strAddonName + ".bns", "w"))
    #Folder Info (.bns)
    bns.save(pPack.compileInstance(), open(strPathPack + "/folderinfo.bns", "w"))
    #Thumbnail File (.tga) (Optional)
    if pPack.hasImage():
        #Now check to see if it's only a given path.
        if not pPack.usingPIL():
            #Just a thumbnail image given, copy over to the export.
            copy(pPack.getThumbnail(), strPathPack)
        #We've got a custom image. Time to compile and export it!
        else:
            #Set the name of the thumbnail to the addon name.
            pPack.compileCustomImage(strPathPack + "/foldericon.tga")

    return

"""
    Creates a clean, UNIX friendly string
"""
def GetCleanName(strName: str):
    #We should first cut off the path, and only have the file name itself.
    if "/" in strName:
        strName = strName[strName.rfind("/") + 1:]
    strNewName = ""
    strExtention = ""
    #Check to see if we still have a file extention in the new name.
    if "." in strName:
        nDotIdx = strName.rfind(".")
        strExtention = strName[nDotIdx:].lower()
        #Clip it out so it doesn't interfere with the new name loop.
        strName = strName[:nDotIdx]
    for char in strName:
        #Check to see if the character is a letter.
        if char.isalpha():
            strNewName = strNewName + char.lower()
        #If it's a space, we instead convert it to a hyphen for readability.
        elif char == " ":
            strNewName = strNewName + "-"
    #Finished looping though all characters.
    #Check to make sure we got something by the end.
    if strNewName == "":
        raise Exception("The given name could not be cleaned!")
    return strNewName + strExtention

"""
    The current export exists. Ask the user if they want to continue
    and overwrite.

    Returns True if it's fine to overwrite.
"""
def RaiseOverwrite(strName: str):
    #Get the user's input.
    strInput = input(f"The project \"{strName}\" already exists!\nWould you like to overwrite it?\nY/[N]> ").lower()
    #Check to see if they want to go though.
    if strInput == "y":
        return True
    else:
        return False

if __name__ == "__main__":

    parser = ap.ArgumentParser(description= "A Source Engine bonus map packager. Takes a bsp/image file and some text and outputs a functioning custom folder or an importable bonus zip file.")

    parser.add_argument("-g", "--gui", action="store_true", help="Opens up the GUI tool for easier editing.")
    parser.add_argument("-s", "--single", action="store_true", help="Flags that you will be compiling for a single map.")
    parser.add_argument("-p", "--pack", action="store_true", help="Flags that you will be compiling a map pack.")
    parser.add_argument("-n", "--name", help="The name you would like to give your map.")
    parser.add_argument("-m", "--map", help="The path to the .bsp file.")
    parser.add_argument("-c", "--comment", help="The text you would like to show up in the comment.")
    parser.add_argument("-i", "--image", help="The path to an image file you would like to use.\n(Will try and auto-fix one if the image isn't the exact 9:5 aspect ratio. Be warned, it won't be exact.)")
    parser.add_argument("-l", "--lock", action="store_true", help="Will flag that the map should be locked by default.")
    parser.add_argument("-z", "--zip", action="store_true", help="Will flag that the map should be zipped into an importable .bnz file.\n(This is best used with map packs due to the import)")
    parser.add_argument("-o", "--output", default="./exports", help="File path in which the compiled pack should output to.")
    parser.add_argument("-j", "--json", help="The path to a json file. For Maps: Instead of compiling, it will serialize the data into a .json file in order to be used in compiling packs. Setting a path to an existing .json will append onto it.\nFor Packs: A file path for the contents inside of the pack.")

    args = parser.parse_args()

    #Check to see if we want to use the GUI instead.
    if len(vars(args)) < 1 or args.gui:
        #GUI
        from libraries.gui.splashScreen import SplashScreen
        from libraries.gui.editorScreen import EditorScreen
        import gc
        pSplash = SplashScreen()
        strSelection = pSplash.GetSelection()

        if not strSelection:
            exit(0)

        gc.collect()

        pEditor = EditorScreen()

        exit(0)


    #Make sure there is either a single or pack.
    if not args.single != args.pack:
        #Both or neither are being used.
        if args.single:
            print("ERROR: Can't have both --single and --pack flagged.")
            exit(1)
        else:
            parser.print_help()
            exit(1)
    #Branch down different paths for whatever method we are using.
    if args.single:
        pMap = GameMap()
        #Set up all of the data inside of the instance.
        try:
            pMap.setName(args.name)
            pMap.setMap(args.map)
            if(args.comment):
                pMap.setComment(args.comment)
            #Check to see if there is an image path.
            if(args.image):
                #Auto set the image keyval just in case.
                pMap.setThumnail(args.image)
                pMap.loadPILImage(args.image)
            pMap.setLocked(args.lock)
        except ... as problem:
            print(problem)
            exit(1)
        #Save it.
        if args.json:
            #... as a serialized json file instead.
            try:
                #New File.
                with open(args.json, "x+") as file:
                    js.dump(pMap.compileInstance(), file, indent= 4)
            except FileExistsError:
                #Appending to file.
                with open(args.json, "r+") as file:
                    dictJSData = js.load(file)
                    file.seek(0)
                    file.truncate()
                    dictJSData.update(pMap.compileInstance())
                    js.dump(dictJSData, file, indent= 4)
            print(f"{pMap.getName()} has been successfully serialized into {args.json}!")
        else:
            ExportMap(pMap, args.output)
            print(f"{pMap.getName()} has been successfully been exported to {args.output}!")
        exit(0)
    #Map Pack
    else:
        pPack = GamePack()
        #Set up all the data inside of the instance.
        try:
            pPack.setName(args.name)
            if(args.comment):
                pPack.setComment(args.comment)
            #Check to see if there is an image path.
            if(args.image):
                pPack.loadPILImage(args.image)
            pPack.setLocked(args.lock)
            #Load in the maps for the pack.
            with open(args.json) as file:
                pPack.importMaps(js.load(file))
                #Iterate though each map instance, creating their thumbnail.
                for pMap in pPack.getMaps():
                    if pMap.hasImage():
                        pMap.loadPILImage(pMap.getThumbnail())
        except ...:
            print("A problem occured while compiling the map pack.")
            exit(1)
        #Save it.
        ExportPack(pPack, args.output)
        print(f"{pPack.getName()} has been successfully been exported to {args.output}!")
        exit(0)
