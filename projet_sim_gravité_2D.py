#Le but est de faire tourner dans une fonction récursive une balle subissant la gravité
#equation gravité : G*((M1xM2)/d^2)

import time as time

import numpy

import pygame 
pygame.init() 
ecran = pygame.display.set_mode((600, 400))

#Constantes :
G=6.674184*10**-11 #m^3 kg^-1 s^-2
M1=float(input("donnez la masse de l'objet 1 en kg"))           #               5.9722*10**24     #masse du soleil#1.9884*10**30                     #5.9722*10**24  #masse de la terre, en kg
M2=float(input("donnez la masse de l'objet 2 en kg"))#masse de la balle, en kg
rayon_de_M1=int(input("donnez le rayon de M1 en m"))  #=6371000 #rayon du soleil#700000000  #rayon terre#6371000
rayon_de_M2=int(input("donnez le rayon de M2 en m"))  #=6371000 #rayon du soleil#700000000  #rayon terre#6371000
obj1_base={"x":float(input("donnez la coordonnée x de obj1 ")),"y":float(input("donnez la coordonnée y de obj1 ")),"Nx":0,"Ny":0,"accx":0,"accy":0, "vitx":float(input("donnez la vitesse x de obj1 en m/s")),"vity":float(input("donnez la vitesse y de obj1 ")), "M":M1}
obj2_base={"x":float(input("donnez la coordonnée x de obj2 ")),"y":float(input("donnez la coordonnée y de obj2 ")),"Nx":0,"Ny":0,"accx":0,"accy":0, "vitx":float(input("donnez la vitesse x de obj2 en m/s")),"vity":float(input("donnez la vitesse y de obj2 ")), "M":M2}

print(G,M1,M2)

def gravité_sim(obj1: dict, obj2: dict)-> dict:
    """
    dans cette fonction, je vais séparer les calculs pour x et pour y de chaque objet,
    ainsi je vais pouvoir leur appliquer un déplacement indépendant,
    et l'affichage, en réunissant les deux, va montrer les objets
    ndt: le pas de temps est de 1/6, et le sleep aussi, pour avoir un retour réaliste avec 1sec de simulée = 1 sec IRL, mais pour avoir un affichage et une simulation plus réaliste et plus lisible, on peut réduire le pas de temps pour éviter les énormes "bonds", et augmenter le sleep pour la lisibilité ou le diminuer pour que ça avance plus vite
    """
    distance_obj1_obj2=numpy.sqrt((obj2["x"]-obj1["x"])**2+(obj2["y"]-obj1["y"])**2)  #calcul de la distance entre les deux centres
    distance_obj1_obj2_x=(obj2["x"]-obj1["x"])
    distance_obj1_obj2_y=(obj2["y"]-obj1["y"])
    force_newton = G*((M1*M2)/((distance_obj1_obj2)**2))    
    force_newton_x= distance_obj1_obj2_x/distance_obj1_obj2*force_newton  #ici, je "réparti" la force en fonction de la distance de x1,X2 et y1,y2"
    force_newton_y= distance_obj1_obj2_y/distance_obj1_obj2*force_newton
    obj1["Nx"]=force_newton_x  
    obj1["Ny"]=force_newton_y
    obj2["Nx"]=-force_newton_x  #négatif, pour que les deux n'aillent pas dans la meme direction
    obj2["Ny"]=-force_newton_y
    print("avant calculs : ", obj1, obj2) #debug pour détécter les abérrations possibles entre deux appels

    obj1["accx"] = obj1["Nx"]/obj1["M"] #je calcule l'accélération de la balle avec la force calculée juste avant
    obj1["accy"] = obj1["Ny"]/obj1["M"] #je calcule l'accélération de la balle avec la force calculée juste avant
    obj2["accx"] = obj2["Nx"]/obj2["M"] #je calcule l'accélération de la balle avec la force calculée juste avant
    obj2["accy"] = obj2["Ny"]/obj2["M"] #je calcule l'accélération de la balle avec la force calculée juste avant
    pas_de_temps=1/50
    obj1["vitx"]+=obj1["accx"]*pas_de_temps #je met à jour la vitesse de l'objet
    obj1["vity"]+=obj1["accy"]*pas_de_temps #je met à jour la vitesse de l'objet

    obj2["vitx"]+=obj2["accx"]*pas_de_temps #je met à jour la vitesse de l'objet
    obj2["vity"]+=obj2["accy"]*pas_de_temps #je met à jour la vitesse de l'objet

    obj1_pos_post_calc={"x":obj1["x"], "y":obj1["y"] }#je sauvegarde les position des objets avant leur modification comme ça le calcul n'est pas influencé par quel position est changée en premier
    obj2_pos_post_calc={"x":obj2["x"], "y":obj2["y"] }

    obj1["x"] += obj1["vitx"]*pas_de_temps #je met à jour sa coordonnée en aplliquant la vitesse en m/s
    obj1["y"] += obj1["vity"]*pas_de_temps #je met à jour sa coordonnée en aplliquant la vitesse en m/s

    obj2["x"] += obj2["vitx"]*pas_de_temps#je met à jour sa coordonnée en aplliquant la vitesse en m/s
    obj2["y"] += obj2["vity"]*pas_de_temps#je met à jour sa coordonnée en aplliquant la vitesse en m/s


    if obj1["x"]==obj2["x"] and obj1["y"]==obj2["y"]:   #je m'arrete seulement si les deux sont au meme endroit, je pourrais aussi vérifier si ils se touchent, en utilisant leur rayon.
        pygame.event.pump()
        time.sleep(0.1) #j'attend une sec pour la lisibilité
        dessiner_scene(ecran, obj1,obj2) #je redessine la balle avec sa coordonnée mise à jour
        pygame.display.flip()
        print("apres calculs : ", obj1, obj2) #debug, vérifier que les données sont cohérentes
        return -1
    else:

        pygame.event.pump()
        time.sleep(pas_de_temps) #j'attens le pas de temps pour avoir une simulation à 1sec simulée = 1sec IRL
        dessiner_scene(ecran, obj1,obj2) #je redessine la balle avec sa coordonnée mise à jour
        pygame.display.flip()
        print("apres calculs : ", obj1, obj2) #debug, vérifier que les données sont cohérentes
        return gravité_sim(obj1,obj2) # je réappelle la fonction avec toutes les données mise à jour


