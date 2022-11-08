'''

Author : Touimer Amin
Date: November 2022
Jeu: Escape Game

But du jeu ?

Le jeu consiste à sortir du labyrinthe en ramassant tous les objets necessaires ainsi
qu'en déverouillant les différentes portes en répondant à divers questions.
Une fois tous les objets récupérer et toutes les portes déverouillées, la victoire est assurée

'''
################################ IMPORTATION ###########################################

import turtle
from CONFIGS import *

################################ CONFIGURATION #########################################

DISTANCE_LARGEUR = ZONE_PLAN_MAXI[0] - ZONE_PLAN_MINI[0]
DISTANCE_HAUTEUR = ZONE_PLAN_MAXI[1] - ZONE_PLAN_MINI[1]
position = (0, 1)

################################ FONCTION ##############################################


def lire_matrice(fichier):

    """
    Renvoie le plan du château sous forme d'une liste de liste
    en recevant comme paramètre le fichier à lire

    :param fichier:
    :return:

    """
    with open(fichier, encoding="utf-8") as f:
        castle = []
        for line in f.readlines():
            liste = []
            for i in range(len(line.split())):
                liste.append(int(line.split()[i]))  #Transformation de chaque string en un nombre
            castle.append(liste)
        return castle


plan = lire_matrice(fichier_plan)


def creer_dictionnaire_des_objets(fichier_des_objets):
    with open(fichier_des_objets,encoding='utf-8') as objet:
        res = ''
        d= {}
        for i in objet:
            res += i
            a, b = eval(res)
            d[a] = b
            res = ''
        return d


dico_objet = creer_dictionnaire_des_objets(fichier_objets)
dico_question_reponse = creer_dictionnaire_des_objets(fichier_questions)


def calculer_pas(plan):

    """
    Calcule la longeur d'un côté d'une case

    :param plan:
    :return:

    """
    case_hauteur = DISTANCE_HAUTEUR / len(plan)
    case_largeur = DISTANCE_LARGEUR / len(plan[0])
    if case_hauteur > case_largeur or case_hauteur == case_largeur: res = case_largeur
    else: res = case_hauteur
    return res


def coordonnees(case, deplacement):  #case = coordonnées de y x dans la matrice

    """
    Renvoie les coordonnées en pixels Turtle d'une case grâce aux
    coordonnées d'un point du plan

    :param case:
    :param deplacement:
    :return:

    """

    x = ZONE_PLAN_MINI[0] + (deplacement * case[1]) #Transformation en pixel turtle
    y = (ZONE_PLAN_MAXI[1]-deplacement) - (deplacement * case[0]) #Transformation en pixel turtle
    return (x,y)


def tracer_carre(deplacement):

    """
    Traçage d'un carré en fonction de la longueur du déplacement

    :param deplacement:
    :return:

    """

    turtle.pencolor(COULEUR_COULOIR)
    for k in range(4):
        turtle.forward(deplacement)
        turtle.left(90)


def tracer_case(case, couleur,deplacement):

    """
    Tracer une case d'une certaine coordonnée et d'une certaine couleur
    à un certain endroit. Le deplacement ici, représente la distance entre deux cases.

    :param case:
    :param couleur:
    :param deplacement:
    :return:

    """
    turtle.up()
    turtle.goto(case)
    turtle.down()
    turtle.color(couleur)
    turtle.begin_fill()
    tracer_carre(deplacement)
    turtle.end_fill()
    turtle.up()


def afficher_plan(plan):

    """
    Affichage du plan

    :param plan:
    :return:

    """

    for i in range(len(plan)): #Coordonnée de y du plan
        for j in range(len(plan[0])): #Coordonnée de x du plan

            """Condtions de remplissage d'une case"""

            if plan[i][j] == 0: couleur_remplissage= COULEURS[0]
            elif plan[i][j] == 1: couleur_remplissage = COULEURS[1]
            elif plan[i][j] == 2: couleur_remplissage = COULEURS[2]
            elif plan[i][j] == 3: couleur_remplissage = COULEURS[3]
            else: couleur_remplissage = COULEURS[4]
            turtle.tracer(0)
            tracer_case(coordonnees((i, j), calculer_pas(plan)), couleur_remplissage, calculer_pas(plan)) #Calcul de l'emplacement de la case


