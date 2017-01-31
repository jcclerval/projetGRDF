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
import os
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
    Met à jour la BDD

- cleanDataBase():
    Nettoie la base de données des doublons
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
    camion = msg.topic.split('/')[-1]
    data = fetchData(camion, str(msg.payload))               # Sinon on envoie l'information
    updateData(camion, data)                                                   # On met à jour la BDD avec les infos recues
    # Suppression des doublons
#    cleanDataBase()
    return 0
    # Mise à jour de la base de donnees
def fetchData(camion, etiId):
    # Ici on va chercher les informations sur l'étiquette afin de l'ajouter dans les effectifs du camion
    # On fait une recherche dans la base de données des étiquettes afin de savoir le type
    # d'outil de l'objet scanné
    con = False
    try:
        print "Etiquette :", etiId
        con = mdb.connect(host=host, user=user, passwd=password, db=bdd)
        cur = con.cursor()
        cur.execute("SELECT type FROM etiquettes WHERE ref='{ref}';".format(ref=str(etiId)))
        temp = cur.fetchone()
        print temp[0]
    except mdb.Error, e:
      
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)
        
    finally:    
        if con:    
            con.close()
    try:        
        return temp[0]  # On renvoie l'id de l'outil concerné
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
    # On vient de recevoir l'Id d'un outil, on va alors ajouter cet item dans 
    # la liste des effectifs du camion.
    print "Data :",data
    con = False
    try:
        con = mdb.connect(host=host, user=user, passwd=password, db=bdd)
        cur = con.cursor()
        try:
            cur.execute("SELECT quantite FROM effectifs WHERE idcamion={camion} AND idoutil = {data};".format(camion=camion, data = data))
            qte = cur.fetchone()
            print qte
            if qte == None:
                print "None, on passe à un"
                qte = 1
                cur.execute("INSERT INTO effectifs VALUES(NULL, {camion}, {outil}, 1);".format(camion=camion, outil = data))
                print "Element ajouté"
            else:
                print "il y avait déjà quelque chose avant"
                qte = int(qte)
                qte += 1
                cur.execute("UPDATE effectifs SET quantite={quantite} WHERE idcamion={camion} AND idoutil = {data} ;".format(quantite=qte, camion=camion, data = data))
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
    
    """
def cleanDataBase():
    con = False
    try:
        con = mdb.connect(host=host, user=user, passwd=password, db=bdd)
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM effectifs WHERE idcamion={camion};".format(camion=camion))
            listOutils = cur.fetchone()
            outilsDic = {}
            for outils in listOutils:
                if outils in outilsDic:
                    outilsDic[outils] += 1
                else:
                    outilsDic[outils] = 0
            
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)
    finally:    
        if con:    
            con.close()
    return 0
    """
  
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