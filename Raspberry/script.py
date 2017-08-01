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
#import paho.mqtt.client as mosquitto
import sys
import time
import io
## Définition des variables ---------------------------------------------------
serverName = "192.168.43.231"
serverPort = 1883
camionId = 30
nbIteration = 20
timeout = 10
## ----------------------------------------------------------------------------

### FONCTIONS UTILES ----------------------------------------------------------
"""
Liste des fonctions utiles :
- read():
    Lance un scan (programme C) et récupère la valeure d'une seule étiquette et
    la renvoie.
    
- scan(l):
    Lance l fois la fonction read() et retourne une liste après en avoir
    supprimé les doublons. Publie ensuite cette liste à l'aide de la fonction
    publish(camionId, data).
    
- publish(camionId, data):
    Publie un paquet MQTT à l'adresse spécifié en variable d'entrée sur 
    etudeje/camionId avec comme valeur l'identifiant de l'étiquette.

"""
def read(errorCount=0):
#    try:
    
    recep = proc.stdout.readline()
    if recep == "Segmentation fault\n":
        print("Segmentation fault")
        errorCount += 1
        return read()
    elif recep != "NTR\n":
        print(recep.split('\n')[0])
        return recep.split('\n')[0]
#    except:
#        return ''
        
def scan(l, errorCount = 0):
    print("Nombre d'itération",l)
    temp = []
    
    proc = Popen(["./scan", str(l)],stdout=PIPE, bufsize=1, universal_newlines=True )

    #print "Débug1"
    j = 0 # To be deleted
    while True:
        j += 1 # To be deleted
#        out, err = proc.communicate()
#        print out.splitlines()

        recep = proc.stdout.readline()
        print(recep)        
        if recep == "Segmentation fault\n" or recep == '' or recep == " ":
            print("Segmentation fault , error count  = {count}".format(count = errorCount))
            if errorCount + 1 > timeout:
                print("Timeout reached")
                proc.terminate()
                return 0
            else:
                scan(l, errorCount + 1)
            
        if recep == "end\n": #or j > 4*l+1:
            break
        
        recep = recep.rstrip('\n')
        #print(j, recep)
        if recep != None and recep != '' and recep not in temp:
            temp.append(recep)                                                   # On ajoute la valeur de l'étiquette si elle est non nulle
    
    proc.wait()
    print(temp)
    
    return 0    
"""
    if temp != []:
        publish(camionId, ["delete"])                                          # On supprime le contenu
        publish(camionId, temp)                                                # On publie la liste des etiquettes trouvées
    
    return 0
"""    
def publish(camionId, data):
    # Connexion au broker mqtt
    mqttc = mosquitto.Client()
    mqttc.connect(serverName, serverPort)
    
    for element in data:
        print("Publié :", element)
        mqttc.publish("etudeje/"+str(camionId), element)
        mqttc.loop(2)
    return 0
    
### INITIALISATION DU SCRIPT --------------------------------------------------
print("Initialisation du script")
time.sleep(1)

### LANCEMENT D'UN SCAN -------------------------------------------------------
#os.chdir("/home/pi/projetGRDF")
try:
    proces = Process(target=lambda : scan(nbIteration))
    proces.start()
    proces.join()
except KeyboardInterrupt:
    print('\nInterrupted')
    try:
        for child in active_children():
            print(child)
            child.terminate()
        sys.exit(0)
    except SystemExit:
        os._exit(0)
print("terminé")
### FIN DU SCRIPT -------------------------------------------------------------
