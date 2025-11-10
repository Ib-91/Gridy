# Gridy
Projet Tableur non interactif du module "Langages de script" en L3 Informatique parcours Administration Système et Réseaux. Le projet est réalisé en groupe, le nom du groupe est FIA (CHANDRASSEGARANE Félicien, IBRAHIM Ibrahim et MBA EMANE Axel). Le but de ce projet est de développer un outil pour calculer les formules dans un fichier CSV.

Noyau minimal et fonctionnalités:
-Ouvrir un fichier csv #1
-Lire un fichier CSV.#2 (dépend de #1)
-Compter le nombre de colonne et de ligne #3 (dépend de #2)
- Utiliser ces valeurs pour créer un dictionnaire de cellules dans lequel la clé sera le numéro de la cellule et la valeur sera le contenu #4 (dépend de #3 )
- Identifier les cellules qui commencent avec un égale (identifier les formules) #5 (dépend de #4)
- Interpréter la formule puis évaluer le résultat #6 (dépend de #5)
-Générer un nouveau tableau contenant les résultats #7 (dépend de #6)
-Coder des fonctions (SUM, MAX, MIN, AVG...etc) #8 (dépend de #6)
-Créer un fichier csv contenant ce tableau #9 (dépend de #7)

Supplémentaires:
-Gérer les erreurs : Formule invalide et afficher des messages d'erreur (dépend de #6) comme (#SYNTAXE! dépend de #5), boucle (#CYCLE! dépend de #4)