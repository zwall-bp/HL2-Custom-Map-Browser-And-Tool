#!/bin/bash
#########################################################
# CUSTOM BACKGROUND INSTALLER!
# For use with BP's custom map browser to allow for a more personalized experience on the end user's side.
#########################################################

#########################################################
# LEVEL DEVELOPER!
# Use this variable below to allow the script to install the correct background maps.
#########################################################
CUSTOM_BACKGROUND_MAPS=([YOUR MAP NAME HERE]) #Put the name of your background maps here. Don't add in the file extention.

#########################################################
# Here's the magic.
# You can ignore everything down here.
#########################################################

HL2_DEFAULT_BG="\"chapters\"
{
	1	\"background01\"
	2	\"background01\"
	3	\"background02\"
	4	\"background02\"
	5	\"background03\"
	6	\"background03\"
	7	\"background04\"
	8	\"background04\"
	9	\"background05\"
	9a	\"background05\"
	10	\"background06\"
	11	\"background06\"
	12	\"background07\"
	13	\"background07\"
	14	\"background07\"
	15	\"background07\"
}"

EPISODIC_DEFAULT_BG="\"chapters\"
{
	1	\"ep1_background01\"
	2	\"ep1_background01\"
	3	\"ep1_background01a\"
	4	\"ep1_background02\"
	5	\"ep1_background02\"
	6	\"ep1_background02\"
	7	\"ep1_background02\"
	8	\"ep1_background02\"
}"

EP2_DEFAULT_BG="\"chapters\"
{
	1	\"ep2_background01\"
	2	\"ep2_background02\"
	3	\"ep2_background02\"
	4	\"ep2_background02a\"
	5	\"ep2_background02a\"
	6	\"ep2_background03\"
	7	\"ep2_background03\"
}"

ADDON_NAME="$(basename "$(pwd)")"
ADDON_PATH="$(pwd)"
SCRIPT_PATH="$(realpath "$0")"

#########################################################
#Functions
#########################################################

#Creates the custom background addon at the given directory, and defaults the chapterbackgrounds.txt
# $1 = directory of the mod. (.../Half-Life 2/hl2)
# $2 = Default backgrounds ($HL2_DEFAULT_BG)
create_addon(){
  #Check to see if the mod doesn't exist.
  if [ ! -d "$1" ]
  then
    echo "ERROR: The mod directory $1 doesn't exist!"
    exit 1;
  fi

  local CHAPTER_PATH="$1/custom/custom-backgrounds/scripts/chapterbackgrounds.txt"
  local BASE_PATH="$1/custom/custom-backgrounds/scripts/base-backgrounds.txt"
	local RESET_PATH="$1/custom/custom-backgrounds/ResetBackgrounds.sh"

  #Check to see if the addon already exists.
  if [ -e "$CHAPTER_PATH" ]
  then
    #The addon already exists
    return 0;
  fi

  #Create the directories to the script, and touch the script.
  mkdir -p "$(dirname "$CHAPTER_PATH")"
  touch "$CHAPTER_PATH"
  touch "$BASE_PATH"

  #Stream over chapterbackgrounds.txt and set up it's relation to base-backgrounds.txt.
  #Truncate
  > "$CHAPTER_PATH"
  echo -e "#base \"base-backgrounds.txt\"" > "$CHAPTER_PATH"

  #Stream over base-backgrounds.txt and set up all of the default backgrounds.
  > "$BASE_PATH"
  echo -n "$2" > "$BASE_PATH"

	#Make the reset script.
	> "$RESET_PATH"
	echo -e -n "echo \"#base \\\"base-backgrounds.txt\\\"\" > \"./scripts/chapterbackgrounds.txt\"" >> "$RESET_PATH"

  return 0;
}

#Creates a file inside of the addon which holds the addon's own chapterbackground data.
# $1 index to start with.
create_addon_background(){
	local CUSTOM_PATH="$ADDON_PATH/scripts/$ADDON_NAME.txt"
	local IDX="$1"

  #Create the directories to the script, and touch the script.
  mkdir -p "$(dirname "$CUSTOM_PATH")/"
  touch "$CUSTOM_PATH"

	#Stream over to the background file the contents of $CUSTOM_BACKGROUND_MAPS.
	#Truncate
	> "$CUSTOM_PATH"
	#Add in the head.
	echo -e "\"chapters\"\n{" >> "$CUSTOM_PATH"
	#Iterate over each background, adding into the file.
	for map in "${CUSTOM_BACKGROUND_MAPS[@]}"
	do
		echo -e "\t$IDX\t$map" >> "$CUSTOM_PATH"
		IDX=$(($IDX+1))
	done
	#End it with a curly bracket.
	echo -n "}" >> "$CUSTOM_PATH"
}

