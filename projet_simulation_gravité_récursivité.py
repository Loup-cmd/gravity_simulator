#Le but est de faire tourner dans une fonction récursive une balle subissant la gravité
#equation gravité : G*((M1xM2)/d^2)

import time as time

import pygame 
pygame.init() 
ecran = pygame.display.set_mode((600, 400))

#Constantes :
G=6.674184*10**-11 #m^3 kg^-1 s^-2
M1=5.9722*10**24  #masse de la terre, en kg
M2=1000               #masse de la balle, en kg


print(G,M1,M2)

vitesse_obj=0

def gravité_sim(coordonnée_obj: float, accélération_f: float, vitesse_obj: float)-> float:

    force_newton = -G*((M1*M2)/((6371000+coordonnée_obj)**2))  #je considère que le sol est en y=0

    print("avant calculs : coordonnées: ",coordonnée_obj,"accélération: ",accélération_f,"force_newton: ",force_newton) #debug pour détécter les abérrations possibles entre deux appels

    accélération_f = force_newton/M2 #je calcule l'accélération de la balle avec la force calculée juste avant

    vitesse_obj+=accélération_f*(1/60) #je met à jour la vitesse de l'objet

    coordonnée_obj += vitesse_obj #je met à jour sa coordonnée en aplliquant la vitesse en m/s

    if coordonnée_obj==0 or coordonnée_obj<0: #si l'objet atteint le sol ( ou le dépasse car vitesse assez grande ) 
        pygame.event.pump()
        dessiner_scene(ecran, coordonnée_obj,350) #je redessine la balle avec sa coordonnée mise à jour
        
        pygame.display.flip()
        
        print("coordonnées: ",coordonnée_obj,"accélération: ",accélération_f,"force_newton: ",force_newton) #debug, vérifier que les données sont cohérentes

        return coordonnée_obj #je met fin à la boucle
    else:
        pygame.event.pump()
        time.sleep(0.5) #j'attend une sec pour la lisibilité
        dessiner_scene(ecran, coordonnée_obj,350) #je redessine la balle avec sa coordonnée mise à jour
        pygame.display.flip()
        print("coordonnées: ",coordonnée_obj,"accélération: ",accélération_f,"force_newton: ",force_newton) #debug, vérifier que les données sont cohérentes
        return gravité_sim(coordonnée_obj,accélération_f, vitesse_obj) # je réappelle la fonction avec toutes les données mise à jour


# caca code écrit pas chat gpt ( en gros c'est l'affichage de la balle avec pygame ) flemme de le faire moi meme + c pas l'ex

def dessiner_scene(ecran, y_balle, y_sol):
    # zoom calculé une seule fois, au tout premier appel, puis figé
    if not hasattr(dessiner_scene, "echelle"):
        marge = 50
        dessiner_scene.echelle = min((y_sol - marge) / max(y_balle, 1), 10)
    echelle = dessiner_scene.echelle

    # taille de la balle : rétrécit légèrement avec l'altitude, avec un minimum
    rayon_max = 20
    rayon_min = 6
    rayon = max(rayon_min, rayon_max - y_balle * 0.01)

    ecran.fill((255, 255, 255))
    y_balle_ecran = y_sol - y_balle * echelle - 20

    pygame.draw.circle(ecran, (255, 0, 0), (300, int(y_balle_ecran)), int(rayon))
    pygame.draw.line(ecran, (0, 0, 0), (0, y_sol), (600, y_sol), 5)


# j'ai modifié l'appel de fonction brute, maintenant on peut y ajouter une force, et modifier la hauteure, 
h=float(input("hauteur de la balle par rapport au sol ( en metres )"))
a=float(input("accélération de la balle ?"))

v=float(input("vitesse de la balle ?( m/s )"))

gravité_sim(h,a,v)