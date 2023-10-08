import numpy as np
import matplotlib.pyplot as plt 
import pygame as py 

py.init()  # Ajout de pygame.init()

largeur, hauteur = 1920,1080
WIN = py.display.set_mode((largeur, hauteur))
py.display.set_caption("Simulation planète")

# Masse des planètes

Msol = 1.989e30 # Masse du soleil
Mmer = 3.28e23 # Masse de mercure
Mven = 4.86e24 # Masse de vénus
Mter = 5.97e24 # Masse de la terre
Mmar = 6.41e23 # Masse de mars
Mjup = 1.89e27 # Masse de jupitère
Msat = 5.68e26 # Masse de saturne
Mura = 8.68e25 # Masse d'uranus
Mnep = 1.02e26 # Masse de neptune

Rsol = 696340e3
Rmer = 2439e3
Rven = 6051e3
Rter = 6371e3
Rmar = 3389e3
Rjup = 69911e3
Rsat = 58232e3
Rura = 25362e3
Rnep = 24622e3

#Création des couleurs des planètes sur l'interface pygame avec la methode RVB

gris = (128,128,128)
bleu_ciel = (135,206,235)
jaune_pale = (87,85,41)
orange = (255,69,0)
jaunatre = (255,200,0)
rouge = (255,0,0)
bleu = (0,255,255)
jaune = (255,255,0)
jaune_fonce = (255,255,0)  # Changement de jaune en jaune_fonce
bleu_fonce = (0,0,150),

LM = [Msol,Mmer,Mven,Mter,Mmar,Mjup,Msat,Mura,Mnep] # Liste des masses
LR = [Rsol,Rmer,Rven,Rter,Rmar,Rjup,Rsat,Rura,Rnep] # liste des rayons
LN = ["soleil","mercure","vénus","terre","mars","jupiter","saturne","uranus","neptune"] # Liste des noms
information = {"Nom":LN,"Masse":LM,"Rayon":LR} # Dictionnaire contenant des information sur les planètes

class Cplanete:
    G = 6.67428e-11 # Constante gravitationelle
    UA = 149.6e9 # Unitée astronomique
    scale = 100/ UA # 22pixel =
    pas_temp = 3600*24
    
    def __init__(self, x, y, rayon, couleur, masse, nom):
        self.x = x
        self.y = y
        self.couleur = couleur
        self.rayon = rayon
        self.masse = masse
        self.nom = nom  # Ajout de l'attribut nom

        self.orbite = []
        self.sol = False

        self.vitx = 0
        self.vity = 0
    
    def draw(self, win):
        x = self.x * self.scale + largeur / 2
        y = self.y * self.scale + hauteur / 2
        py.draw.circle(win, self.couleur, (x, y), self.rayon)

        # Afficher le nom de la planète sous l'image avec une taille de police plus petite
        font = py.font.Font(None, 18)  # Modifiez la taille de la police ici (par exemple, 18)
        text = font.render(self.nom, True, (255, 255, 255))  # Créer un objet de texte avec le nom
        text_rect = text.get_rect()
        text_rect.center = (x, y + self.rayon + 20)  # Positionner le texte sous l'image
        win.blit(text, text_rect)  # Afficher le texte sur la fenêtre
    
    def attraction(self,autre):
        distance_x = autre.x - self.x
        distance_y = autre.y - self.y
        distance = np.sqrt(distance_x**2 + distance_y**2)    

        force = self.G * self.masse * autre.masse / distance**2
        theta = np.arctan2(distance_x , distance_y)
        force_x = np.cos(theta)* force
        force_y = np.sin(theta)* force
        return force_x,force_y                             
    
    def position(self,planetes):
        tot_force_x = tot_force_y = 0
        for planete in planetes:
            if self == planete:
                continue
            fx,fy = self.attraction(planete)
            tot_force_x -= fx
            tot_force_y += fy
       
        self.vitx = tot_force_x / self.masse * self.pas_temp
        self.vity = tot_force_y / self.masse * self.pas_temp
        
        self.x += self.vitx * self.pas_temp
        self.y += self.vity * self.pas_temp
        self.orbite.append((self.x , self.y))

def fenetre():
    run = True
    heure = py.time.Clock()
    
    sol = Cplanete(0,0,4,jaune,Msol,"Soleil")
    
    ter = Cplanete(149.6e9,0,1,bleu,Mter,"Terre")
    
    mar = Cplanete(1.5*149.6e9 ,0,1,rouge,Mmar,"Mars")
    
    ven = Cplanete(0.72*149.6e9 ,0,1,jaunatre,Mven,"Venus")
   
    jup = Cplanete(5.2*149.6e9 ,0,2,orange,Mjup,"Jupiter")
    
    sat = Cplanete(9.5*149.6e9 ,0,2,jaune_pale,Msat,"Saturne")
   
    ura = Cplanete(19.2*149.6e9 ,0,2,bleu_ciel,Mura,"Uranus")
    
    mer = Cplanete(0.39*149.6e9 ,0,1 ,gris,Mmer,"Mercure")
   
    nep = Cplanete(30*149.6e9 ,0,2,bleu_fonce,Mnep,"Neptune")
    
    sol.sol = True
    planetes = [sol,ter,mar,ven,jup,sat,ura,mer,nep]
    f=0
    while run:
        WIN.fill((0,0,0))
        heure.tick(10000)
        
        for even in py.event.get():
            if even.type == py.QUIT:
                run = False
        for planete in planetes :
            planete.position(planetes)
        if (f==0) :
            for planete in planetes :
                planete.draw(WIN)
            py.display.update()
            f=70
        else :
            f=f-1
    py.quit()

fenetre()
