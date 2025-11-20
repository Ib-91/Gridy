import pandas

class Cellule:
    def __init__(self, texte):
        self.texte = texte # texte de la cellule
        self.valeur = None   # le résultat numérique
        self.en_cours = False  # pour détecter les cycles

def indice_to_colonne(ind): # convertir un indice en lettre de colonne
    resultat = ""
    while True:
        ind, reste = divmod(ind, 26)
        lettre = chr(ord('A') + reste)
        resultat = lettre + resultat
        if ind == 0:
            break
        ind -= 1
    return resultat

def creer_dico(fichier):
    nb_lignes, nb_colonnes = fichier.shape
    grille = {}

    for i in range(nb_lignes) : # index lignes
        for j in range(nb_colonnes) : # index colonnes
            lettre_colonne = indice_to_colonne(j)
            numero_ligne = i + 1
            nom_cellule = f"{lettre_colonne}{numero_ligne}" 
            texte = fichier.iat[i, j]  # texte de la cellule
            if pandas.isna(texte): # si la cellule est vide, on met une chaîne vide
                texte = "" 

            grille[nom_cellule] = Cellule(str(texte)) # ajouter la cellule au dictionnaire

    return grille


def evaluer_cellule(nom_cellule, dico):
   # pas encore implémenté
    cellule = dico[nom_cellule]

    if cellule.valeur is not None:
        return cellule.valeur
    if cellule.en_cours:
        raise ValueError(f"Cycle détecté dans la cellule {nom_cellule}")
    cellule.en_cours = True

    if cellule.texte.startswith('='):
        if cellule.texte.contains('SUM'):
            evaluer_somme(cellule, dico)

        if cellule.texte.contains('AVERAGE'):
            evaluer_average(cellule, dico)

        if cellule.texte.contains('IF'):
            evaluer_if(cellule, dico)

        if cellule.texte.contains('MAX'):
            evaluer_max(cellule, dico)  

        if cellule.texte.contains('MIN'):
            evaluer_min(cellule, dico)

        if cellule.texte.contains('COUNT'):
            evaluer_count(cellule, dico)

        if cellule.texte.contains('PRODUCT'):
            evaluer_product(cellule, dico)

        if cellule.texte.contains('COUNTA'): 
            evaluer_counta(cellule, dico)

        if cellule.texte.contains('MEDIAN'):
            evaluer_median(cellule, dico)
        
        try :
            eval(cellule.texte[1:],dico)
    else :
        try :
            cellule.valeur = float(cellule.texte)
        except ValueError :
            


# def calculer_valeurs(dico):





"""Programme principal"""



fichier = pandas.read_csv("test.csv", header=None) # lecture du fichier csv
nb_lignes, nb_colonnes = fichier.shape # compter les lignes et colonnes
dico = creer_dico(fichier) # On crée le dictionnaire des cellules avec leur texte brut
# afficher_dico(dico) # On affiche le dictionnaire des cellules

# calculer_valeurs(dico) # On appelle la fonction pour calculer les valeurs des cellules



