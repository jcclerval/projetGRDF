#!/bin/bash

sleep 3
echo "--- Lancement d'un scan ---"
#
i="0"
echo "--- Lancement de Wvdial ---"
#wvdial &
sleep 2
echo "--- Test de connection ---"
while [ $i -lt 10 ]
	do
	echo "Tentative $i"
	# Test de la connection internet
	wget -q --tries=10 --timeout=20 --spider http://google.com
	if [[ $? -eq 0 ]]; then
			echo "Online"
			echo "proceed with programm"
			i="10"
	else
			echo "Offline"
			sleep 2
	fi
	i=$[$i+1]
done
#
echo "Fin du code"
sleep 2
