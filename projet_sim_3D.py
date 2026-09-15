#Le but est de simuler la gravité dans un univers composé de n objets, nE[0,+infini]

import time as time

import numpy


#Constantes :
G=6.674184*10**-11 #m^3 kg^-1 s^-2
MASSE_DICT=[]

#CETTE LISTE EST ULTRA IMPORTANTE: 
#nouvelle méthode pour pouvoir manipuler un nombre indéfini d'objets au lieu de 2 max
#maintenant univers[0] est le premier objet, univers[n+1] est le suivant
#chaque indice est un dictionnaire contenant les meme données que qu'avant
#ainsi je peux rajouter dynamiquement des objets et les gérer "plus facilement"
#
#EXEMPLE D'UNIVERS :
#
#[
# {"x":0,"y":0,"z":0,"accx":0,"accy":0, "accz":0,"vitx":0,"vity":0,"vitz":0, "M":2.5*(10**19), "R_o": 1300},
#{"x":3000,"y":0,"z":1000,"accx":0,"accy":0, "accz":0,"vitx":0,"vity":750,"vitz":-200, "M":1*(10**15),"R_o: 1000"}
# ]

univers=[]

JSON_or_NOT=int(input("Est ce qu'un JSON nommé ""univers.json"" contenant les infos sur les objets de la simulation sous la forme réglementaire est présent dans le répertoire du fichier ? 1 si oui, 0 si non :"))

if JSON_or_NOT==1:
    import os
    import json

    DOSSIER_SCRIPT = os.path.dirname(os.path.abspath(__file__))
    CHEMIN_JSON = os.path.join(DOSSIER_SCRIPT, "univers.json")

    with open(CHEMIN_JSON, "r", encoding="utf-8") as f:
        univers = json.load(f)

else:
    print("bon courage pour tout rentrer...")
    nb_objets=int(input("combien d'objets dans la simulation ?"))

    print("en fait flm de te faire rentrer les données une par une, tu vas jamais t'en sortir, économises nous du temps à tout les deux et mets un JSON ")


