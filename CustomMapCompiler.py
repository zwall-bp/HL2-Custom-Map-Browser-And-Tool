'''
Created on Jul 19, 2020

@author: Zach Wallace (BP)

Half Life 2 Custom Map Compiler.

A tool which helps streamlines the process of creating custom maps/map packs which make use of
the Source Engine's bonus map feature.
'''

from libraries.compiler import *

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
    if not (args.single and args.pack):
        #GUI
        #I'll add in the splash screen later.
        #from libraries.gui.splashScreen import SplashScreen
        from libraries.gui.editorScreen import EditorScreen
        #pSplash = SplashScreen()
        #strSelection = pSplash.GetSelection()

        #if not strSelection:
        #    exit(0)

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
                pMap.setThumbnail(args.image)
                pMap.loadPILImage(args.image)
            pMap.setLocked(args.lock)
        except ... as problem:
            print(problem)
            exit(1)
        #Save it.
        if args.json:
            SaveData(pMap, args.json)
            print(f"{pMap.getName()} has been successfully serialized into {args.json}!")
        else:
            bForce = False
            while True:
                try:
                    ExportMap(pMap, args.output, bForce)
                    print(f"{pMap.getName()} has been successfully been exported to {args.output}!")
                    break
                except FileExistsError as strName:
                    #Get the user's input.
                    print(strName)
                    strInput = input(f"The project \"{pMap.getName()}\" already exists!\nWould you like to overwrite it?\nY/[N]> ").lower()
                    #Check to see if they want to go though.
                    if strInput == "y":
                        bForce = True
                    else:
                        break

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
        except Exception:
            print("A problem occured while compiling the map pack.")
            exit(1)
        #Save it.
        ExportPack(pPack, args.output)
        print(f"{pPack.getName()} has been successfully been exported to {args.output}!")
        exit(0)
