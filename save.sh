#!/bin/bash

ACCESS_TOKEN=""
FILE_PATH="/workspaces/Servermods/Minecraft-server/world-paper.zip"
DROPBOX_PATH="/world-paper.zip"

cd "/workspaces/Servermods/Minecraft-server"
zip -r $FILE_PATH /workspaces/Servermods/Minecraft-server/world /workspaces/Servermods/Minecraft-server/world_nether /workspaces/Servermods/Minecraft-server/world_the_end

curl -X POST https://content.dropboxapi.com/2/files/upload \
  --header "Authorization: Bearer $ACCESS_TOKEN" \
  --header "Dropbox-API-Arg: {\"path\": \"$DROPBOX_PATH\", \"mode\": \"overwrite\", \"strict_conflict\": false}" \
  --header "Content-Type: application/octet-stream" \
  --data-binary @$FILE_PATH

printf "\n\nMundo guardado con exito en dropbox\n"
