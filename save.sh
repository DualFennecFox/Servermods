#!/bin/bash

ACCESS_TOKEN="sl.B6r5viU7d9Ko5UiLBwzM1af1U3YClxRalagyD7Ztlr0sJh9rbUuavQ2_laVvA3jBUWRsQgWpoUAa4ZicWwYs9ZG___7hEpUwBrUtQIkEHDYvBf-jX5qOt8mJQx1zNOo0oHiI3H7bJARJUE0bO1x4"
FILE_PATH="/workspaces/Servermods/Minecraft-server/world-r.zip"
DROPBOX_PATH="/world-r.zip"

cd "/workspaces/Servermods/Minecraft-server"
zip -r $FILE_PATH /workspaces/Servermods/Minecraft-server/world

curl -X POST https://content.dropboxapi.com/2/files/upload \
  --header "Authorization: Bearer $ACCESS_TOKEN" \
  --header "Dropbox-API-Arg: {\"path\": \"$DROPBOX_PATH\", \"mode\": \"overwrite\", \"strict_conflict\": false}" \
  --header "Content-Type: application/octet-stream" \
  --data-binary @$FILE_PATH

printf "\n\nMundo guardado con exito en dropbox\n"
