# server.py
 
### IMPORTS ###
 
import socket
import select
from custom_format import *
 

### FONCTIONS ###
 
def start():
    print(f"""
     --------------------
 
       *** CHATROOM ***
 
         >> SERVER <<
 
     --------------------
    """)
 
    server.bind(ADDRESS)    # On lance le serveur sur l'adresse et le port voulu
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    # On définit l'option de réutiliser notre adresse même si elle est occupé (si le serveur ne s'est pas bien éteint)
    print(f"Server running on {socket.gethostname()}:{ADDRESS[1]}")
 
    server.listen(200)    # On attend une connexion. Max 200 connexions
    print("Waiting for client connection...\n")
 
    # On commence alors le chat
    stream()
 
 
def stream():
    """
    La boucle qui permet de garder le serveur en route.
    """
 
    while True:

        # On créé une liste des sockets qui vérifient l'activité de chaque socket
        read_sockets, _, _ = select.select(socket_list, [], [])    # select.select renvoie un tuple de trois listes. On veut uniquement read_sockets (sockets actives)

        for new_sock in read_sockets:
            # On itère sur chaque socket active
 
            if new_sock == server:

                # Nouvelle connexion
                client_socket, address = server.accept()    # On accepte les nouvelles connexions
                socket_list.append(client_socket)   # On ajoute la nouvelle connexion à notre liste de connexions

                try:
                    username = recv_data(client_socket)[1]
                except TypeError:
                    # recv_data() a renvoyé False donc essayer d'accéder l'élément d'indice 1 renvoie une erreur
                    # L'utilisateur s'est déconnecté avant d'entrer un nom d'utilisateur
                    socket_list.remove(client_socket)
                    continue
                
                print(f"Nouvelle connexion de {username} sur {address[0]} : {address[1]}")
                user_dict[client_socket] = username
 

            else:
                # Message
                data = recv_data(new_sock)
 
                if data:
                    # On affiche uniquement les données reçus ne sont pas vides/False
                    print(f"[ {data[0]} ]  {data[1]}")  # On affiche le message ainsi que l'utilisateur qui l'a envoyé
                    broadcast(data, new_sock)
                else:
                    # Si les données sont vides on ne fait rien (la connexion s'est fermée du côté client)
                    print(f"Déconnexion de {user_dict[new_sock]}")

                    socket_list.remove(new_sock)
                    user_dict.pop(new_sock)
 

def recv_data(client_socket):
    try:
        data = dec_tuple(client_socket.recv(1024))  # On reçoit les données et on les décode en format lisible

        if data[0] == '':
            # Déconnexion d'un utilisateur
            return False
        else:
            return data
 
    except:
        # Déconnexion brutale d'un utilisateur
        return False


def broadcast(data, new_sock):
    """
    Permet de renvoyer un message reçu à tous les utilisateurs connectés.
    """

    data = enc_tuple(data[0],data[1]+"□")  # On encode le message avec un séparateur pour differer les messages
    # On est obligé de les séparer pour éviter des erreurs si l'utilisateur récoit plusieurs messages avant d'en envoyer un

    for client in user_dict:
        # On itère sur toutes les sockets activent
        if client != new_sock:
            # On ne renvoie pas à l'auteur du message
            client.send(data)  # On renvoie le message à chaque socket


### CONSTANTES ###
 
ADDRESS = ('', 8081)    # '' est pareil que 'localhost' mais permet une connexion depuis les autres appareils du réseau
 

### VARIABLES ###
 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # On définit le type de serveur
socket_list = [server]  # La liste de tous les sockets
user_dict = {}  # Va contenir tous les utilisateurs connectés avec leur socket respective comme clé


### EXECUTION ###

if __name__ == "__main__":
    start()