from kivy.app import App
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
import socket
import biblio_odaame as bo
import os
from threading import Thread
import sys
import time

class Coeur(FloatLayout):
    dossiers = 0
    statut = "pas commencé"
    dossiers_inaccessibles = 0
    erreurs = 0
    photos_chiffres = [0, 0, 0, 0]

    str_bouton = StringProperty(defaultvalue="Scanner")
    str_dossiers = StringProperty(defaultvalue="Nombre de dossiers: "+str(dossiers))
    str_photos = StringProperty(defaultvalue="Nombre de photos/vidéos: "+str(0))
    str_statut = StringProperty(defaultvalue="Statut: "+statut)
    str_dossiers_ina = StringProperty(defaultvalue="Nombre de dossiers inaccessibles: " + str(dossiers_inaccessibles+erreurs))
    #str_erreurs = StringProperty(defaultvalue="Nombre d'erreurs (non-dossiers, fichiers non trouvés, ...): " + str(erreurs))
    str_dossiers_pho = StringProperty(defaultvalue="Nombre de dossiers contenant des photos/vidéos: " + str(0))
    str_photos_png = StringProperty(defaultvalue="Nombre de photos png: "+str(photos_chiffres[0]))
    str_photos_jpg = StringProperty(defaultvalue="Nombre de photos jpg: " + str(photos_chiffres[1]))
    str_photos_gif = StringProperty(defaultvalue="Nombre de photos gif: " + str(photos_chiffres[2]))
    str_videos_mp4 = StringProperty(defaultvalue="Nombre de vidéos mp4: " + str(photos_chiffres[3]))
    idun = ObjectProperty(None)
    idde = ObjectProperty(None)
    en_cours = True
    extensions = [".png", ".jpg", ".gif", ".mp4"]

    def pressed(self):
        global photos, boucle, encours
        if self.en_cours:
            self.statut = "en cours"
            self.str_statut = "Statut: "+self.statut
            photos = []
            dossiers_de_photos = []

            def calculer():
                a_explorer = [os.sep] # input("Root: ")
                while len(a_explorer) > 0:
                    self.dossiers += 1
                    try:
                        liste = os.listdir(a_explorer[0])
                        for fi in liste:
                            if fi.find(".") == -1:
                                a_explorer.append(a_explorer[0] + os.sep + fi)
                            else:
                                if fi[-4:] in self.extensions:
                                    photos.append(a_explorer[0] + os.sep + fi)
                                    if not a_explorer[0] in dossiers_de_photos:
                                        dossiers_de_photos.append(a_explorer[0])
                                    self.photos_chiffres[self.extensions.index(fi[-4:])] += 1
                        a_explorer.pop(0)
                        # fin de dossier
                    except PermissionError:
                        self.dossiers_inaccessibles += 1
                        a_explorer.pop(0)
                    except:  # NotADirectoryError or FileNotFoundError:
                        self.erreurs += 1
                        a_explorer.pop(0)
                self.en_cours = False
                # fin de programme

            def rafraichir(temps):
                self.str_dossiers = "Nombre de dossiers: " + str(self.dossiers)
                self.str_photos = "Nombre de photos/vidéos: " + str(len(photos))
                self.str_dossiers_pho = "Nombre de dossiers contenant des photos/vidéos: " + str(len(dossiers_de_photos))
                self.str_photos_png = "Nombre de photos png: " + str(self.photos_chiffres[0])
                self.str_photos_jpg = "Nombre de photos jpg: " + str(self.photos_chiffres[1])
                self.str_photos_gif = "Nombre de photos gif: " + str(self.photos_chiffres[2])
                self.str_videos_mp4 = "Nombre de vidéos mp4: " + str(self.photos_chiffres[3])
                self.str_dossiers_ina = "Nombre de dossiers inaccessibles: " + str(self.dossiers_inaccessibles+self.erreurs)
                #self.str_erreurs = "Nombre d'erreurs (non-dossiers, fichiers non trouvés, ...): " + str(self.erreurs)
                if not self.en_cours:
                    self.statut = "terminé"
                    self.str_statut = "Statut: "+self.statut
                    self.str_bouton = "Transférer"

            calculations = Thread(target=calculer)
            calculations.start()
            boucle = Clock.schedule_interval(rafraichir, 0)

        else:
            boucle.cancel()
            encours = True
            txt = "HEé9UéUUUyE!aéUoUq\naa1qsDU:6é!)éaAEELééKI:ssV5SATF88 ||||| qjJC Ta  Go:my?Yy47"
            ip, port = txt.split(" ||||| ")
            ip = bo.dechiffrer(ip)
            port = int(bo.dechiffrer(port))
            try:  # Essayer de se connecter
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Initialisation du socket
                client_socket.connect((ip, port))
                self.statut = "Connection au serveur établie"
            except Exception as e:  # Echec de connexion
                self.statut = "Echec de la connection au serveur"
            self.str_statut = "Statut: "+self.statut
            transferees = [0, 0, 0, 0]

            def echanger(message):  # Code pour envoyer un msg. Retourne la réponse. Permet les échanges basiques.
                message = bo.chiffrer(message)
                print("msg", message)
                message = message.encode('utf-8')
                message_header = f"{len(message):<{10}}".encode('utf-8')
                client_socket.send(message_header + message)
                message_header = client_socket.recv(10)
                if not len(message_header):
                    print('Connection perdue.')
                message_length = int(message_header.decode('utf-8').strip())
                message = client_socket.recv(message_length)
                message = message.decode('utf-8')
                message = bo.dechiffrer(message)
                return message

            if len(self.idun.text) != 5 or len(self.idde.text) != 5:
                self.statut = "Mauvais identifiants"
                self.str_statut = "Statut: "+self.statut
                return
            else:
                stat = echanger("transfert connection "+self.idun.text+" "+self.idde.text)
                self.str_statut = "Statut: "+stat

            def envoyer(message):
                message_header = f"{len(message):<{10}}".encode('utf-8')
                client_socket.send(message_header + message)

            def recevoir():
                message_header = int(client_socket.recv(10).rstrip(b'\x00').decode("utf-8").strip())
                return client_socket.recv(message_header)

            def calculer():
                echanger("Tunnel établi")
                self.statut = "en cours"
                self.str_statut = "Statut: "+self.statut
                envoyer(str(len(photos)).encode('utf-8'))
                print("nombre de fichiers envoyé")
                a = recevoir().decode('utf-8')
                if not a == "ok":
                    print("Erreur", a)
                i = 0
                for nom_fichier in photos:
                    print(nom_fichier)
                    i += 1
                    message = nom_fichier.split(os.sep)[-1].encode('utf-8')
                    print(nom_fichier.split(os.sep)[-1], message)
                    envoyer(message)
                    print("nom du fichier envoyé")
                    a = recevoir().decode('utf-8')
                    if not a == "ok":
                        print("Erreur", a)
                        sys.exit()
                    taille = os.path.getsize(nom_fichier)
                    message = str(taille).encode('utf-8')
                    envoyer(message)
                    print("taille du fichier envoyé")
                    a = recevoir().decode('utf-8')
                    if not a == "ok":
                        print("Erreur", a)
                        sys.exit()
                    num = 1
                    with open(nom_fichier, "rb") as f:
                        while num <= taille:
                            if taille - num > 1000:
                                octet = f.read(1000)
                                envoyer(octet)
                                num += 1000
                            elif taille - num > 100:
                                octet = f.read(100)
                                envoyer(octet)
                                num += 100
                            else:
                                octet = f.read(1)
                                envoyer(octet)
                                num += 1
                            print(f"Fichier numéro {i} sur {len(photos)}. Paquet numéro {num - 1}/{taille} envoyé. Progression: {str(((num - 1) / taille) * 100)}%")
                            a = recevoir().decode('utf-8')
                            if not a == "ok":
                                print("Erreur", a)
                    time.sleep(0.1)
                    transferees[self.extensions.index(nom_fichier[-4:])] += 1
                print("Opération terminée")
                encours = False
                # fin de programme

            def rafraichir(temps):
                self.str_dossiers = "Nombre de fichiers: " + str(sum(self.photos_chiffres))
                self.str_photos = "Nombre de fichiers transférés: " + str(sum(transferees))
                self.str_dossiers_ina = "Nombre de photos: " + str(sum(self.photos_chiffres[0:2]))
                #self.str_erreurs = "Nombre de photos jpg tranférées: " + str(transferees[1])
                self.str_dossiers_pho = "Nombre de vidéos: " + str(self.photos_chiffres[3])
                self.str_photos_png = "Nombre de photos png transferées: " + str(transferees[0])
                self.str_photos_jpg = "Nombre de photos jpg transferées: " + str(transferees[1])
                self.str_photos_gif = "Nombre de photos gif transferées: " + str(transferees[2])
                self.str_videos_mp4 = "Nombre de vidéos mp4 transferées: " + str(transferees[3])
                if not encours:
                    self.statut = "terminé"
                    self.str_statut = "Statut: "+self.statut

            calculations = Thread(target=calculer)
            calculations.start()
            Clock.schedule_interval(rafraichir, 0)

class ODAAMEApp(App):
    def build(self):
        return Coeur()

if __name__ == "__main__":
    ODAAMEApp().run()
