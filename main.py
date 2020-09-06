from kivy.app import App
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
import socket
import os
from threading import Thread
import sys
import time
from random import randint

class bo():
    def chiffrer(self, A):
        Liste = []  # Décomposition du message en liste
        i = 0
        while i != len(A):
            Liste.append(A[i])
            i += 1
        i = 0
        while i != len(A):
            Liste[i] = self.coeur_chiffrer(Liste[i])
            i += 1
        A = str()
        i = 0
        while i != len(Liste):
            A = str(A) + str(Liste[i])
            i += 1
        i = 0
        while i != 5:
            A = self.coeur_chiffrer(A)
            i += 1
        return A

    def coeur_chiffrer(self, A):
        clef_1 = {" ": "n", "é": "!", "a": " ", "b": "l", "c": "X", "d": "w", "e": "R", "f": "s", "g": "é", "h": "2",
                  "i": "a",
                  "j": "P", "k": "e", "l": "H", "m": "G", "n": ",", "o": "?", "p": "Y", "q": ".", "r": "1", "s": "0",
                  "t": "Z",
                  "u": "c", "v": "S", "w": "t", "x": "I", "y": "|", "z": "'", "'": "q", "A": ":", "B": "/", "C": "U",
                  "D": "j",
                  "E": "k", "F": "N", "G": "6", "H": "D", "I": "u", "J": "x", "K": "f", "L": "4", "M": "F", "N": "3",
                  "O": "Q",
                  "P": "h", "Q": "K", "R": "W", "S": "y", "T": "9", "U": "p", "W": "5", "X": "-", "Y": "T", "Z": "C",
                  "(": "z",
                  "0": "E", "1": "o", "2": "g", "3": "d", "4": "(", "5": "v", "6": "b", "7": "A", "8": "J", "9": "V",
                  ".": "r",
                  "?": "O", ")": "i", "!": ")", ",": "M", "/": "L", "V": "\n", "\n": "8", "|": "7", ":": "B", "-": "m"}
        clef_2 = ['O', 'l', 'm', 'T', 'u', 'p', 'x', 'W', 'P', 'd', 'C', 'a', 'Z', '!', 'Y', '(', 'S', 'D', 'q', 'N',
                  'g',
                  '9', '1', 'G', 'R', '0', 't', '.', '8', 'A', '|', 'b', '-', 'F', ',', 'J', 'r', 'E', 'H', 'L', 'e',
                  '4',
                  'Q', '/', 'j', '7', '?', 'U', 'i', 'I', '2', 'K', 'y', '3', 'c', 'w', '6', 'B', ':', ' ', 'é', 'h',
                  ')',
                  'k', 'v', 'o', 'M', 's', '5', 'f', 'n', "'", "\n", "z", "X", "V"]
        clef_3 = {"0": "2", "1": "4", "2": "3", "3": "9", "4": "8", "5": "7", "6": "0", "7": "1", "8": "6", "9": "5"}
        Liste = []  # commencer substitution
        Liste2 = []
        i = 0
        while i != len(A):  # Décomposition du message en liste
            Liste.append(A[i])
            i += 1
        i = 0
        while i != len(Liste):  # Substitution par liste parallèle avec clef 1
            mot = Liste[i]
            Liste2.append(clef_1[mot])
            i += 1  # fin substitution
        transpo = randint(10, 70)
        i = 0
        Liste = []
        while i != len(Liste2):
            index = clef_2.index(Liste2[i])
            index = index + transpo
            x = len(Liste)
            while len(Liste) == x:
                try:  # Si on va plus loin que la len de la clef on retourne au début
                    Liste.append(clef_2[index])
                except:
                    index -= 76
            i += 1
        A = str(transpo)
        i = 0
        Liste2 = []
        while i != 2:  # Décomposition du message en liste
            Liste2.append(A[i])
            i += 1
        i = 0
        while i != len(Liste2):  # Substitution par liste parallèle avec clef 3
            mot = Liste2[i]
            Liste.append(clef_3[mot])
            i += 1  # fin substitution
        A = str()
        i = 0
        while i != len(Liste):
            A = str(A) + str(Liste[i])
            i += 1
        return A

    def dechiffrer(self, D):
        i = 0
        while i != 5:
            D = self.coeur_dechiffrer(D)
            i += 1
        Liste = []  # Décomposition du message en liste
        Liste2 = []
        i = 0
        while i != len(D):
            Liste.append(D[i])
            i += 1
        groupe = ''
        i = 0
        while i != len(Liste):
            groupe = groupe + Liste[i]
            if len(groupe) == 3:
                Liste2.append(groupe)
                groupe = ''
            i += 1
        i = 0
        while i != len(Liste2):
            Liste2[i] = self.coeur_dechiffrer(Liste2[i])
            i += 1
        D = str()
        i = 0
        while i != len(Liste2):
            D = str(D) + str(Liste2[i])
            i += 1
        return D

    def coeur_dechiffrer(self, D):
        clef_2 = ['O', 'l', 'm', 'T', 'u', 'p', 'x', 'W', 'P', 'd', 'C', 'a', 'Z', '!', 'Y', '(', 'S', 'D', 'q', 'N',
                  'g',
                  '9', '1', 'G', 'R', '0', 't', '.', '8', 'A', '|', 'b', '-', 'F', ',', 'J', 'r', 'E', 'H', 'L', 'e',
                  '4',
                  'Q', '/', 'j', '7', '?', 'U', 'i', 'I', '2', 'K', 'y', '3', 'c', 'w', '6', 'B', ':', ' ', 'é', 'h',
                  ')',
                  'k', 'v', 'o', 'M', 's', '5', 'f', 'n', "'", "\n", "z", "X", "V"]
        clef_4 = {"n": " ", "!": "é", " ": "a", "l": "b", "X": "c", "w": "d", "R": "e", "s": "f", "é": "g", "2": "h",
                  "a": "i",
                  "P": "j", "e": "k", "H": "l", "G": "m", ",": "n", "?": "o", "Y": "p", ".": "q", "1": "r", "0": "s",
                  "Z": "t",
                  "c": "u", "S": "v", "t": "w", "I": "x", "7": "|", "q": "'", "'": "z", "B": ":", "/": "B", "U": "C",
                  "j": "D",
                  "k": "E", "N": "F", "6": "G", "D": "H", "u": "I", "x": "J", "f": "K", "4": "L", "F": "M", "3": "N",
                  "Q": "O",
                  "h": "P", "K": "Q", "W": "R", "y": "S", "9": "T", "p": "U", "5": "W", "m": "-", "T": "Y", "C": "Z",
                  "z": "(",
                  "E": "0", "o": "1", "g": "2", "d": "3", "(": "4", "v": "5", "b": "6", "A": "7", "J": "8", "V": "9",
                  "r": ".",
                  "O": "?", "i": ")", ")": "!", "M": ",", "L": "/", "8": "\n", "\n": "V", "|": "y", ":": "A", "-": "X"}
        clef_5 = {"0": "6", "1": "7", "2": "0", "3": "2", "4": "1", "5": "9", "6": "8", "7": "5", "8": "4", "9": "3"}
        Liste = []
        Liste2 = []
        i = 0
        while i != len(D):  # Décomposition du message en liste
            Liste.append(str(D[i]))
            i += 1
        try:
            Liste[-2] = clef_5[Liste[-2]]
            Liste[-1] = clef_5[Liste[-1]]
        except:
            print(Liste)
        Transpo = Liste[-2] + Liste[-1]
        Transpo = int(Transpo)
        Liste.pop(-1)
        Liste.pop(-1)
        i = 0
        while i != len(Liste):  # Décomposition du message en liste
            index = clef_2.index(Liste[i])
            index = index - Transpo
            if index < 0:
                index += 76
            Liste2.append(clef_2[index])
            i += 1
        Liste = []
        i = 0
        while i != len(Liste2):  # Substitution par liste parallèle avec clef 1
            mot = Liste2[i]
            mot = clef_4[mot]
            Liste.append(mot)
            i += 1  # fin substitution
        D = str()
        i = 0
        while i != len(Liste):
            D = str(D) + str(Liste[i])
            i += 1
        return D

