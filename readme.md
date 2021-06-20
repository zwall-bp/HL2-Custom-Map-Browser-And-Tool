# BP's Custom Map Compiler And Browser
### For Half-Life 2 Mappers and Players
### By: [BP](https://steamcommunity.com/id/builderpro/)

## Table Of Contents

>**End User**
* [What Is This?](#what-is-this)
* [Map Packs](#map-packs)
* [Installing The Browser](#installing-the-browser)
* [Uninstalling The Browser](#uninstalling-the-browser)
* [Installing Maps](#installing-maps)
* [Managing Maps](#managing-maps)

>**Level Designer**
* [Compiling Your Own Maps (Command Line)](#compiling-your-own-maps-cli)
    * [Compiling A Single Map](#compiling-a-single-map-cli)
    * [Compiling A Map Pack](#compiling-a-map-pack-cli)
* [Command Line Arguments](#cli-arguments)
* GUI Tool. (Coming soon!)

## What Is This?
For those who have played a good amount of custom Half-Life 2 maps, you may understand that most level designers have you enter their map through means of the console. While this is the standard, it isn't a user-friendly approach. Some other people try to solve the issue by instead turning their map packs into mods. But, if the player wants to swap to a different map, not made by the developer, they would need to leave the game. That's where this tool comes in to help solve that problem.

Using the power of Source's [Bonus Map](https://developer.valvesoftware.com/wiki/Bonus_Maps) feature, we now have a means of sorting all of our installed custom maps in a single place!

<img src="./assets/Markdown/custom_browser.png" alt="Example of the custom map browser">

With this browser, level designer are able to:
* Create map packs, where the player can browse subdirectories filled with maps.
    * Packs inside of packs are also available for even more map!
* Catch player's attentions with the use of thumbnails.
    * With the compiling tool automatically generating the correct thumbnail specs.
* Credit themselves with the use of the comments.
* And the best part, no more needing to see an ugly bsp-friendly name. Add spaces, colons, and other characters to the name of your map!
* `[NOT YET IMPLEMENTED]` You can even pack your maps into a `.bmz` file for easier installation on the end user's side!

## Map Packs
Along with browsing single maps, by creating a subdirectory inside of `./maps` allows you to have a specified *map pack* in which you can give your own name, comment, and thumbnail.

<img src="./assets/Markdown/custom_pack_exterior.png" alt="The outside of Halloween Vile 4">
<img src="./assets/Markdown/custom_pack_interior.png" alt="The inside of Halloween Vile 4">

This allows for a much cleaner and modular experience for the end user.

> **TIP:** You can *lock* maps, which can then be [unlocked](https://developer.valvesoftware.com/wiki/Point_bonusmaps_accessor) when playing other maps to allow for a progression similar to that seen for the game's chapter select.

## Installing The Browser
### [You can find the download right here](https://github.com/sectopodwreck/HL2-Custom-Map-Browser-And-Tool/releases/tag/Browser)
Adding the map browser to your own game is extremely easy and unintrusive. Simply:
1. Copy the folder `./custom-map-explorer` to `[Steam Directory]/common/Half-Life 2/hl2/custom/`

And you're done.<br/>
Next time you boot up your game you will see a new menu option:

<img src="./assets/Markdown/hl2_menu.png" alt="Half-Life 2 Ep 2 menu with the custom maps option">

> **WARNING:** For users playing in a language other than English, you will be missing localization! To fix this, check out `./custom-map-explorer/resource/gameui_english.txt` to see what keyvals you will need to change for your own language.

## Uninstalling The Browser
Deleting the browser is just as easy as installing. Just:
1. Delete `[Steam Directory]/common/Half-Life 2/hl2/custom/custom-map-explorer`

And now you're game is back to factory settings.

## Installing Maps
> **Reminder:** The level designer must of made a folder using this tool in order for it to work. You cannot just drag and drop a `.bsp` file and get the same result.

**Unless it's specified by the level designer**, it's best to play all of the maps in *Half-Life 2: Episode 2*. Because of this, be sure to:
1. Copy the given folder into `[Steam Directory]/common/Half-Life 2/ep2/custom/`

With that done, it should now show up in the browser.

## Managing Maps
As we know, when it comes to the standard way of managing custom maps, end users drag and drop the `.bsp` into their `maps/` directory without a thought. Sometimes, there's extra assets which need to be installed into `materials/` and `models/`. This leads to very messy folders.

With the power of the Source Engine's `custom/` directory, for overwriting and adding assets, we can separate each map into their own folder to allow for easy installation and deletion of custom maps.

<img src="./assets/Markdown/hl2_custom_dir.png" alt="My custom/ directory with a bunch of maps">

## Compiling Your Own Maps (CLI)
Alright, now for the fun part. Level designers, you wanna use this tool to spice up your presentation? I know you do. :)

To get started, this tool hasn't been *frozen* yet, so **you will need to install [Python](https://www.python.org/downloads/)** in order to run the program. Python was chosen as I am on a Linux, and would like for this tool to be as portable as possible.

> WARNING: You will need to install PIL in order to run the program. To install this Python Package, simply:
```bash
python -m pip install pillow
```

To check out all arguments available, open a terminal in this directory and run the command:
```bash
python ./CustomMapCompiler.py --help
```

### Compiling A Single Map (CLI)
All single maps require at the very least a:
* **-s:** To clarify that you are compiling a single map.
* **--name:** To allow for building directories.
* **--map:** To give a path to a `.bsp` file.

There are also the optional:
* **--comment:** To allow for flavor text.
* **--image:** To give your map a thumbnail.
* **--lock:** To flag that this map needs to be [unlocked by playing another map](https://developer.valvesoftware.com/wiki/Point_bonusmaps_accessor).
* **--output:** To change the output directory. Default is `./exports`
* **--json:** To instead output or add onto a json file with the data of this map. Used for creating map packs.

#### Example Of Compiling A Map
Let's say we have a map which is located in a folder on our desktop. Along with that, we took a screenshot and cropped it to what we want. What we would do is **open a terminal in the this program's directory** and:

```bash
python ./CustomMapCompiler.py -s -n "The Coolest Map Ever" -c "This map was made by: BP" -m "/home/Desktop/my-map/my-example-map.bsp" -i "/home/Desktop/my-map/my-screenshot.png"
```

The finished product will now be found in `./exports`.

##### What we did with that command
* Told the tool we are compiling a single map **-s**
* Gave it the name *The Coolest Map Ever* **-n**
* Gave it the comment *This map was made by: BP* **-c**
* Gave the map's path at */home/Desktop/my-map/my-example-map.bsp* **-m**
* Gave the thumbnail's path at */home/Desktop/my-map/my-screenshot.png* **-i**

### Compiling A Map Pack (CLI)
All map packs require at the very least a:
* **-p:** To clarify that you are compiling a map pack.
* **--name:** To allow for building directories.
* **--json:** To give a list of maps which are apart of the pack.

There are also the optional:
* **--comment:** To allow for flavor text.
* **--image:** To give your map pack a thumbnail.
* **--lock:** To flag that this map pack needs to be [unlocked by playing another map](https://developer.valvesoftware.com/wiki/Point_bonusmaps_accessor).
* **--output:** To change the output directory. Default is `./exports`

#### Example Of Compiling A Map Pack
#### We need to create a list of maps first
Before we begin with making the pack, we must first make a `.json` file with all of the maps which will be inside of the pack. Let's use our map in the previous example.

```bash
python ./CustomMapCompiler.py -s -n "The Coolest Map Ever" -c "This map was made by: BP" -m "/home/Desktop/my-map/my-example-map.bsp" -i "/home/Desktop/my-map/my-screenshot.png" -j "./my-map-pack.json"
```

##### What's different
* Gave it the json path *./my-map-pack.json* **-j**

This prevents the tool from compiling a single map. Do this with all of your other maps, giving it the **-j** argument to add onto it.

#### Now for the pack itself
It's self explanatory, just like compiling a map. But, we swap out the **-s** flag for a **-p** and never use the **-m** argument. We replace it out with the **-j** argument as the input.

```bash
python ./CustomMapCompiler.py -p -n "The Coolest Map Pack Ever" -c "This pack was made by: BP" -j "./my-map-pack.json" -i "/home/Desktop/my-map-pack/my-screenshot.png"
```

That's all! You are now prepared to make your own maps and map packs for this browser!

## CLI Arguments
This is a more verbose explanation of all of the available arguments.

### -g --gui (GUI Editor)
> ***WARNING:*** This tool isn't complete. Single pack works fine (hangs when you attempt to overwrite an existing folder. Check console for extra instrucitons.), but map pack hasn't been implemented.

* A more user friendly way of compiling custom maps and packs for the browser.
* It also allows for a much easier means of creating thumbnails.

```bash
-g
```

### -s (Single Map)
* Tells the tool that you will only be compiling a single map.

```bash
-s
```

### -p (Map Pack)
* Tells the tool that you will be compiling a map pack.

```bash
-p
```

### -n --name (Addon Name)
* Sets the name of the map. Along with this, it will also be used when naming your addon.

```bash
-n "The Great Mod Which Is Awesome!"
```

### -c --comment (Comment)
* Sets the text for the comment. Shown right below the path in the map browser.

```bash
-c "Made by: BP"
```

### -m --map (Map Path)
* The file path to your map (`.bsp`) file.

```bash
-m "~/Desktop/Half-Life 2/maps/my-map.bsp"
```

### -j --json (Export To Json)
* **When used on a map** it will open that `.json` file and append its data into it instead of creating a compiled folder.
* **When used on a pack** it's the contents of that map's pack. All maps within the `.json` will be compiled into a single folder.

```bash
-j "./the-cool-map-pack.json"
```

### -i --image (Image Path)
* The file path to an image file that will be used for the thumbnail.
> **NOTE:** The tool will happily scale down your image to the required size, but **the thumbnail's aspect ratio is 9:5**. If you want your image to look exactly like what you want, **be sure to crop it beforehand.**

```bash
-i "~/Desktop/Screenshots/my-map-screenshot.png"
```

### -l --lock (Lock Map/Pack)
* Tells the game that this should be locked until a [point_bonusmaps_accessor](https://developer.valvesoftware.com/wiki/Point_bonusmaps_accessor) is fired that unlocks it.

```bash
-l
```

### -o --output (Folder Output)
* Change the directory in which we output the compiled bonus map folder. The default directory is `./exports`

```bash
-o "~/Desktop"
```
