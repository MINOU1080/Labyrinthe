'''

Author : MINOU
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
INVENTAIRE = (70,180)
TORTUE_GOMME = turtle.Turtle()
position = (0, 1)
REGLEMENT =  "★★★Lancelot entre dans le château au sommet du Python des Neiges,\n" \
             "muni de son précieux sac de rangement et de sa\n" \
             "torche fraîchement allumée aux feux de Beltane. Il doit trouver son chemin.★★★\n" \
             " \n"\
             "○Tâche 1: Ramasse tous les objets !\n" \
             " \n"\
             "○Tâche 2 : Résous les enigmes grâce aux objets ramasser.\n" \
             " \n"\
             "○Tâche 3: Ne pas se faire manger par le Monstre du château !"
################################ FONCTION ##############################################


def lire_matrice(fichier):

    """ Renvoie le plan du château sous forme d'une liste de liste
    en recevant comme paramètre le fichier à lire."""

    with open(fichier, encoding="utf-8") as f:
        castle = []
        for line in f.readlines():
            liste = []
            for i in range(len(line.split())):
                liste.append(int(line.split()[i]))  #Transformation de chaque string en un nombre
            castle.append(liste)
        return castle


def creer_dictionnaire_des_objets(fichier_des_objets):

    """Renvoie un dictionnaire des objets ou des portes en fonction
    du fichier de lecture. """

    with open(fichier_des_objets,encoding='utf-8') as objet:
        res,d = '', {}
        for i in objet:
            res += i
            a, b = eval(res)
            d[a], res = b,''
        return d


def calculer_pas(plan):

    """ Calcule la longeur d'un côté d'une case. """

    case_hauteur,case_largeur = DISTANCE_HAUTEUR / len(plan),DISTANCE_LARGEUR / len(plan[0])
    res = min(case_hauteur,case_largeur)
    return res


def coordonnees(case, deplacement):  #case = coordonnées de y x dans la matrice

    """ Renvoie les coordonnées en pixels Turtle d'une case grâce aux
    coordonnées d'un point du plan. """

    x,y = ZONE_PLAN_MINI[0] + (deplacement * case[1]),(ZONE_PLAN_MAXI[1]-deplacement) - (deplacement * case[0]) #Transformation en pixel turtle
    return (x,y)


def tracer_carre(deplacement):

    """ Traçage d'un carré en fonction de la longueur du déplacement. """

    turtle.pencolor(COULEUR_COULOIR)
    for k in range(4):
        turtle.forward(deplacement)
        turtle.left(90)


def tracer_case(case, couleur,deplacement):

    """  Tracer une case d'une certaine coordonnée et d'une certaine couleur
    à un certain endroit. Le deplacement ici, représente la distance entre deux cases.  """

    turtle.up()
    turtle.goto(case)
    turtle.down()
    turtle.color(couleur)
    turtle.begin_fill()
    tracer_carre(deplacement)
    turtle.end_fill()
    turtle.up()


def afficher_plan(plan):

    """ Affichage du plan avec coloriage des cases."""

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

    """Permet au joueur de se déplacer sur le plan (m)
    en fonction de son mouvement (fonctions des déplacements du joueurs, gauche,droite,ect...),
    la position sera mise à jour à chaque mouvement du joueur."""

    global matrice,position
    position = (p[0] + mouvement[0],p[1] + mouvement[1])
    tracer_case(coordonnees((position[0] - mouvement[0], position[1] - mouvement[1]), m), COULEUR_VUE,m)
    """Conditions pour pouvoir se déplacer sur le plan"""
    if plan[position[0]][position[1]] == 0:
        dessin(m)
    elif plan[position[0]][position[1]] == 3:
        poser_question(plan,position,mouvement)
    elif plan[position[0]][position[1]] == 4:
        dessin(m)
        ramasser_objet()
    elif plan[position[0]][position[1]] == 2:
        dessin(m)
        position = (p[0], p[1])
        fin_jeu()
    else:
        position = (p[0],p[1])
        dessin(m)


def deplacer_gauche(): # X -1

    """Permet au joueur de se déplacer vers la gauche."""

    mouvement = (0,-1)
    deplacer(calculer_pas(plan),position,mouvement)
    turtle.onkeypress(deplacer_gauche, "Left")


def deplacer_droite(): # X +1

    """Permet au joueur de se déplacer vers la droite."""

    mouvement = (0,1)
    deplacer(calculer_pas(plan),position,mouvement)
    turtle.onkeypress(deplacer_droite, "Right")


def deplacer_haut(): # y-1

    """Permet au joueur de se déplacer vers le haut."""

    mouvement = (-1,0)
    deplacer(calculer_pas(plan),position,mouvement)
    turtle.onkeypress(deplacer_haut, "Up")


def deplacer_bas(): # y +1

    """Permet au joueur de se déplacer vers le bas."""

    mouvement = (1,0)
    deplacer(calculer_pas(plan),position,mouvement)
    turtle.onkeypress(deplacer_bas, "Down")


def dessin(m):

    """Dessine le personnage à l'emplacement adéquat."""

    turtle.up()
    turtle.goto(coordonnees(position, m))
    coord_pixel_turtle = coordonnees(position, m)
    turtle.goto(coord_pixel_turtle[0] + (m / 2), coord_pixel_turtle[1] + (m/ 2))
    turtle.down()
    turtle.dot(RATIO_PERSONNAGE * m, "red")


def ramasser_objet():

    """Permet de rammasser un objet qui se trouve sur une certaine case."""

    global INVENTAIRE
    if position in dico_objet:
        afficher_inventaire(dico_objet[position])
        afficher_annonce("Vous avez trouvé : " + dico_objet[position])
    suppression_objet()
    INVENTAIRE = (INVENTAIRE[0],INVENTAIRE[1] - 30)


def afficher_annonce(annonce):

    """Permet d'afficher l'annonce dans le bandeau d'annonce"""

    TORTUE_GOMME.clear()
    TORTUE_GOMME.up()
    TORTUE_GOMME.goto(POINT_AFFICHAGE_ANNONCES)
    TORTUE_GOMME.down()
    TORTUE_GOMME.write(annonce, font=("Verdana", 8, "bold"))


def afficher_inventaire(objet):

    """Permet d'ajouter l'objet ramasser dans l'inventaire."""

    turtle.up()
    turtle.goto(INVENTAIRE)
    turtle.down()
    turtle.pencolor("black")
    turtle.write(" ▏" + objet, font=("Verdana", 8, "bold"))


def poser_question(matrice, case, mouvement):

    """Permet de poser une question au joueur quand il passe sur
    case qui contient une question."""

    if position in dico_question_reponse:
        reponse = turtle.textinput("Question", dico_question_reponse[case][0])
        if reponse == dico_question_reponse[case][1]:
            turtle.listen()
            turtle.pencolor("black")
            afficher_annonce("Bonne réponse ! La porte s'ouvre.")
            dessin(calculer_pas(matrice))
        else:
            turtle.listen()
            turtle.pencolor("black")
            afficher_annonce("Mauvaise réponse ! La porte est fermé :/")
            poser_question(plan, position, mouvement)
    suppression_porte()


def suppression_porte():

    """Permet de supprimer une porte dans le dictionnaire des portes."""

    try: del dico_question_reponse[position]
    except: print(end='')


def suppression_objet():

    """Permet de supprimer un objet dans le dictionnaire des objets."""

    try: del dico_objet[position]
    except: print(end='')


def event():
    turtle.listen()
    turtle.onkeypress(deplacer_gauche, "Left")
    turtle.onkeypress(deplacer_droite, "Right")
    turtle.onkeypress(deplacer_haut, "Up")
    turtle.onkeypress(deplacer_bas, "Down")
    turtle.mainloop()


def jeu():

    """Fonction principale du jeu, fait appel à toutes les fonctions afin
    de lancer le jeu."""

    afficher_plan(plan)
    dessin(calculer_pas(plan))
    turtle.up()
    turtle.goto(POINT_AFFICHAGE_INVENTAIRE)
    turtle.down()
    turtle.pencolor("black")
    turtle.write("Inventaire : ", font=("Verdana", 10, "bold"))
    event()


def fin_jeu():

    """Permet de mettre fin au déroulement du jeu en donnant la victoire au joueur"""
    turtle.hideturtle()
    turtle.pencolor("black")
    afficher_annonce("Felicitations ! Vous avez terminé le jeu !")
    pseudo = turtle.textinput("Félicitations !", "Veuillez entrer votre pseudo")
    afficher_annonce(" ")
    turtle.clear()
    turtle.up()
    turtle.goto(-150,0)
    turtle.down()
    turtle.pencolor("red")
    turtle.write("Victoire de "+ pseudo, font=("Verdana", 20, "bold"))


def objectif():

    """Permet d'afficher les objectifs à réaliser au joueur."""

    turtle.hideturtle()
    turtle.up()
    turtle.goto(-240,75)
    turtle.down()
    turtle.pencolor("black")
    turtle.write(REGLEMENT, font=("Verdana", 8, "bold"))
    lancement_jeu = turtle.textinput("Objectif.", "Après avoir lu les objectifs veuillez,taper ok.")

    if lancement_jeu == "ok": turtle.clear()
    else: objectif()


#################################### JEU ####################################################


dico_objet,dico_question_reponse,plan = creer_dictionnaire_des_objets(fichier_objets),creer_dictionnaire_des_objets(fichier_questions),lire_matrice(fichier_plan)

objectif()
jeu()
