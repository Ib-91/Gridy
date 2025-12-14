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


class Eval(dict):
    def __init__(self, tab):
        self.tab = tab  # dico des Cellule
        super().__init__()

        self["SUM"] = self.SUM # méthode de la classe
        self["PRODUCT"] = self.PRODUCT
        self["AVG"] = self.AVG
        self["MIN"] = self.MIN        
        self["MAX"] = self.MAX
        self["CONCAT"] = self.CONCAT
        self["LEN"] = self.LEN #nombre de caractères dans une cellule
        self["COUNT"] = self.COUNT #les valeurs numériques
        self["COUNTA"] =self.COUNTA #toutes les valeurs non vides

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
    
    def get_pos(self, nom_cellule):
        # "B12" devient (1, 12), "A20" devient (0, 20)
        col = ''
        row = ''
        for char in nom_cellule:
            if char.isalpha():
                col += char
            elif char.isdigit():
                row += char
            else:
                return "#ERREURSYNTAXE"
        col_ind = colonne_to_indice(col)
        row_ind = int(row)
        return col_ind, row_ind
    
    def LEN(self, arg):
        #cellule unique "A1"
        if isinstance(arg, str) and arg in self.tab:
            val = self[arg]
            if isinstance(val, str) and val.startswith("#"):
                return val
            return len(str(val))
        #valeur directe
        return len(str(arg))
    
    def analyse_args(self, *args):
        # FONCTION(A1, "B2:B5", "texte", 5, ...)
        for arg in args:

            #plage A1:B5
            if isinstance(arg, str) and ":" in arg:
                cell1, cell2 = arg.split(":")

                pos1 = self.get_pos(cell1)
                pos2 = self.get_pos(cell2)
                if isinstance(pos1, str) or isinstance(pos2, str):
                    yield "#ERREURSYNTAXE"
                    return
                col1, row1 = pos1
                col2, row2 = pos2
                for row in range(min(row1, row2), max(row1, row2) + 1):
                    for col in range(min(col1, col2), max(col1, col2) + 1):
                        cellule_nom = f"{indice_to_colonne(col)}{row}"
                        if cellule_nom in self.tab:
                            yield self[cellule_nom]          
            #cellule unique "A1"
            elif isinstance(arg, str) and arg in self.tab:
                yield self[arg]
            #valeur directe
            else:
                yield arg

    def SUM(self, *args):
        total = 0
        for val in self.analyse_args(*args):
            if isinstance(val, str) and val.startswith("#"):
                return val
            if isinstance(val, (int, float)):
                total += val
        return total

    
    def PRODUCT(self, *args):
        produit = 1
        for val in self.analyse_args(*args):
            if isinstance(val, str) and val.startswith("#"):
                return val
            if isinstance(val, (int, float)):
                produit *= val
        return produit
    
    def CONCAT(self, *args):
        resultat = ""
        for val in self.analyse_args(*args):
            if isinstance(val, str) and val.startswith("#"):
                return val
            resultat += str(val)
        return resultat
    
    def AVG(self, *args):
        total = 0
        count = 0
        for val in self.analyse_args(*args):
            if isinstance(val, str) and val.startswith("#"):
                return val
            if isinstance(val, (int, float)):
                total += val
                count += 1
        if count == 0:
            return 0
        return total / count

    
    def MIN(self, *args):
        valeurs = []
        for val in self.analyse_args(*args):
            if isinstance(val, str) and val.startswith("#"):
                return val
            if isinstance(val, (int, float)):
                valeurs.append(val)
        if valeurs == []:
            return 0
        return min(valeurs)


    def MAX(self, *args):
        valeurs = []
        for val in self.analyse_args(*args):
            if isinstance(val, str) and val.startswith("#"):
                return val
            if isinstance(val, (int, float)):
                valeurs.append(val)
        if valeurs == []:
            return 0
        return max(valeurs)
    
    def COUNT(self, *args):
        count = 0
        for val in self.analyse_args(*args):
            if isinstance(val, str) and val.startswith("#"):
                return val
            if isinstance(val, (int, float)):
                count += 1
        return count

    
    def COUNTA(self, *args):
        count = 0
        for val in self.analyse_args(*args):
            if isinstance(val, str) and val.startswith("#"):
                return val
            if val != "":
                count += 1
        return count



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


def generer_csv(dico, nb_lignes, nb_colonnes, nom_fichier):
    data = []
    for i in range(nb_lignes):
        ligne = []
        for j in range(nb_colonnes):
            nom_cellule = f"{indice_to_colonne(j)}{i+1}"
            val = dico[nom_cellule].valeur
            if val is None:
                val = ""
            ligne.append(val)
        data.append(ligne)

    df_resultat = pandas.DataFrame(data)
    df_resultat.to_csv(nom_fichier, header=False, index=False)

"""Programme principal"""

fichier = pandas.read_csv("test.csv", header=None)
dico = creer_dico(fichier)

calculer_valeurs(dico)
afficher_dico(dico)
nb_lignes, nb_colonnes = fichier.shape
generer_csv(dico, nb_lignes, nb_colonnes, "resultat.csv")