class Coeur(FloatLayout):
    dossiers = 0
    statut = "pas commencé"
    dossiers_inaccessibles = 0
    photos_chiffres = [0, 0, 0, 0]

    str_bouton = StringProperty(defaultvalue="Scanner")
    str_dossiers = StringProperty(defaultvalue="Nombre de dossiers: "+str(dossiers))
    str_photos = StringProperty(defaultvalue="Nombre de photos/vidéos: "+str(0))
    str_statut = StringProperty(defaultvalue="Statut: "+statut)
    str_dossiers_ina = StringProperty(defaultvalue="Nombre de dossiers inaccessibles: " + str(dossiers_inaccessibles))
    #str_erreurs = StringProperty(defaultvalue="Nombre d'erreurs (non-dossiers, fichiers non trouvés, ...): " + str(erreurs))
    str_dossiers_pho = StringProperty(defaultvalue="Nombre de dossiers contenant des photos/vidéos: " + str(0))
    str_photos_png = StringProperty(defaultvalue="Nombre de photos png: "+str(photos_chiffres[0]))
    str_photos_jpg = StringProperty(defaultvalue="Nombre de photos jpg: " + str(photos_chiffres[1]))
    str_photos_gif = StringProperty(defaultvalue="Nombre de photos gif: " + str(photos_chiffres[2]))
    str_videos_mp4 = StringProperty(defaultvalue="Nombre de vidéos mp4: " + str(photos_chiffres[3]))
    idun = ObjectProperty(None)
    idde = ObjectProperty(None)
    en_cours = True

    def pressed(self):
        global photos, boucle, encours
        if self.en_cours:
            self.statut = "en cours"
            self.str_statut = "Statut: "+self.statut
            photos = []
            dossiers_de_photos = []

            def calculer():
                sep = os.sep
                a_explorer = [sep] # input("Root: ")
                while len(a_explorer) > 0:
                    self.dossiers += 1
                    try:
                        liste = os.listdir(a_explorer[0])
                        for fi in liste:
                            if fi.find(".") == -1:
                                a_explorer.append(a_explorer[0] + sep + fi)
                            else:
                                if fi[-4:] in [".png", ".jpg", ".gif", ".mp4"]:
                                    photos.append(a_explorer[0] + sep + fi)
                                    if not a_explorer[0] in dossiers_de_photos:
                                        dossiers_de_photos.append(a_explorer[0])
                                    self.photos_chiffres[[".png", ".jpg", ".gif", ".mp4"].index(fi[-4:])] += 1
                        # fin de dossier
                    except:
                        self.dossiers_inaccessibles += 1
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
