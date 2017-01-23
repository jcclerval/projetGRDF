#!/bin/bash

echo '*****************************************'
echo '*                                       *'
echo '*      Installation de la Raspberry     *'
echo '*                                       *'
echo '*****************************************'

#-----------------------------------------------
echo '	- Copy des fichiers'

mkdir $HOME/fichiers
cp rasp/skyetek $HOME/projetGRDF/skyetek
cp rasp/script.py $HOME/projetGRDF/script.py

#-----------------------------------------------
echo '	- Installation du script de démarrage'

sed -i -e "s/exit 0/cd \/home\/pi\/projetGRDF\/\npython \/home\/pi\/projetGRDF\/script.pi\nexit 0/g" /etc/rc.local

#-----------------------------------------------
echo '	- Installation des modules necessaires'
sudo apt-get update && sudo apt-get upgrade && sudo apt-get install -y mosquitto python-pip python-mysqldb

pip install paho-mqtt

echo '********** Installation terminée **********'

exit 0
