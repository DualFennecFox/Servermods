import sys

version = sys.argv[1]
forge_version = "47.3.5" # If you are going to use forge

#Chose server type. Currently available versions: fabric, paper, forge
server_type = sys.argv[2]
java_path = "/usr/lib/jvm/java-17-openjdk-amd64/bin/java"

import os 
# Update the package lists
os.system("sudo apt -y update && echo \"apt cache successfully updated\" || echo \"apt cache update failed, you might receive stale packages\"")
# Install OpenJDK 17
# !wget -qO - https://adoptopenjdk.jfrog.io/adoptopenjdk/api/gpg/key/public | sudo apt-key add -
# !sudo add-apt-repository --yes https://adoptopenjdk.jfrog.io/adoptopenjdk/deb/ &>/dev/null || echo \"Failed to add repo. Still can be ignored if openjdk17 gets installed.\"
os.system("sudo apt-get -y install openjdk-17-jre-headless && echo \"Yay! Openjdk17 has been successfully installed.\" || echo \"Failed to install OpenJdk17.\"")
#Perform java version check
java_ver = os.system("java -version 2>&1 | awk -F[\"\.] -v OFS=. \"NR==1{print $2}\"")

import requests
import json
import os


os.system("mkdir \"./Minecraft-server\"")
os.system("cd \"./Minecraft-server\"")
os.system("mkdir \"./Minecraft-server/mods\"")

if server_type == "paper":
  a = requests.get("https://papermc.io/api/v2/projects/paper/versions/" + version)
  b = requests.get("https://papermc.io/api/v2/projects/paper/versions/" + version + "/builds/" + str(a.json()["builds"][-1]))
  print("https://papermc.io/api/v2/projects/paper/versions/" + version + "/builds/" + str(a.json()["builds"][-1]) + "/downloads/" + b.json()["downloads"]["application"]["name"])

  url = "https://papermc.io/api/v2/projects/paper/versions/" + version + "/builds/" + str(a.json()["builds"][-1]) + "/downloads/" + b.json()["downloads"]["application"]["name"]

  jar_name = "server.jar"
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

print('Servidor creado.')