# caca code écrit par chat gpt ( en gros c'est l'affichage de la balle avec pygame ) flemme de le faire moi meme + c pas l'ex

def dessiner_scene(ecran, obj1, obj2):
    largeur, hauteur = 600, 400
    centre_x, centre_y = largeur // 2, hauteur // 2

    # échelle calculée une seule fois, à partir des positions initiales, puis figée
    if not hasattr(dessiner_scene, "echelle"):
        etendue = max(
            abs(obj1["x"]), abs(obj1["y"]),
            abs(obj2["x"]), abs(obj2["y"]),
            1  # évite une division par zéro si tout est à l'origine
        )
        marge = 50
        dessiner_scene.echelle = (min(centre_x, centre_y) - marge) / etendue

    echelle = dessiner_scene.echelle

    ecran.fill((255, 255, 255))

    # rayon affiché : proportionnel au rayon réel, avec un minimum de lisibilité
    rayon1 = max(6, int(rayon_de_M1 * echelle))
    rayon2 = max(4, int(rayon_de_M2 * echelle))

    x1 = centre_x + int(obj1["x"] * echelle)
    y1 = centre_y - int(obj1["y"] * echelle)  # inversion : y écran vers le bas
    x2 = centre_x + int(obj2["x"] * echelle)
    y2 = centre_y - int(obj2["y"] * echelle)

    pygame.draw.circle(ecran, (255, 200, 0), (x1, y1), rayon1)  # obj1
    pygame.draw.circle(ecran, (255, 0, 0), (x2, y2), rayon2)    # obj2

# j'ai modifié l'appel de fonction brute, maintenant on peut y ajouter une force, et modifier la hauteure, 


gravité_sim(obj1_base,obj2_base)