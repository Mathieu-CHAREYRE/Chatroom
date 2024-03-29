# client.py
 
### IMPORTS ###
 
import socket
from custom_format import *

 
### CONSTANTES ###
 
SERVER_ADDRESS = (socket.gethostname(),8081)
 
### VARIABLES ###
 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
 
### FONCTIONS ###

def start():
    print(f"""
     --------------------
 
       *** CHATROOM ***
 
         >> CLIENT <<
 
     --------------------
    """)
 
    print(f"Tentative de connexion sur {SERVER_ADDRESS[0]}:{SERVER_ADDRESS[1]}\n")

    try:
      client.connect(SERVER_ADDRESS)  # On se connecte au serveur
      client.setblocking(False)  # On met le socket en mode non bloquant pour pouvoir envoyer des messages même quand on essaye d'en recevoir

    except ConnectionResetError:
      print("""
                >> ECHEC DE CONNEXION <<

            Le serveur n'est pas disponible pour le moment.
            Veuillez réessayer plus tard.
            """)
      
      input("\nAppuyez sur Entrée pour quitter...")
      exit()
 
    username = str(input("Nom d'utilisateur : ")) # Choix de nom d'utilisateur
    client.send(enc_tuple(0, username)) # On envoie notre nom d'utilisateur
 
    while True:
      chat(username)
      
      try:
        recv_msg()  # On reçoit les messages du serveur
      except IOError:
        # Erreur attendue : on ne reçoit plus de message donc on passe à l'input pour envoyer un message
        continue
 
 
### FONCTIONS ###
 
def chat(username):
    msg = input(" > ")
 
    if "■" not in msg:
      # Pour la séparation dans la conversion tuple en string (c.f. custom_format.py)
 
      try:
         client.send(enc_tuple(username, msg))
 
      except:
         # Le serveur est arrété
 
         print("""
            >> ECHEC DE CONNEXION <<
 
        Le serveur semble avoir été arrêté.
        Fermeture de la connexion...
         """)
         input("\nAppuyez sur Entrée pour quitter...")
         exit()
 
    else:
      print("Le message ne peut pas contenir '■' ou '□'.")  # On ne veut pas de séparateur dans le message


def recv_msg():
    """
    Reçoit les messages du serveur et les affiche.
    """

    while True:
      # On recoit tous les messages extérieurs
      # La boucle va s'arréter avec une erreur quand plus aucun message n'est reçu
      data = dec_tuple(client.recv(1024),"□")  # On sépare les différents messages

      for msg in data:
        try:
          msg = msg.split("■")  # On sépare le nom d'utilisateur du message, pas besoin d'appeler dec_tuples()
          print(f"[ {msg[0]} ]  {msg[1]}")  # On l'affiche
        except IndexError:
          # On est arrivé à la fin des messages reçus, on continue
           continue


### EXECUTION ###

if __name__ == "__main__":
    start()