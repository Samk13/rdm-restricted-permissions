#!/bin/bash
# DO NOT USE IT IN PROD!
# this is for development only

./scripts/acr_pull_latest_tag.sh
docker-compose -f docker-compose.full.yml up -d
docker image prune -f
# nohup command to prevent the system from terminating a running command when you log out or sleep. 
# Also, appending & to run it in the background.
# nohup ./scripts/ignite_app.sh &
# systemd-inhibit --what=idle
./scripts/ignite_app.sh
# docker-compose -f docker-compose.full.yml restart

echo "Restarting kth-rdm-prod-web-ui-1 ..."
docker restart kth-rdm-prod-web-ui-1


echo "Service Setup Done, go to:"
echo "https://127.0.0.1/"