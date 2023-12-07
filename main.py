from concurrent.futures import thread

from pip import main
from function import *
from GUI import *
import constant
import threading
from time import sleep
from tkinter import *
from tkinter.ttk import *

# Get actual version of CDN
version = getActualVersion()
champions = getChampionsData()
championsPerso = getChampionsSpellsSpecific()
summoners = getSummonersData()
items = getItemsData()
itemsS14 = getItemsS14Data()

theTHREAD = NULL

mainGUI = GUI()

pool_sema = threading.Semaphore(value=5)

def threadDownloadChamp(kC):
    pool_sema.acquire()
    actualChamp = champions[kC]
    championName = trimChampionName(actualChamp["name"])
    championData = getChampionDataById(actualChamp["key"])
    if mainGUI.cb_icon.get() == 1:
        downloadIconImage(kC,version)
        constant.actualImg+= 1
    if mainGUI.cb_splash.get() == 1:
        downloadSplashImage(kC)
        constant.actualImg+= 1
    if mainGUI.cb_vertical.get() == 1:
        downloadVerticalImage(kC)
        constant.actualImg+= 1
    if mainGUI.cb_spells.get() == 1:
        for spell in championData["spells"]:
            spellKey = defineSpellKey(spell["spellKey"].upper())
            newName = championName+'_'+spellKey+".png"
            downloadSpellImage(spell["abilityIconPath"], newName)
            constant.actualImg+= 1
        newName = championName+"_Passif.png";
        downloadSpellImage(championData["passive"]["abilityIconPath"], newName)
        constant.actualImg+= 1
    mainGUI.updateTask("Download files for "+championName, constant.actualImg)
    pool_sema.release()
    
def threadDownloadSpecificChamp(cham):
    pool_sema.acquire()
    if mainGUI.cb_spells.get() == 1:
        championName = trimChampionName(cham["name"])
        for spell in cham["spells"]:
            spellKey = defineSpellKey(spell["spellKey"].upper())
            newName = championName+'_'+spellKey+".png";
            downloadSpellImage(spell["abilityIconPath"], newName) 
            constant.actualImg+= 1
            mainGUI.updateTask("Download additional files for "+championName, constant.actualImg)
    pool_sema.release()

def threadDownloadSummoner(kS):
    pool_sema.acquire()
    summoner = summoners[kS]
    downloadSummonerImage(summoner["image"]["full"],  remove_accents(trimChampionName(summoner["name"]))) 
    constant.actualImg+= 1
    mainGUI.updateTask("Download summoner "+summoner["name"], constant.actualImg)
    pool_sema.release()

def threadDownloadItem(kI):
    pool_sema.acquire()
    item = items[kI]
    if "requiredChampion" in item:
        imageName =  remove_accents(item["requiredChampion"]+kI)
    else:
        imageName =  remove_accents(trimChampionName(item["name"]))
    downloadItemImage(item["image"]["full"], imageName) 
    constant.actualImg+= 1
    mainGUI.updateTask("Download item "+item["name"], constant.actualImg)
    pool_sema.release()

def threadDownloadItemS14(item):
    pool_sema.acquire()
    downloadItemS14Image(item) 
    constant.actualImg+= 1
    mainGUI.updateTask("Download item "+item, constant.actualImg)
    pool_sema.release()

def mainScript():
    threads = []
    constant.actualImg = 0
    mainGUI.updateTask("Starting...", 0)

    tChampStatus = mainGUI.cb_icon.get() + mainGUI.cb_splash.get() + mainGUI.cb_vertical.get() + mainGUI.cb_spells.get() 
    if tChampStatus > 0 :
        for keyChampion in champions:
            new_thread = threading.Thread(target=threadDownloadChamp, args=(keyChampion,), daemon=True)
            # Start the thread
            new_thread.start()
            
            threads.append(new_thread)
    
    if mainGUI.cb_spells.get() > 0 :
        for champion in championsPerso:
            new_thread = threading.Thread(target=threadDownloadSpecificChamp, args=(champion,), daemon=True)
            # Start the thread
            new_thread.start()
            threads.append(new_thread)

    if mainGUI.cb_summoners.get() == 1:
        for summoner in summoners:
            new_thread = threading.Thread(target=threadDownloadSummoner, args=(summoner,), daemon=True)
            # Start the thread
            new_thread.start()
            threads.append(new_thread)

    if mainGUI.cb_items.get() == 1:
        for item in items:
            new_thread = threading.Thread(target=threadDownloadItem, args=(item,), daemon=True)
            # Start the thread
            new_thread.start()
            threads.append(new_thread)

    if mainGUI.cb_items_s14.get() == 1:
        for item in itemsS14:
            new_thread = threading.Thread(target=threadDownloadItemS14, args=(item,), daemon=True)
            # Start the thread
            new_thread.start()
            threads.append(new_thread)


    for x in threads:
        x.join()
    mainGUI.window.destroy()
    exit()

def on_closing():
    constant.exit_flag = True
    mainGUI.window.destroy()
    exit()


def newThread():
    mainGUI.b["state"] = "disabled"
    # Remove all old files from folders
    recreate_folders(mainGUI)
    # Count img for progress bar
    allImagesToDownload = countNbImagesToDownload(champions, championsPerso, summoners, items, itemsS14, mainGUI)
    mainGUI.setTotalImage(allImagesToDownload)
    # Set the thread
    theTHREAD = threading.Thread(target=mainScript, daemon=True)
    # Start the thread
    theTHREAD.start()
    # continue code or run this:
    while theTHREAD.is_alive(): # While the new thread is still running
        mainGUI.window.update()
        if constant.exit_flag: 
            break
        sleep(0.4)

mainGUI.b = Button(mainGUI.window, text ="Launch download", command = newThread)
mainGUI.b.grid(row=7, column=1,columnspan=2)

mainGUI.window.iconbitmap('./aled.ico')
mainGUI.window.protocol("WM_DELETE_WINDOW", on_closing)
mainGUI.window.title("LoL DL Images & Data")
mainGUI.window.mainloop()