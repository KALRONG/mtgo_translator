# mtgo-translator
# Introduction
This is a first "really ugly" version of an script that will use the translations on scryfall to translate the cards in mtgo to the language that we want.

# Requirements
- Python 3
- Libraries:
--lxml
--progressbar
--glob
--json

# Preparation
For the script to work several variables need to be modified:
- language: This will be the language code from scryfall (https://scryfall.com/docs/api/languages)
- path: Working path where the script will use for the input/output files
- json_file: The name of the all cards json file from scryfall (https://scryfall.com/docs/api/bulk-data)

You also need to copy, to the same folder set on the path variable, the CardDataSource folder of your mtgo installation, it can be found in C:\Users\<user>\AppData\Local\Apps\2.0\Data\ there are several subfolders with ID's that Im not sure what they mean, follow them and when facing a folder with several ones choose the one with the latest date.

# How it "works"
MTGO cards information is stored in several XML files that are correlated using unique ID's for each part of the card, the ID used to identify the card is the same as the mtgo_id but with the prefix DOC, this helps us find the specific card in the json file from scryfall that we then use to find the specific data in the selected language and generate the new XMLs with the text translated.

# why scryfall and not mtgjson?
mtgjson provides an sqlite database but it doesnt have the neede end of file on the texts so the game goes a little bit crazy, scryfall in the other hand, provides the proper ends of line.

# Run time
As I said this script is ugly and probably not the best way to do this, but it works, it just takes several hours and around 5gb of ram in the mean time.

# TODO
- Maybe generate an sqlite from the json to makes things easier and faster.
- Multithreading?
- Multi face cards and PW.

# Disclaimer
This script has nothing to do with WoTC and is provided as is with little test, so always use a backup, and use it as your own risk.