def deplacer(m,p,mouvement):
    global matrice,position
    position = (p[0] + mouvement[0],p[1] + mouvement[1])
    tracer_case(coordonnees((position[0] - mouvement[0], position[1] - mouvement[1]), m), COULEUR_VUE,m)

    """Conditions pour pouvoir se déplacer sur le plan"""

    if plan[position[0]][position[1]] == 0: dessin(m)
    elif plan[position[0]][position[1]] == 3:  poser_question(plan,position,mouvement)
    elif plan[position[0]][position[1]] == 4: dessin(m); ramasser_objet()
    elif plan[position[0]][position[1]] == 2:dessin(m);turtle.pencolor("black");afficher_annonce("Felicitations !")
    else:position = (p[0],p[1]) ; dessin(m)


def deplacer_gauche(): # X -1
    mouvement = (0,-1)
    deplacer(calculer_pas(plan),position,mouvement)
    turtle.onkeypress(deplacer_gauche, "Left")


def deplacer_droite(): # X +1
    mouvement = (0,1)
    deplacer(calculer_pas(plan),position,mouvement)
    turtle.onkeypress(deplacer_droite, "Right")


def deplacer_haut(): # y-1
    mouvement = (-1,0)
    deplacer(calculer_pas(plan),position,mouvement)
    turtle.onkeypress(deplacer_haut, "Up")


def deplacer_bas(): # y +1
    mouvement = (1,0)
    deplacer(calculer_pas(plan),position,mouvement)
    turtle.onkeypress(deplacer_bas, "Down")


def dessin(m):
    turtle.up()
    turtle.goto(coordonnees(position, m))
    coord_pixel_turtle = coordonnees(position, m)
    turtle.goto(coord_pixel_turtle[0] + (m / 2), coord_pixel_turtle[1] + (m/ 2))
    turtle.down()
    turtle.dot(RATIO_PERSONNAGE * m, "red")


def ramasser_objet():
    afficher_inventaire(dico_objet[position])
    afficher_annonce("Vous avez trouvé : "+ dico_objet[position])


def afficher_annonce(annonce):
    turtle.up()
    turtle.goto(POINT_AFFICHAGE_ANNONCES)
    turtle.down()
    turtle.write(annonce,font=("Verdana",8, "bold"))


def afficher_inventaire(objet):
    turtle.up()
    turtle.goto(POINT_AFFICHAGE_INVENTAIRE)
    turtle.down()
    turtle.pencolor("black")
    turtle.write(" ▏"+ objet,font=("Verdana",10, "bold"))


def poser_question(matrice, case, mouvement):

    joueur = turtle.textinput("Question",dico_question_reponse[case][0])
    if joueur == dico_question_reponse[case][1]:
        turtle.listen()
        turtle.pencolor("black")
        afficher_annonce("Bonne réponse ! La porte s'ouvre.")
        dessin(calculer_pas(matrice))
    else:
        turtle.listen()
        turtle.pencolor("black")
        afficher_annonce("Mauvaise réponse ! La porte est fermé :/")
        poser_question(plan,position,mouvement)


def event():
    turtle.listen()
    turtle.onkeypress(deplacer_gauche, "Left")
    turtle.onkeypress(deplacer_droite, "Right")
    turtle.onkeypress(deplacer_haut, "Up")
    turtle.onkeypress(deplacer_bas, "Down")
    turtle.mainloop()


def jeu():
    afficher_plan(plan)
    dessin(calculer_pas(plan))
    event()

#################################### JEU ####################################################

jeu()


"""
A faire

- Effacer la derniere annonce à chaque fois
- Tous les objets de l'inventaire s'affiche au même endroit
- Quand une porte est ouverte si on repasse sur la même case on doit encore répondre à la question

"""