def gravité_sim(univers:list)-> list:
    global G
    while True:
        """
        dans cette fonction, je vais séparer les calculs pour x ,y et z de chaque objet,
        ainsi je vais pouvoir leur appliquer un déplacement indépendant,
        et l'affichage, en réunissant les 3, va montrer les objets
        chaque étape est expliquée de manière détaillée avec des commentaires
        """
        """
        ok alors en gros là, je parcours tous les éléments de l'univers, et je calcule la distance entre un objet, et les prochains, puis je passe au prochain
        comme ça la distance entre chaque objet est calculée
        ensuite,le résultat est stocké dans un dictionnaire, sous forme:
        [{(0, '<->', 1): np.float64(3162.2776601683795)},....,....] ( là c'est la distance entre univers[0] et univers[1])
        je dois calculer la distance entre chaque objet, pour ensuite calculer leur force d'attraction entre chaqun, 
        car ils s'infulencent tous entres eux
        c'est principalement ce qui a rendu le passage de "simulation entre 2 objets" -> "simulation n objets" nE[0,+infini] difficile
        et a rendu l'utilisation de dictionnaires et de listes manipulables nécessaire
        """
        distances_dict={}
        for i in range(len(univers)):
            for j in range(i + 1, len(univers)):

                distance = numpy.sqrt(
                    (univers[j]["x"]-univers[i]["x"])**2+
                    (univers[j]["y"]-univers[i]["y"])**2+
                    (univers[j]["z"]-univers[i]["z"])**2)

                distances_dict[i, "<->", j] = distance

        distances_dict_x={}
        for i in range(len(univers)):
            for j in range(i+1, len(univers)):
                distance_x = (univers[j]["x"]-univers[i]["x"])
                distances_dict_x[i, "<->", j]=distance_x

        distances_dict_y={}
        for i in range(len(univers)):
            for j in range(i+1, len(univers)):
                distance_y = (univers[j]["y"]-univers[i]["y"])
                distances_dict_y[i, "<->", j]=distance_y

        distances_dict_z={}
        for i in range(len(univers)):
            for j in range(i+1, len(univers)):
                distance_z = (univers[j]["z"]-univers[i]["z"])
                distances_dict_z[i, "<->", j]=distance_z

        #distance_obj1_obj2_x=(obj2["x"]-obj1["x"])#ancien systeme
        #distance_obj1_obj2_y=(obj2["y"]-obj1["y"])
        #distance_obj1_obj2_z=(obj2["z"]-obj1["z"])

        """
        je fais la meme chose pour le calcul de la force newtonienne, 
        """

        force_newton_dict={}
        for i in range(len(univers)):
            for j in range(i+1,len(univers)):
                force_newton=G*((univers[i]["M"]*univers[j]["M"])/((distances_dict[i,"<->",j])**2))
                force_newton_dict[i,"<->",j]=force_newton

        force_newton_dict_x={}
        for i in range(len(univers)):
            for j in range(i+1,len(univers)):
                force_newton_x=distances_dict_x[i,"<->",j]/distances_dict[i,"<->",j]*force_newton_dict[i,"<->",j]
                force_newton_dict_x[i,"<->",j]=force_newton_x
        
        force_newton_dict_y={}
        for i in range(len(univers)):
            for j in range(i+1,len(univers)):
                force_newton_y=distances_dict_y[i,"<->",j]/distances_dict[i,"<->",j]*force_newton_dict[i,"<->",j]
                force_newton_dict_y[i,"<->",j]=force_newton_y
        
        force_newton_dict_z={}
        for i in range(len(univers)):
            for j in range(i+1,len(univers)):
                force_newton_z=distances_dict_z[i,"<->",j]/distances_dict[i,"<->",j]*force_newton_dict[i,"<->",j]
                force_newton_dict_z[i,"<->",j]=force_newton_z
        

        #force_newton = G*((M1*M2)/((distance_obj1_obj2)**2))    
        #force_newton_x= distance_obj1_obj2_x/distance_obj1_obj2*force_newton  #ici, je "réparti" la force en fonction de la distance de x1,X2 et y1,y2"
        #force_newton_y= distance_obj1_obj2_y/distance_obj1_obj2*force_newton
        #force_newton_z=distance_obj1_obj2_z/distance_obj1_obj2*force_newton



        #obj1["Nx"]=force_newton_x  
        #obj1["Ny"]=force_newton_y
        #obj1["Nz"]=force_newton_z
        #obj2["Nx"]=-force_newton_x  #négatif, pour que les deux n'aillent pas dans la meme direction
        #obj2["Ny"]=-force_newton_y
        #obj2["Nz"]=-force_newton_z

        #print("avant calculs : ", univers) #debug pour détécter les abérrations possibles entre deux appels

        """
        okok, alors là c'etait troooooooop dur, mais j'ai fini par trouver :
        je parcours les clefs du dictionnaire avec tous les rapports de force newton entre chaque objet
        puis dans chaque je vérifie si l'objet que je calcule actuellement fait partie d'un des deux éléments de la valeur
        si c'est le premier, l'accélération est positive
        si c'est le deuxieme, elle est négative ( 3e loi de newton le goat )
        c'est possible parceque le nom des clefs est adapté pour indiquer à quelle pair objet appartient quelle force
        puis j'ajoute le résultat à mon dico, 
        qui recense donc pour chaque objet  accélération(x) de objet 1 <=> univers[0]["accx"] , = accx_dict[0]
        """
        accx_dict_x={}
        for i in range(len(univers)):
            accx=0
            for cle in force_newton_dict_x:
                if cle[0]==i: 
                    accx+=force_newton_dict_x[cle]/univers[i]["M"]
                elif cle[2]==i:
                    accx+=-force_newton_dict_x[cle]/univers[i]["M"]        
            accx_dict_x[i]=accx


        accy_dict_y={}
        for i in range(len(univers)):
            accy=0
            for cle in force_newton_dict_y:
                if cle[0]==i: 
                    accy+=force_newton_dict_y[cle]/univers[i]["M"]
                elif cle[2]==i:
                    accy+=-force_newton_dict_y[cle]/univers[i]["M"]        
            accy_dict_y[i]=accy


        accz_dict_z={}
        for i in range(len(univers)):
            accz=0
            for cle in force_newton_dict_z:
                if cle[0]==i: 
                    accz+=force_newton_dict_z[cle]/univers[i]["M"]
                elif cle[2]==i:
                    accz+=-force_newton_dict_z[cle]/univers[i]["M"]        
            accz_dict_z[i]=accz


        #obj1["accx"] = obj1["Nx"]/obj1["M"] #je calcule l'accélération de la balle avec la force calculée juste avant
        #obj1["accy"] = obj1["Ny"]/obj1["M"] #je calcule l'accélération de la balle avec la force calculée juste avant
        #obj1["accz"] = obj1["Nz"]/obj1["M"] #je calcule l'accélération de la balle avec la force calculée juste avant

        #obj2["accx"] = obj2["Nx"]/obj2["M"] #je calcule l'accélération de la balle avec la force calculée juste avant
        #obj2["accy"] = obj2["Ny"]/obj2["M"] #je calcule l'accélération de la balle avec la force calculée juste avant
        #obj2["accz"] = obj2["Nz"]/obj2["M"]

        """
        pas de temps = temps que je veux qu'il s'écoule entre chaque calcul
        pas de temps élevé = simulation plus "grossière", moins précise, et parfois cahotique
        pas de temps ->0 = simulation plus précise, mais aussi plus lourde à calculer 
        """

        pas_de_temps=3600

        """
        ensuite, je calcule le reste des données, pour pouvoir déterminer les coordonnées,
        le fonctionnement est différent d'avant, maintenant je n'injecte rien dans le dictionnaire univers
        tous les résultats d'un equation pour chaque objet sont stockés dans le meme dico
        univers[n]  ["type_de_donnée"]=type_de_donnée_dict[n]
        """

        vitx_dict_x={}
        for i in range(len(univers)):
            vitx_dict_x[i]=univers[i]["vitx"]+univers[i]["accx"]*pas_de_temps


        vity_dict_y={}
        for i in range(len(univers)):
            vity_dict_y[i]=univers[i]["vity"]+univers[i]["accy"]*pas_de_temps



        vitz_dict_z={}
        for i in range(len(univers)):
            vitz_dict_z[i]=univers[i]["vitz"]+univers[i]["accz"]*pas_de_temps

        #obj1["vitx"]+=obj1["accx"]*pas_de_temps #je met à jour la vitesse de l'objet
        #obj1["vity"]+=obj1["accy"]*pas_de_temps #je met à jour la vitesse de l'objet
        #obj1["vitz"]+=obj1["accz"]*pas_de_temps #je met à jour la vitesse de l'objet

        #obj2["vitx"]+=obj2["accx"]*pas_de_temps #je met à jour la vitesse de l'objet
        #obj2["vity"]+=obj2["accy"]*pas_de_temps #je met à jour la vitesse de l'objet
        #obj2["vitz"]+=obj2["accz"]*pas_de_temps #je met à jour la vitesse de l'objet



        #obj1_pos_post_calc={"x":obj1["x"], "y":obj1["y"], "z":obj1["z"]}#je sauvegarde les position des objets avant leur modification comme ça le calcul n'est pas influencé par quel position est changée en premier
        #obj2_pos_post_calc={"x":obj2["x"], "y":obj2["y"], "z":obj2["z"]}

        """
        je calcule maintenant les coordonnées
        """


        cord_x_dict={}
        for i in range(len(univers)):
            cord_x_dict[i]=univers[i]["x"]+vitx_dict_x[i]*pas_de_temps


        cord_y_dict={}
        for i in range(len(univers)):
            cord_y_dict[i]=univers[i]["y"]+vity_dict_y[i]*pas_de_temps



        cord_z_dict={}
        for i in range(len(univers)):
            cord_z_dict[i]=univers[i]["z"]+vitz_dict_z[i]*pas_de_temps




        #obj1["x"] += obj1["vitx"]*pas_de_temps #je met à jour sa coordonnée en aplliquant la vitesse en m/s
        #obj1["y"] += obj1["vity"]*pas_de_temps #je met à jour sa coordonnée en aplliquant la vitesse en m/s
        #obj1["z"] += obj1["vitz"]*pas_de_temps #je met à jour sa coordonnée en aplliquant la vitesse en m/s

        #obj2["x"] += obj2["vitx"]*pas_de_temps#je met à jour sa coordonnée en aplliquant la vitesse en m/s
        #obj2["y"] += obj2["vity"]*pas_de_temps#je met à jour sa coordonnée en aplliquant la vitesse en m/s
        #obj2["z"] += obj2["vitz"]*pas_de_temps #je met à jour sa coordonnée en aplliquant la vitesse en m/s


        """
        ok maintenant, je réinjecte toutes les nouvelles données dans le dictionnaire univers
        """

        for i in range(len(univers)):
            univers[i]={"x":cord_x_dict[i],
                        "y":cord_y_dict[i],
                        "z":cord_z_dict[i],
                        "accx":accx_dict_x[i],
                        "accy":accy_dict_y[i],
                        "accz":accz_dict_z[i],
                        "vitx":vitx_dict_x[i],
                        "vity":vity_dict_y[i],
                        "vitz":vitz_dict_z[i], 
                        "M":univers[i]["M"],
                        "R_o":univers[i]["R_o"]
                        }

        #time.sleep(0.02) #j'attens le pas de temps pour avoir une simulation à 1sec simulée = 1sec IRL
        dessiner_scene(univers) #je redessine la balle avec sa coordonnée mise à jour
        #print("apres calculs : ", univers) #debug, vérifier que les données sont cohérentes
    




