import urllib.request
import json

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

######## GENERAL FUNCTION ###########

def getJSONData(url):
    json_url = urllib.request.urlopen(url)
    data = json.loads(json_url.read())
    return data