#Gets the next available index allowed based off the given .txt file path.
#	$1 = Path to a .txt file containing chapterbackground data.
#	Returns the next available index, or 0 if the file doesn't exist.
get_next_index(){
	#Check to see if the file exists.
	if [ ! -e "$1" ]
	then
		#The file doesn't exist!
		echo "ERROR: $1 doesn't exist!"
		return 0;
	fi

	#The file does exist, find the last instance of a number.
	local FILE_LINE_COUNT="$(wc -l < "$1")"
	local LINE_BEFORE=$(sed "$FILE_LINE_COUNT!d" "$1")

	local LAST_NUMBER="$(grep -E -o "[0-9]+" -m "1" <<< "$LINE_BEFORE" | head -1)"

	if (( $LAST_NUMBER >= 99 ))
	then
		echo "ERROR: You have hit the game's limit for the amount of background maps!."
		exit 1;
	fi

	return $(($LAST_NUMBER + 1))
}

#Get the addon name.

#Find out what version of the game we are installing to.
cd ../..  #Go back two in order to get to the mod directory.
MOD_TYPE="$(basename "$(pwd)")" #hl2/episodic/ep2
MOD_BG="" #Should become one of the three default BGs

#Switch/Case for what background file to use.
case $MOD_TYPE in
  hl2)
    MOD_BG="$HL2_DEFAULT_BG"
    ;;
  episodic)
    MOD_BG="$EPISODIC_DEFAULT_BG"
    ;;
  ep2)
    MOD_BG="$EP2_DEFAULT_BG"
    ;;
  *)
    echo "ERROR: Can't figure out the current mod directory!"
    exit 1;
    ;;
esac

#Check to see if the user has already intalled the addon.
create_addon "$(pwd)" "$MOD_BG"
#Go back into the mod's custom directory.
cd "./custom/"

#The addon should now exist. We can now attempt to update the background to allow for the custom map to display.
CHAPTER_PATH="$(pwd)/custom-backgrounds/scripts/chapterbackgrounds.txt"
CHAPTER_CUSTOM_COUNT="$(wc -l < "$CHAPTER_PATH")"
ADDON_IDX="1"
NEXT_CHAPTER_IDX="0"
#Create an iteration just in case the latest addon is no longer available.
while [[ "$(sed "$ADDON_IDX!d" "$CHAPTER_PATH")" != "" ]]
do
	#Open up the addon's chapterbackgrounds.txt and get the first line on it, the latest added.
	LATEST_ADDED_FILE_RAW="$(sed "$ADDON_IDX!d" "$CHAPTER_PATH")"

	#Filename we are trying to find.
	LATEST_ADDED_FILE="$(grep -o '".*"' <<< $LATEST_ADDED_FILE_RAW | sed 's/"//g')"
	#Addon we are trying to find.
	LATEST_ADDED_ADDON=${LATEST_ADDED_FILE%.*}

	#Check to see if the base background is the latest one.
	if [[ $LATEST_ADDED_ADDON == "base-backgrounds" ]]
	then
		#We will get the last index from /custom-backgrounds/scripts/base-backgrounds.txt
		get_next_index "$(pwd)/custom-backgrounds/scripts/base-backgrounds.txt"
		NEXT_CHAPTER_IDX="$?"
		#We now have the index, break!
		break;
	else
		#We will attempt to get the last index from /$LATEST_ADDED_ADDON/scripts/$LATEST_ADDED_FILE
		#Check to see if the file still exists.
		ADDON_BACKGROUND_PATH="$(pwd)/$LATEST_ADDED_ADDON/scripts/$LATEST_ADDED_FILE"
		if [ ! -e "$ADDON_BACKGROUND_PATH" ]
		then
			echo "$LATEST_ADDED_ADDON no longer exists!"
			continue;
		fi
		#The file exists!
		get_next_index "$ADDON_BACKGROUND_PATH"
		NEXT_CHAPTER_IDX="$?"
		#We now have the index, break!
		break;
	fi
	ADDON_IDX=$(( $ADDON_IDX + 1 ))
done

#Create the background file inside of this addon's /scripts
create_addon_background "$NEXT_CHAPTER_IDX"

#Now, append this to the start of the custom-background addon's chapterbackgrounds.txt
echo -e -n "#base \"$ADDON_NAME.txt\"\n$(cat "$CHAPTER_PATH")" > "$CHAPTER_PATH"

echo "$ADDON_NAME's background has been appened to your game's background rotation.
Be sure to do the command:

sv_unlockedchapter 99

to allow for all background maps to be shown"

#wait for keypress.
read -n 1 -s -r -p "Press any key to continue..."

echo ""