# caca code écrit par chat gpt ( en gros c'est l'affichage de la balle avec pygame ) flemme de le faire moi meme + c pas l'ex

import numpy
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons
from collections import deque

plt.style.use("dark_background")
fig = plt.figure(figsize=(10, 8))
# la 3D prend 75% de la largeur à droite, on garde de la place à gauche pour le panneau de boutons
ax = fig.add_axes([0.22, 0.05, 0.75, 0.9], projection='3d')
plt.ion()
plt.show()

TAILLE_TRAINEE = 60  # nombre de positions passées gardées en mémoire par objet, pour dessiner sa trajectoire


def dessiner_scene(univers):
    n = len(univers)

    # init une seule fois : mémoire des trainées + panneau de boutons "verrouiller sur"
    if not hasattr(dessiner_scene, "trainees"):
        dessiner_scene.trainees = [deque(maxlen=TAILLE_TRAINEE) for _ in range(n)]
        dessiner_scene.locked_index = None  # None = vue libre, sinon indice de l'objet suivi

        # "nom" est optionnel dans le JSON : si tu en mets un, il remplace "Objet i" partout (boutons + titre)
        etiquettes = ["Vue libre"] + [univers[i].get("nom", f"Objet {i}") for i in range(n)]

        radio_ax = fig.add_axes([0.02, 0.3, 0.16, 0.4])
        radio_ax.set_facecolor("#111111")
        dessiner_scene.radio = RadioButtons(radio_ax, etiquettes, active=0, activecolor="lightskyblue")
        for lbl in dessiner_scene.radio.labels:
            lbl.set_color("white")
            lbl.set_fontsize(9)

        def _on_select(etiquette):
            dessiner_scene.locked_index = None if etiquette == "Vue libre" else etiquettes.index(etiquette) - 1

        dessiner_scene.radio.on_clicked(_on_select)

    xs = numpy.array([obj["x"] for obj in univers], dtype=float)
    ys = numpy.array([obj["y"] for obj in univers], dtype=float)
    zs = numpy.array([obj["z"] for obj in univers], dtype=float)
    rayons = numpy.array([float(obj.get("R_o", 1)) for obj in univers])

    for i in range(n):
        dessiner_scene.trainees[i].append((xs[i], ys[i], zs[i]))

    rmax = rayons.max() if rayons.max() > 0 else 1
    tailles = 30 * numpy.sqrt(rayons / rmax) + 5
    couleurs = plt.cm.plasma(numpy.linspace(0, 1, max(n, 1)))

    ax.cla()

    # panneaux + arêtes de la boîte, tout transparent : c'était les arêtes (pas la grille) qui
    # restaient visibles malgré grid(False), d'où l'effet "cage" en fond
    for axe in (ax.xaxis, ax.yaxis, ax.zaxis):
        axe.pane.set_facecolor((0, 0, 0, 0))
        axe.pane.set_edgecolor((0, 0, 0, 0))
    ax.grid(False)

    # cadrage : vue globale centrée sur l'origine, ou verrouillée + zoomée sur un objet précis
    i_lock = dessiner_scene.locked_index
    if i_lock is not None and n > 1:
        centre = numpy.array([xs[i_lock], ys[i_lock], zs[i_lock]])
        autres = numpy.delete(numpy.stack([xs, ys, zs], axis=1), i_lock, axis=0)
        dist_voisin = numpy.min(numpy.linalg.norm(autres - centre, axis=1))
        # zoom adaptatif : plus l'objet le plus proche est loin, plus on élargit le cadre
        etendue = max(dist_voisin * 2.5, rayons[i_lock] * 50)
        cx, cy, cz = centre
    else:
        etendue = max(numpy.max(numpy.abs(xs)), numpy.max(numpy.abs(ys)), numpy.max(numpy.abs(zs)), 1) * 1.15
        cx, cy, cz = 0.0, 0.0, 0.0

    ax.set_xlim(cx - etendue, cx + etendue)
    ax.set_ylim(cy - etendue, cy + etendue)
    ax.set_zlim(cz - etendue, cz + etendue)
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.set_zlabel("z (m)")

    for i in range(n):
        if len(dessiner_scene.trainees[i]) > 1:
            tx, ty, tz = zip(*dessiner_scene.trainees[i])
            ax.plot(tx, ty, tz, color=couleurs[i], alpha=0.4, linewidth=1)

    # halo lumineux discret derrière chaque point, pour casser l'effet "point plat"
    ax.scatter(xs, ys, zs, c=couleurs, s=tailles * 4, alpha=0.15, linewidths=0)
    ax.scatter(xs, ys, zs, c=couleurs, s=tailles, edgecolors="white", linewidths=0.3)

    # anneau autour de l'objet verrouillé, pour le repérer d'un coup d'œil même de près
    if i_lock is not None:
        ax.scatter([xs[i_lock]], [ys[i_lock]], [zs[i_lock]],
                   s=tailles[i_lock] * 2.5, facecolors="none", edgecolors="lightskyblue", linewidths=1.5)

    dessiner_scene.frame = getattr(dessiner_scene, "frame", 0) + 1
    cible = "vue libre" if i_lock is None else univers[i_lock].get("nom", f"objet {i_lock}")
    ax.set_title(f"étape {dessiner_scene.frame} — {cible}")

    plt.pause(0.0001)

gravité_sim(univers)