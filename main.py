import urllib.request
import json
import os
import constant
import shutil
from function import *

print(constant.ICON_FOLDER)
folders = [constant.ICON_FOLDER, constant.SPELL_FOLDER,constant.SPLASH_FOLDER,constant.VERTICAL_FOLDER]
    
def recreate_folders():
    for folder in folders:
        shutil.rmtree(folder, ignore_errors=True)
        os.makedirs(folder)


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

# Remove all old files from folders
recreate_folders()

# Get actual version of CDN
version = getActualVersion()
champions = getChampionsData(version)
championsPerso = getChampionsSpellsSpecific()
othersAbilitiesCount = countOthersAbilities(championsPerso)

for keyChampion in champions:

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

for champion in championsPerso:
    championName = trimChampionName(champion["name"])
    for spell in champion["spells"]:
        spellKey = defineSpellKey(spell["spellKey"].upper())
        newName = championName+'_'+spellKey+".png";
        downloadSpellImage(spell["abilityIconPath"], newName)   
