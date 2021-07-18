'''
Created on Jun 22, 2021

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
def ExportMap(pMap: GameMap, EXPORT_DIR: str = "./exports", pForceExport: bool = False):
    #Get the path for where we will be exporting.
    strAddonName = GetCleanName(pMap.getName())
    strPath = EXPORT_DIR + "/" + strAddonName
    strPathPack = strPath + "/maps"
    pPath = Path(strPath)
    pPathPack = Path(strPathPack)

    #Check to make sure it doesn't exist.
    if(pPath.exists()):
        #The base directory exists, ask the user if they want to quit the operation.
        if pForceExport:
            rmtree(strPath)
        else:
            #Ask if they want to force it, and try again.
            RaiseOverwrite(strAddonName)
            return

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
def ExportPack(pPack: GamePack, EXPORT_DIR: str = "./exports", pForceExport: bool = False):
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
        if pForceExport:
            rmtree(strPath)
        else:
            #Ask if they want to force it, and try again.
            RaiseOverwrite(strAddonName)
            return

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
    dictData = pPack.compileInstance()
    #Remove the unessicary info.
    strPackName = list(dictData.keys())[0]
    dictData.pop("maps", None)
    dictData[strPackName].pop("image", None)
    dictData[strPackName].pop("imageX", None)
    dictData[strPackName].pop("imageY", None)
    dictData[strPackName].pop("imageScale", None)

    bns.save(dictData, open(strPathPack + "/folderinfo.bns", "w"))
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
Takes a dictionary and saves the data of it.
"""
def SaveData(pBonusInstance, strPath, bCompletelyClear = False):
    #... as a serialized json file instead.
    try:
        #New File.
        with open(strPath, "x+") as file:
            js.dump(pBonusInstance.compileInstance(), file, indent= 4)
    except FileExistsError:
        #Appending to file.
        with open(strPath, "r+") as file:
            dictJSData = js.load(file)
            file.seek(0)
            file.truncate()
            if bCompletelyClear:
                dictJSData = {}
            dictJSData.update(pBonusInstance.compileInstance())
            js.dump(dictJSData, file, indent= 4)

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
    raise FileExistsError(strName)
