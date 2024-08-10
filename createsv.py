version = '1.20.1'
forge_version = "47.2.21"  # If you are going to use forge

#Chose server type. Currently available versions: fabric, paper, forge
server_type = 'forge'
java_path = "/usr/lib/jvm/java-17-openjdk-amd64/bin/java"

import requests
import json
import os


os.system("mkdir \"./Minecraft-server\"")
os.system("cd \"./Minecraft-server\"")
os.system("mkdir \"./Minecraft-server/mods\"")

os.system("wget \"https://github.com/gorilla-devs/ferium/releases/download/v4.5.2/ferium-linux-nogui.zip\"")
os.system("unzip -n \"ferium-linux-nogui.zip\"")
os.system("rm \"ferium-linux-nogui.zip\"")

os.system("./ferium profile delete \"Server\"")
os.system(f"./ferium profile create -n \"Server\" -v \"{version}\" -m \"{server_type}\" -o \"/workspaces/Servermods/Minecraft-server/mods\"")
os.system("./ferium add 472661") #Fabric API
os.system("./ferium add 306612") #CraftControlRCON Fabric
os.system("./ferium upgrade")

if server_type == "fabric":
  url = "https://maven.fabricmc.net/net/fabricmc/fabric-installer/1.0.0/fabric-installer-1.0.0.jar"
  jar_name = "fabric-installer.jar"
if server_type == "forge":
  url = f"https://maven.minecraftforge.net/net/minecraftforge/forge/{version}-{forge_version}/forge-{version}-{forge_version}-installer.jar"
  jar_name = "server.jar"

r = requests.get(url)

if r.status_code is 200:
  with open('/workspaces/Servermods/Minecraft-server/' + jar_name, 'wb') as f:
    f.write(r.content)
else:
  print('Error '+ str(r.status_code) + '!Most likely you entered a unsupported version. Try running the code again if you think that shouldn\'t have happened.')

# Running specific install path.

if server_type == "fabric":
  os.system(f'''
            /workspaces/Servermods/Minecraft-server/
            {java_path} -jar {jar_name} server -mcversion {version} -downloadMinecraft
            ''')
  
elif server_type == "forge":
  os.system(f'''
            cd /workspaces/Servermods/Minecraft-server/
            {java_path} -jar {jar_name} --installServer
            ''')

gitconfig = {"server_type": server_type}
json.dump(gitconfig, open("gitconfig.json",'w'))

print('Done!')