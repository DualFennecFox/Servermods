import os
import re
import json
from os.path import exists


version = input("Elija la version de Minecraft: ")
forge_version = "47.3.5"  # If you are going to use forge
java_path = "/usr/lib/jvm/java-17-openjdk-amd64/bin/java"
#Chose server type. Currently available versions: fabric, paper, forge
server_type = input("Elija el tipo de servidor (fabric, paper, forge): ")

if not exists("/workspaces/Servermods/Minecraft-server/server.py"):
  os.system(f"python createsv.py {version} {server_type}")


# Update the package lists
os.system("sudo apt -y update && echo \"apt cache successfully updated\" || echo \"apt cache update failed, you might receive stale packages\"")
# Install OpenJDK 17
# !wget -qO - https://adoptopenjdk.jfrog.io/adoptopenjdk/api/gpg/key/public | sudo apt-key add -
# !sudo add-apt-repository --yes https://adoptopenjdk.jfrog.io/adoptopenjdk/deb/ &>/dev/null || echo \"Failed to add repo. Still can be ignored if openjdk17 gets installed.\"
os.system("sudo apt-get -y install openjdk-17-jre-headless && echo \"Yay! Openjdk17 has been successfully installed.\" || echo \"Failed to install OpenJdk17.\"")
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

tunnel_service = "playit"
print("Procedding to use", tunnel_service)

if tunnel_service == "playit":
  os.system(f'''curl -SsL https://playit-cloud.github.io/ppa/key.gpg | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/playit.gpg >/dev/null
            echo "deb [signed-by=/etc/apt/trusted.gpg.d/playit.gpg] https://playit-cloud.github.io/ppa/data ./" | sudo tee /etc/apt/sources.list.d/playit-cloud.list
            sudo apt -y update
            sudo apt -y install playit 
            ''')
  
  os.system(f'''
      cd Minecraft-server
      java {memory_allocation} {server_flags} -jar {jar_name} nogui
      ''')

from subprocess import Popen, CREATE_NEW_CONSOLE

Popen("playit", creationflags=CREATE_NEW_CONSOLE)

os.system("/workspaces/Servermods/save.sh")
