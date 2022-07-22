from function import *

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
