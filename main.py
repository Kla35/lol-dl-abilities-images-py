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

pool_sema = threading.Semaphore(value=5)

def newThread():
    new_thread = threading.Thread(target=mainScript, daemon=True)
    # Start the thread
    new_thread.start()
    # continue code or run this:
    while new_thread.is_alive(): # While the new thread is still running
        mainGUI.window.update()
        sleep(0.4)

def threadDownloadChamp(kC):
    pool_sema.acquire()
    actualChamp = champions[kC]
    championName = trimChampionName(actualChamp["name"])
    championData = getChampionDataById(actualChamp["key"])
    
    downloadIconImage(kC,version)
    downloadSplashImage(kC)
    downloadVerticalImage(kC)
    
    for spell in championData["spells"]:
        spellKey = defineSpellKey(spell["spellKey"].upper())
        newName = championName+'_'+spellKey+".png";
        downloadSpellImage(spell["abilityIconPath"], newName)
    
    newName = championName+"_Passif.png";
    downloadSpellImage(championData["passive"]["abilityIconPath"], newName)
    constant.actualImg+= 8
    mainGUI.updateTask("Download files for "+championName, constant.actualImg)
    pool_sema.release()
    
def threadDownloadSpecificChamp(cham):
    pool_sema.acquire()
    championName = trimChampionName(cham["name"])
    for spell in cham["spells"]:
        spellKey = defineSpellKey(spell["spellKey"].upper())
        newName = championName+'_'+spellKey+".png";
        downloadSpellImage(spell["abilityIconPath"], newName) 
        constant.actualImg+= 1
        mainGUI.updateTask("Download additional files for "+championName, constant.actualImg)
    pool_sema.release()

def mainScript():
    threads = []
   
    for keyChampion in champions:
        new_thread = threading.Thread(target=threadDownloadChamp, args=(keyChampion,))
        # Start the thread
        new_thread.start()
        threads.append(new_thread)

    for champion in championsPerso:
        new_thread = threading.Thread(target=threadDownloadSpecificChamp, args=(champion,))
        # Start the thread
        new_thread.start()
        threads.append(new_thread)
    
    for x in threads:
        x.join()
    mainGUI.window.destroy()
    exit()

def on_closing():
    mainGUI.window.destroy()
    exit()

mainGUI.window.protocol("WM_DELETE_WINDOW", on_closing)
mainGUI.window.after(1000, newThread)
mainGUI.window.mainloop()