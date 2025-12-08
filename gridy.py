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

def colonne_to_indice(colonne): # convertit une lettre de colonne (A,B,C,...etc) en indice (0,1,2,...)
    ind = 0
    for lettre in colonne:
        ind = ind * 26 + (ord(lettre.upper()) - ord('A') + 1)
    return ind - 1


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

def AVG(*args): # fonction pour calculer la moyenne
    return sum(args) / len(args) if args else 0


class Eval(dict):
    def __init__(self, tab):
        self.tab = tab  # dico des Cellule
        super().__init__()

        self["SUM"] = self.SUM # méthode de la classe
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
    
    def get_pos(self, name):
        # "B12" devient (1, 12), "A20" devient (0, 20)
        col = ''
        row = ''
        for char in name:
            if char.isalpha():
                col += char
            elif char.isdigit():
                row += char
            else:
                return "#ERREUR"
        col_ind = colonne_to_indice(col)
        row_ind = int(row)
        return col_ind, row_ind

    def SUM(self, *args):
        total = 0

        for arg in args:

            # Cas 1, plage "A1:B5"
            if isinstance(arg, str) and ":" in arg:
                cell1, cell2 = arg.split(':')
                col1, row1 = self.get_pos(cell1)
                col2, row2 = self.get_pos(cell2)

                # Erreur dans get_pos
                if isinstance(col1, str) or isinstance(col2, str):
                    return "#ERREUR"

                for row in range(min(row1, row2), max(row1, row2) + 1):
                    for col in range(min(col1, col2), max(col1, col2) + 1):
                        cell_name = f"{indice_to_colonne(col)}{row}"
                        if cell_name not in self.tab:
                            continue  # cellule qui n'existe pas
                        val = self[cell_name] #eval.__getitem__(cell_name)

                        #erreur on la renvoie
                        if isinstance(val, str) and val.startswith("#"):
                            return val

                        if isinstance(val, (int, float)):
                            total += val
                continue # Fin du Cas 1

            # Cas 2, cellule unique "A1"
            if isinstance(arg, str):
                val = self[arg]

                if isinstance(val, str) and val.startswith("#"):
                    return val

                if isinstance(val, (int, float)):
                    total += val

                continue

            # Cas 3, SUM(A1, 5, B2)
            if isinstance(arg, (int, float)):
                total += arg
                continue

            # Cas 4 à voir ( A:A colonne , 1:1 ligne , inverse des plages, Ignorer le texte, etc)
            continue

        return total


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
