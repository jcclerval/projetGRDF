#!/bin/bash

echo '*****************************************'
echo '*                                       *'
echo '*      Installation de la Raspberry     *'
echo '*                                       *'
echo '*****************************************'

#-----------------------------------------------
echo '	- Installation du script de démarrage'

sudo sed -i -e "s/exit 0/cd \/home\/pi\/projetGRDF\/\npython \/home\/pi\/projetGRDF\/script.pi\nexit 0/g" /etc/rc.local

#-----------------------------------------------
echo '	- Installation des modules necessaires'
sudo apt-get update && sudo apt-get upgrade -y && sudo apt-get install -y mosquitto python-pip python-mysqldb

pip install paho-mqtt

echo '********** Installation terminée **********'

rm README.md
rm installation.sh
exit 0
