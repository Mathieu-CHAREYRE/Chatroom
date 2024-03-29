# custom_format.py

### FONCTIONS ###

def enc_tuple(t_0, t_1):
    """
    Permet de coder un tuple (a,b) en string au format 'a■b'.
    """

    data = str(t_0) + "■" + t_1
    return data.encode()


def dec_tuple(data, separator="■"):
    """
    Permet de décoder une string au format 'a■b' en tuple (a,b).
    """
    
    if separator == "□":
        messages = data.decode().split(separator)   # Liste des messages
        return messages

    else:
        t_0, t_1 = data.decode().split(separator)   # On sépare au niveau du séparateur

        try:
            # On définit le type de message en int
            t_0 = int(t_0)
        except ValueError:
            # Le type est le nom d'utilisateur (str) donc on ne fait rien
            pass

        return (t_0, t_1)