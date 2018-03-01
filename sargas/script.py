# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Created on Sat Dec  3 12:35:20 2016

@author: Jean-Christophe Clerval
"""

### IMPORTS NECESSAIRES -------------------------------------------------------
from subprocess import Popen, PIPE
from multiprocessing import Process, active_children
import os
import paho.mqtt.client as mosquitto
import sys
import time
## Définition des variables ---------------------------------------------------
serverName = "192.168.1.23"
#serverName = "jcsgrdf.ddns.net"
serverPort = 1883
camionId = 30
tpsIteration = 10000
## ----------------------------------------------------------------------------

### FONCTIONS -----------------------------------------------------------------
"""
Liste des fonctions:
- scan(l):
    Lance l fois la fonction read() et retourne une liste après en avoir
    supprimé les doublons. Publie ensuite cette liste à l'aide de la fonction
    publish(camionId, data).
 
- read():
    Lance un scan (programme C) et récupère la valeure d'une seule étiquette et
    la renvoie.
   
- publish(camionId, data):
    Publie un paquet MQTT à l'adresse spécifié en variable d'entrée sur 
    etudeje/camionId avec comme valeur l'identifiant de l'étiquette.
    
Stratégie :
1. On lance le scan pendant x secondes
2. Pour chaque étiquette
    2.1. on envoie /grdf/camionId/outil/etiquette
"""

def scan(l):
	print 'Début du scan'
	print "Temps du scan en milisecondes ",l
	temp = []

	proc = Popen(["./src/api/read", "tmr://localhost", "--ant", "1","--time",str(l)],stdout=PIPE, bufsize=1, universal_newlines=True )
	temp = proc.stdout.read().split('\n')
	temp.pop()

	print temp
	print 'Scan terminé, envoie des informations sur le brooker MQTT'

	#temp = list(set(temp))                                                     # On transforme la liste pour supprimer les doublons
	if temp != []:
		publish(camionId, ["delete"])                                          # On supprime le contenu
		publish(camionId, temp)                                                # On publie la liste des etiquettes trouvées
	return 0
  
""" 
def read():
#    try:
    proc = Popen(["./example"],stdout=PIPE)
    proc.wait()
    recep = proc.stdout.readline()
    if recep == "Segmentation fault\n":
        print "Segmentation fault"
        return read()
    elif recep != "NTR\n":
        print recep.split('\n')[0]
        return recep.split('\n')[0]
#    except:
#        return ''
"""        
  
def publish(camionId, data):
    # Connexion au broker mqtt
    mqttc = mosquitto.Client()
    mqttc.connect(serverName, serverPort)
    
    for element in data:
        print "Publié :", element
        mqttc.publish("etudeje/"+str(camionId), element)
        mqttc.loop(2)
    return 0
    
### INITIALISATION DU SCRIPT --------------------------------------------------
print "Initialisation du script"
time.sleep(1)
print 'Lancement du scan'

### LANCEMENT D'UN SCAN -------------------------------------------------------
#os.chdir("/home/pi/projetGRDF")
try:
    proces = Process(target=lambda : scan(tpsIteration))
    proces.start()
    proces.join()
except KeyboardInterrupt:
    print '\nInterrupted'
    try:
        for child in active_children():
            print child
            child.terminate()
        sys.exit(0)
    except SystemExit:
        os._exit(0)
print "terminé"
### FIN DU SCRIPT -------------------------------------------------------------
