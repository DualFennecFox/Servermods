import os
import re
import json

version = '1.20.1'
forge_version = "47.2.21"  # If you are going to use forge
java_path = "/usr/lib/jvm/java-17-openjdk-amd64/bin/java"
#Chose server type. Currently available versions: fabric, paper, forge
server_type = 'forge'


# Update the package lists
os.system("sudo apt update &>/dev/null && echo \"apt cache successfully updated\" || echo \"apt cache update failed, you might receive stale packages\"")
# Install OpenJDK 17
# !wget -qO - https://adoptopenjdk.jfrog.io/adoptopenjdk/api/gpg/key/public | sudo apt-key add -
# !sudo add-apt-repository --yes https://adoptopenjdk.jfrog.io/adoptopenjdk/deb/ &>/dev/null || echo \"Failed to add repo. Still can be ignored if openjdk17 gets installed.\"
os.system("sudo apt-get install openjdk-17-jre-headless &>/dev/null && echo \"Yay! Openjdk17 has been successfully installed.\" || echo \"Failed to install OpenJdk17.\"")
#Perform java version check
java_ver = os.system("java -version 2>&1 | awk -F[\"\.] -v OFS=. \"NR==1{print $2}\"")

# Change directory to the Minecraft server folder on Google Drive
os.system("cd \"/workspaces/Servermods/Minecraft-server\"")
os.system("ls") #list the directory contents (to verify that working directory was changed)

# Import config file.
if os.path.isfile("gitconfig.json"):
  gitconfig = json.load(open("gitconfig.json"))
else:
  gitconfig = {"server_type": "generic"} # using default, if config doesn't exists.
  json.dump(gitconfig, open("gitconfig.json",'w'))

# Server jar names.
jar_list = {'paper': 'server.jar', 'fabric': 'fabric-server-launch.jar', 'generic': 'server.jar', 'forge': 'server.jar'}
jar_name = jar_list[gitconfig["server_type"]]

# Java arguments.
if gitconfig["server_type"] == "paper":
  server_flags = "-XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true"
else:
  server_flags = "-Djava.awt.headless=true" # aiker's flags might negatively impact performance on non-paper servers.
memory_allocation = "-Xmx8162M -Xms512M"

# Chose the tunnle service you want to use
# Available options: ngrok, argo, playit
os.system("touch eula.txt")
os.system("echo \"eula=true\" >> eula.txt")

#ferium
os.system("wget \"https://github.com/gorilla-devs/ferium/releases/download/v4.5.2/ferium-linux-nogui.zip\"")
os.system("unzip -n \"ferium-linux-nogui.zip\"")
os.system("rm \"ferium-linux-nogui.zip\"")

os.system("./ferium profile delete \"Server\"")
os.system(f"./ferium profile create -n \"Server\" -v \"{version}\" -m \"{server_type}\" -o \"/workspaces/Servermods/Minecraft-server/mods\"")

os.system("./ferium add 472661") #Fabric API
os.system("./ferium add 306612") #CraftControlRCON
os.system("./ferium add 630406") #CosmeticsArmours
os.system("./ferium add 405076") #Epic Fight
os.system("./ferium add 258587") #ItemPhysic
os.system("./ferium add 890166") #Cosmetic Nametags
os.system("./ferium add 348521") #Cloth Config API
os.system("./ferium add 306770") #Patchouli 
os.system("./ferium add 659110") #Regions Unexplored
os.system("./ferium add 618298") #Sophisticated Core
os.system("./ferium add 243707") #Corail Tombstone
os.system("./ferium add 500273") #Visual Workbench
os.system("./ferium add 331936") #Citadel
os.system("./ferium add 419699") #Architectury API
os.system("./ferium add 531761") #Balm
os.system("./ferium add 237749") #CoroUtil
os.system("./ferium add 257814") #CreativeCore
os.system("./ferium add 349559") #FallingTree
os.system("./ferium add 238222") #Just Enough Items
os.system("./ferium add 658587") #playerAnimation Lib
os.system("./ferium add 914094") #SetHome TCT
os.system("./ferium add 535489") #Sound Physics Remastered
os.system("./ferium add 235577") #TrashSlot
os.system("./ferium add 945479") #What Are They Up To (Watut)
os.system("./ferium add 493246") #Flan
os.system("./ferium add 404465") #FTB Library
os.system("./ferium add 237307") #Cosmetic Armor Reworked
os.system("./ferium add 240633") #Inventory Sorter
os.system("./ferium add 32274") #JourneyMap
os.system("./ferium add 250898") #Ore Excavation
os.system("./ferium add 495476") #PuzzlesLib 
os.system("./ferium add 422301") #Sophisticated Backpacks
os.system("./ferium add 1001299") #The Knocker
os.system("./ferium add 227639") #The Twilight Forest
os.system("./ferium add 563928")  #TerraBlender
os.system("./ferium add 404468") #FTB Teams Forge
os.system("./ferium add 939167")  #TPA
os.system("./ferium add 221939") #More Player Models
os.system("./ferium add 225643") #Botania
os.system("./ferium add 309927") #Curios API

os.system("./ferium upgrade")

tunnel_service = "playit"
print("Procedding to use", tunnel_service)

if tunnel_service == "playit":
  os.system(f'''curl -SsL https://playit-cloud.github.io/ppa/key.gpg | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/playit.gpg >/dev/null
            echo "deb [signed-by=/etc/apt/trusted.gpg.d/playit.gpg] https://playit-cloud.github.io/ppa/data ./" | sudo tee /etc/apt/sources.list.d/playit-cloud.list
            sudo apt update
            sudo apt install
            ''')
  
  os.system("./run.sh")
  os.system("../save.sh")
