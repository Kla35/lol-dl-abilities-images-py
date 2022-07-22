from function import *
from GUI import *
import constant
import threading
from time import sleep

# Remove all old files from folders
recreate_folders()

# Get actual version of CDN
version = getActualVersion()
champions = getChampionsData(version)
championsPerso = getChampionsSpellsSpecific()
othersAbilitiesCount = countOthersAbilities(championsPerso)

allImagesToDownload = othersAbilitiesCount + len(champions) * 5 + len(champions) * 3

mainGUI = GUI(allImagesToDownload)


def newThread():
    new_thread = threading.Thread(target=mainScript, daemon=True)
    # Start the thread
    new_thread.start()
    # continue code or run this:
    while new_thread.is_alive(): # While the new thread is still running
        mainGUI.window.update()
        sleep(0.4)

def mainScript():
    for keyChampion in champions:
        print(constant.actualImg)

        actualChamp = champions[keyChampion]
        championName = trimChampionName(actualChamp["name"])
        championData = getChampionDataById(actualChamp["key"])
        
        downloadIconImage(keyChampion,version)
        downloadSplashImage(keyChampion)
        downloadVerticalImage(keyChampion)
        
        for spell in championData["spells"]:
            spellKey = defineSpellKey(spell["spellKey"].upper())
            newName = championName+'_'+spellKey+".png";
            downloadSpellImage(spell["abilityIconPath"], newName)
        
        newName = championName+"_Passif.png";
        downloadSpellImage(championData["passive"]["abilityIconPath"], newName)
        constant.actualImg+= 8
        mainGUI.updateTask("Download files for "+championName, constant.actualImg)

    for champion in championsPerso:
        championName = trimChampionName(champion["name"])
        for spell in champion["spells"]:
            spellKey = defineSpellKey(spell["spellKey"].upper())
            newName = championName+'_'+spellKey+".png";
            downloadSpellImage(spell["abilityIconPath"], newName) 
            constant.actualImg+= 1
            mainGUI.updateTask("Download additional files for "+championName, constant.actualImg)
    
    mainGUI.window.destroy()
    exit()

def on_closing():
    mainGUI.window.destroy()
    exit()

mainGUI.window.protocol("WM_DELETE_WINDOW", on_closing)
mainGUI.window.after(1000, newThread)
mainGUI.window.mainloop()