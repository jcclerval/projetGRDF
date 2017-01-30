# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Created on Tue Nov 29 21:14:30 2016

@author: Jean-Christophe Clerval
"""

### IMPORTS NECESSAIRES -------------------------------------------------------
import MySQLdb as mdb
import paho.mqtt.client as mqtt
import sys
import time
## Définition des variables ---------------------------------------------------
serverName = "bord3l"
serverPort = 1883

bdd = 'u925639974_grdf'
host = 'localhost'
user = 'root'
password = 'jcclerval'
## ----------------------------------------------------------------------------

### FONCTIONS UTILES ----------------------------------------------------------
"""
Liste des fonctions utiles :
- on_connect():
    Definit le comportement du broker lorsqu'une connexion a lieu.

- on_message():
    Definit le comportement lors de la reception d'un message.
    
- fetchData(camion, etiId):
    Récupère les informations concernant l'outil selectionné et lance
    updateData().

- updateData(camion, data):
    Met à jour la BDD.
"""
def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("etudeje/+")

def on_message(client, userdata, msg):
    # A la reception d'un message ...
    print "Topic: ", msg.topic+'\nMessage: '+str(msg.payload)                  # On affiche le message
    if str(msg.payload) == "delete":                                           # Si le message contient la commande "delete"
        print "delete content"
        deleteContent(msg.topic.split('/')[-1])                                # On supprime tout
        return 0
    fetchData(msg.topic.split('/')[-1], str(msg.payload))                      # Sinon on envoie l'information
    return 0
    # Mise à jour de la base de donnees
def fetchData(camion, etiId):
    # Ici on va chercher les informations sur l'étiquette afin de l'ajouter dans les effectifs du camion
    con = False
    try:
        print "Etiquette :", etiId
        con = mdb.connect(host=host, user=user, passwd=password, db=bdd)
        cur = con.cursor()
        cur.execute("SELECT id FROM outils WHERE ref='{ref}';".format(ref=str(etiId)))
        temp = cur.fetchone()
        print temp[0]
    except mdb.Error, e:
      
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)
        
    finally:    
        if con:    
            con.close()
    try:        
        updateData(camion, temp[0])
    except:
        pass
    return 0
    
def deleteContent(camionId):
    con = False
    try:
        con = mdb.connect(host=host, user=user, passwd=password, db=bdd)
        cur = con.cursor()
        try:
            cur.execute("DELETE FROM effectifs WHERE idcamion={camionId};".format(camionId=camionId))
            print "Ancien contenu supprimé"
        except:
            pass
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)
    finally:    
        if con:    
            con.close()
    return 0
def updateData(camion, data):
    print "Data :",data
    con = False
    try:
        con = mdb.connect(host=host, user=user, passwd=password, db=bdd)
        cur = con.cursor()
        try:
            cur.execute("INSERT INTO effectifs VALUES({data0}, {data1}, '{data2}', {data3});".format(data0 = str('NULL'), data1 = int(camion), data2 = str(data), data3 = int(1)))
            print "Element ajouté"
        except:
            pass
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)
    finally:    
        if con:    
            con.close()
    return 0
  
### INITIALISATION DU SCRIPT --------------------------------------------------
print "Initialisation du script"
time.sleep(10)

### LANCEMENT DE l'ECOUTE------------------------------------------------------
try:
    client = mqtt.Client()
    client.connect(serverName,serverPort,60)
    
    client.on_connect = on_connect
    client.on_message = on_message
    
    client.loop_forever()
    
    sys.exit(0)
except KeyboardInterrupt:
    print '\nInterrupted'
    sys.exit(0)
except SystemExit:
    os._exit(0)