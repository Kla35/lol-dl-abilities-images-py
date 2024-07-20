from audioop import mul
import os
import constant
import shutil
import urllib.request
import json
import constant
import unicodedata
import requests
from bs4 import BeautifulSoup

######### DOWNLOAD DATA FUNCTION ##########

def getActualVersion():
    versionJSON = getJSONData("https://ddragon.leagueoflegends.com/api/versions.json")
    constant.version = versionJSON[0]
    return versionJSON[0]

def getChampionsData():
    championsJSON = getJSONData("https://ddragon.leagueoflegends.com/cdn/"+constant.version+"/data/en_US/champion.json")
    return championsJSON["data"]
    
def getChampionsSpellsSpecific():
    otherAbilitesJSON = getJSONData("https://raw.githubusercontent.com/Kla35/lol-dl-abilities-images-py/master/othersabilities.json")
    return otherAbilitesJSON
    
def getChampionDataById(id):
    req = urllib.request.Request("https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champions/"+id+".json", headers={'User-Agent': 'Mozilla/5.0'})
    data = json.loads(urllib.request.urlopen(req).read())
    return data

def getSummonersData():
    summoners = getJSONData("https://ddragon.leagueoflegends.com/cdn/"+constant.version+"/data/fr_FR/summoner.json")
    return summoners["data"]

def getItemsData():
    items = getJSONData("https://ddragon.leagueoflegends.com/cdn/"+constant.version+"/data/fr_FR/item.json")
    return items["data"]
    
######### TREAT FUNCTION ############

def countOthersAbilities(data):
    nbAbilities = 0
    for champ in data:
        nbAbilities+= len(champ["spells"])
    return nbAbilities

def countNbImagesToDownload(champions, championsPerso, summoners, items, mainGUI):
    if mainGUI.cb_spells.get() == 1:
        nbSpells = countOthersAbilities(championsPerso)+len(champions)*5
    else:
        nbSpells = 0

    if mainGUI.cb_summoners.get() == 1:
        nbSummoners = len(summoners)
    else:
        nbSummoners = 0
    
    if mainGUI.cb_items.get() == 1:
        nbItems = len(items)
    else:
        nbItems = 0

    if mainGUI.cb_items.get() == 1:
        nbItems = len(items)
    else:
        nbItems = 0

    nbChampion = len(champions)
    multiplicator = mainGUI.cb_splash.get() + mainGUI.cb_icon.get() + mainGUI.cb_vertical.get()
    champImage = nbChampion * multiplicator

    return champImage + nbSpells + nbSummoners + nbItems
def trimChampionName(str):
    returnStr = str.replace("'","")
    returnStr = returnStr.replace(".","")
    returnStr = returnStr.replace("&","")
    returnStr = returnStr.replace(" ","")
    returnStr = returnStr.replace(" ","")
    return returnStr

def defineSpellKey(str):
    match str:
        case "P2":
            return "Passif_2"
        case "P3":
            return "Passif_3"
        case "Q2":
            return "A_2"
        case "Q3":
            return "A_3"
        case "Q4":
            return "A_4"
        case "W2":
            return "Z_2"
        case "W3":
            return "Z_3"
        case "E2":
            return "E_2"
        case "E3":
            return "E_3"
        case "R2":
            return "R_2"
        case "R3":
            return "R_3"
        case "R4":
            return "R_4"
        case "R5":
            return "R_5"
        case "Q":
            return "A"
        case "W":
            return "Z"
        case _:
            return str

######## DOWNLOAD IMAGES FUNCTION ########
def download_image(url, file_path, file_name):
    full_path = file_path + '/' + file_name
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        response = urllib.request.urlopen( req )
    except urllib.error.URLError as e:
        if hasattr( e, 'reason' ):
            print( 'Fail in reaching the server -> ', e.reason )
            print(url)
            return False
        elif hasattr( e, 'code' ):
            print( 'The server couldn\'t fulfill the request -> ', e.code )
            print(url)
            return False
    else:
        with open( full_path, 'wb' ) as fo:
            fo.write( response.read() )
            
            #print( 'Url saved as %s' % full_path )
        return True

def downloadSpellImage(spellPath, fileName):
    imageURL = ""
    if spellPath.startswith('/lol-game-data/assets/ASSETS/'):
        trim = spellPath.split('/lol-game-data/assets/ASSETS/')
        imageURL = 'https://raw.communitydragon.org/latest/game/assets/'+trim[1].lower()
    else:
        trim = spellPath.split('/lol-game-data/assets/v1/champion-ability-icons/')
        imageURL = 'https://raw.communitydragon.org/latest/game/data/characters/qiyana/hud/icons2d/'+trim[1].lower()
    
    download_image(imageURL, constant.folders['cb_spells'], fileName)

def downloadIconImage(champName,version):
    imageURL = 'http://ddragon.leagueoflegends.com/cdn/'+version+'/img/champion/'+champName+'.png';
    download_image(imageURL, constant.folders['cb_icon'], champName+'.jpg')

def downloadSplashImage(champName):
    imageURL = 'https://ddragon.leagueoflegends.com/cdn/img/champion/splash/'+champName+'_0.jpg';
    download_image(imageURL, constant.folders['cb_splash'], champName+'.jpg')

def downloadVerticalImage(champName):
    imageURL = 'https://ddragon.leagueoflegends.com/cdn/img/champion/loading/'+champName+'_0.jpg';
    download_image(imageURL, constant.folders['cb_vertical'], champName+'.jpg')

def downloadSummonerImage(summonerPath, summonerName):
    imageURL = 'https://ddragon.leagueoflegends.com/cdn/'+constant.version+'/img/spell/'+summonerPath
    download_image(imageURL, constant.folders['cb_summoners'], summonerName+'.jpg')

def downloadItemImage(itemPath, itemName):
    imageURL = 'https://ddragon.leagueoflegends.com/cdn/'+constant.version+'/img/item/'+itemPath
    download_image(imageURL, constant.folders['cb_items'], itemName+'.png')

######## GENERAL FUNCTION ###########

def getJSONData(url):
    json_url = urllib.request.urlopen(url)
    data = json.loads(json_url.read())
    return data


    
def recreate_folders(mainGUI):
    foldersCb = ['cb_icon','cb_spells','cb_splash','cb_vertical','cb_summoners','cb_items']
    base_folder = mainGUI.folder_path.get()
    constant.folders = {'cb_icon': os.path.join(base_folder, 'championIcon'), 'cb_spells': os.path.join(base_folder, 'championSpell'), 'cb_splash': os.path.join(base_folder, 'championSplash'), 'cb_vertical': os.path.join(base_folder, 'championVertical'), 'cb_summoners': os.path.join(base_folder, 'summoners'), 'cb_items': os.path.join(base_folder, 'items')}
    for folderCb in foldersCb:
        if mainGUI.getCheckbox(folderCb).get() == 1:
            folder = constant.folders[folderCb]
            shutil.rmtree(folder, ignore_errors=True)
            os.makedirs(folder)

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])