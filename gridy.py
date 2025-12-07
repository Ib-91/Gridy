import pandas


class Cellule:
    def __init__(self, texte):
        self.texte = texte      # texte brut de la cellule (ex: "3", "=A1+2")
        self.valeur = None      # valeur numérique ou texte après calcul
        self.en_cours = False   # pour détecter les cycles


def indice_to_colonne(ind): # convertit un indice (0,1,2,...) en lettre de colonne (A,B,C,...etc)
    resultat = ""
    while True:
        ind, reste = divmod(ind, 26)
        lettre = chr(ord('A') + reste)
        resultat = lettre + resultat
        if ind == 0:
            break
        ind -= 1
    return resultat


def creer_dico(fichier): # crée le dictionnaire à partir du fichier pandas
    nb_lignes, nb_colonnes = fichier.shape
    grille = {}

    for i in range(nb_lignes):
        for j in range(nb_colonnes):
            lettre_colonne = indice_to_colonne(j)
            numero_ligne = i + 1
            nom_cellule = f"{lettre_colonne}{numero_ligne}"

            texte = fichier.iat[i, j] # récupère le texte de la cellule [i,j]
            if pandas.isna(texte): 
                texte = ""

            grille[nom_cellule] = Cellule(str(texte))

    return grille


def SUM(*args): # fonction pour calculer la somme
    return sum(args)


def AVG(*args): # fonction pour calculer la moyenne
    return sum(args) / len(args) if args else 0


class Eval(dict):
    def __init__(self, tab):
        self.tab = tab  # dico des Cellule
        super().__init__()

        self["SUM"] = SUM
        self["AVG"] = AVG
        self["MAX"] = max
        self["MIN"] = min

    def __getitem__(self, cle):

        # si on a déja la valeur calculée on la renvoie
        if cle in self:
            return super().__getitem__(cle)

        # sinon, on récupère la cellule
        cellule = self.tab[cle]

        # pour détecter si il y a un cycle
        if cellule.en_cours:
            cellule.valeur = "#CYCLE"
            self[cle] = cellule.valeur
            return cellule.valeur

        cellule.en_cours = True


        texte = cellule.texte.strip() # on récupère le texte de la cellule

        if not texte.startswith("="):
            # si ce n'est pas une formule :
            if texte == "": # si c'est une chaine vide on laisse
                val = ""
            else: # si ce n'est pas une chaine vide :
                try: # on essaye de convertir en nombre
                    val = float(texte)
                except ValueError: # si erreur alors on écrit juste le texte
                    val = texte
        else:
            # si c'est une formule, on enlève le = au début et on évalue
            formule = texte[1:]
            try:
                val = eval(formule, self) # on évalue en utilisant le dictionnaire de valeurs comme environnement
            except Exception: # si l'évaluation échoue il y a une erreur
                val = "#ERREUR"

        cellule.en_cours = False 
        cellule.valeur = val
        self[cle] = val
        return val



def calculer_valeurs(dico): # calcule toutes les cellules
    valeurs = Eval(dico)
    for cle in dico:
        valeurs[cle]


def afficher_dico(dico):
    affichage = []

    for nom in sorted(dico.keys()):
        cellule = dico[nom]
        valeur_str = str(cellule.valeur) if cellule.valeur is not None else "None"
        line = f"'{nom}' : ('{cellule.texte}', {valeur_str})"
        affichage.append(line)

    print("--- Affichage du Dictionnaire des Cellules ---")
    print("{")
    print(",\n".join(affichage))
    print("}")
    print("------------------------------------------")


"""Programme principal"""

fichier = pandas.read_csv("test.csv", header=None)
dico = creer_dico(fichier)

calculer_valeurs(dico)
afficher_dico(dico)
