import os
import constant
import shutil
import urllib.request
import json
import constant

######### DOWNLOAD DATA FUNCTION ##########

def getActualVersion():
    versionJSON = getJSONData("https://ddragon.leagueoflegends.com/api/versions.json")
    return versionJSON[0]

def getChampionsData(version):
    championsJSON = getJSONData("https://ddragon.leagueoflegends.com/cdn/"+version+"/data/en_US/champion.json")
    return championsJSON["data"]
    
def getChampionsSpellsSpecific():
    otherAbilitesJSON = getJSONData("https://raw.githubusercontent.com/Kla35/lol-dl-abilities-images/main/othersabilities.json")
    return otherAbilitesJSON
    
def getChampionDataById(id):
    req = urllib.request.Request("https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champions/"+id+".json", headers={'User-Agent': 'Mozilla/5.0'})
    data = json.loads(urllib.request.urlopen(req).read())
    return data

######### TREAT FUNCTION ############

def countOthersAbilities(data):
    nbAbilities = 0
    for champ in data:
        nbAbilities+= len(champ["spells"])
    return nbAbilities


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
    
    download_image(imageURL, constant.SPELL_FOLDER, fileName)

def downloadIconImage(champName,version):
    imageURL = 'http://ddragon.leagueoflegends.com/cdn/'+version+'/img/champion/'+champName+'.png';
    download_image(imageURL, constant.ICON_FOLDER, champName+'.jpg')

def downloadSplashImage(champName):
    imageURL = 'https://ddragon.leagueoflegends.com/cdn/img/champion/splash/'+champName+'_0.jpg';
    download_image(imageURL, constant.SPLASH_FOLDER, champName+'.jpg')

def downloadVerticalImage(champName):
    imageURL = 'https://ddragon.leagueoflegends.com/cdn/img/champion/loading/'+champName+'_0.jpg';
    download_image(imageURL, constant.VERTICAL_FOLDER, champName+'.jpg')

######## GENERAL FUNCTION ###########

def getJSONData(url):
    json_url = urllib.request.urlopen(url)
    data = json.loads(json_url.read())
    return data


    
def recreate_folders():
    folders = [constant.ICON_FOLDER, constant.SPELL_FOLDER,constant.SPLASH_FOLDER,constant.VERTICAL_FOLDER]
    for folder in folders:
        shutil.rmtree(folder, ignore_errors=True)
        os.makedirs(folder)