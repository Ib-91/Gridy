# Gridy

Projet Tableur non interactif du module "Langages de script" en L3 Informatique parcours Administration Système et Réseaux. Le projet est réalisé en groupe, le nom du groupe est FIA (CHANDRASSEGARANE Félicien, IBRAHIM Ibrahim et MBA EMANE Axel). 
Le but de ce projet est de développer un outil, un tableur non interactif permettant d'évaluer des formules présentes dans un fichier CSV.

Chaque cellule du CSV peut contenir :
- Une valeur simple (nombre ou texte),
- Une **formule** (commençant par `=`) pouvant inclure :
  - des références à des cellules (`A1`, `C12`, etc.),
  - des références à des plages de cellules (`A1:A20`, `B3:C15`, etc.),
  - des opérations arithmétiques (`+`, `-`, `*`, `/`),
  - des appels à des fonctions (`SUM`, `AVG`, `MIN`, etc.).

L’outil doit :
- évaluer les formules
- tenir compte des dépendances entre cellules
- détecter les cycles
- détecter les erreurs
- générer un **nouveau fichier CSV** contenant les valeurs finales.

## Bibliothèques utilisées
- **pandas**


## Structure du code

Les cellules sont modélisées avec une classe Cellule qui a comme attributs le texte brut, la valeur apres calcul et un attribut booléen pour la gestion de cycle.

Pour calculer les valeurs récursivement et gérer les longues dépendances, on utilise une classe eval qui hérite de dict.

Le système de calcul fonctionne avec le __getitem__ dans la classe Eval. Lors du calcul d'une cellule, on appelle la fonction eval() en passant en paramètre notre objet de la classe Eval, qui joue le rôle de dictionnaire de valeurs. En modifiant le getitem, l'appel à la fonction eval utilisera le getitem, qui calcule la cellule demandée si elle n'est pas encore calculée, et déclenchera d'autres appels de manière récursive si il y a une dépendance.



Algorithme :

- On commence par ouvrir et lire le fichier CSV. On crée ensuite un dictionnaire représentant la grille, avec comme clé le nom de la cellule(A1,A2...) et comme valeur un objet de type cellule.
- On va ensuite simplement parcourir toutes les cases et forcer le calcul sur chacune grâce à l'objet Eval.
- On termine par re générer un fichier csv en écrivant les valeurs de chaque cellule.


## Répartition du travail
- CHANDRASSEGARANE Félicien
    Gestion du fonctionnement interne du tableur avec le getitem (récursion, analyse, cycles et erreurs) avec utilisation du eval avec dictionnaire dynamique, et conception des structures de données principales (dictionnaire, self). 
    Implémentation des classes eval(__init__ && __getitem__) et cellule(__init__)

- IBRAHIM Ibrahim
    Gestion/Implémentation complète des fonctions  de calcul (SUM, AVG...etc) et textuelles (CONCAT,LEN) 
    Gestion de la logique de traitement de tout type d'arguments et des plages de cellules

- MBA EMANE Axel
    Extraction et analyse du csv, transformation en données utilisables et création des objets cellules. 
    Implémentation des algorithmes de conversion entre lettres de colonnes et indices numériques (colonne_to_indice, indice_to_colonne).
    Structuration des données sous forme de dictionnaire
    Affichage final
