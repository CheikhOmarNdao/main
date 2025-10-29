# # # -*- coding: utf-8 -*-
# # """
# # Created on Tue Oct 28 16:43:36 2025

# # @author: 7KAKSACOD
# # """

# import random

# # ================================================================

# # Classe : Objet de base

# # ================================================================
# """Classe de base pour tous les objets du jeu."""
# class Objet:
              
#       def __init__(self, nom, description):
#             self.nom = nom
#             self.description = description
       
#       def utiliser(self, joueur):               "Méthode à surcharger selon le type d'objet."
   
#       pass


# # ================================================================

# # Classes : Objets consommables et permanents

# # ================================================================
# "Objets à usage unique (ex : nourriture, gemmes, clés, dés)."
# class ObjetConsommable(Objet):
      
#       def __init__(self, nom, effet, description=""):
#             super().__init__(nom, description)
#             self.effet = effet  # fonction ou lambda
  

# def utiliser(self, joueur):
#     self.effet(joueur)
#     print(f"{joueur.nom} utilise {self.nom}.")


# class ObjetPermanent(Objet):
# #Objets permanents (ex : pelle, marteau, kit de crochetage).
#     def __init__(self, nom, effet=None, description=""):
#         super().__init__(nom, description)
#         self.effet = effet

# # ================================================================

# # Classe : Inventaire du joueur

# # ================================================================

# class Inventaire:
#     def __init__(self):
#         self.pas = 70
#         self.gemmes = 2
#         self.cles = 0
#         self.des = 0
#         self.pieces = 0
#         self.objets_permanents = []
#         self.objets_conso = []


#     def ajouter_objet(self, objet):
#         if isinstance(objet, ObjetPermanent):
#             self.objets_permanents.append(objet)
#         elif isinstance(objet, ObjetConsommable):
#             self.objets_conso.append(objet)
    
#     def afficher(self):
#         print(f"Pas: {self.pas}, Gemmes: {self.gemmes}, Clés: {self.cles}, Dés: {self.des}, Pièces: {self.pieces}")
#         print("Objets permanents :", [o.nom for o in self.objets_permanents])
#         print("Objets consommables :", [o.nom for o in self.objets_conso])


# # ================================================================

# # Classe : Porte

# # ================================================================

# class Porte:
#         def __init__(self, direction, niveau=0):
#             self.direction = direction  # "haut", "bas", "gauche", "droite"
#             self.niveau = niveau        # 0 = ouverte, 1 = verrouillée, 2 = double verrou
#             self.connectee = False


#         def est_ouverte(self, joueur):
#             """Vérifie si la porte peut être ouverte par le joueur."""
#             if self.niveau == 0:
#                 return True
#             elif self.niveau == 1 and ("kit de crochetage" in [o.nom for o in joueur.inventaire.objets_permanents]):
#                 return True
#             elif joueur.inventaire.cles > 0:
#                 joueur.inventaire.cles -= 1
#                 return True
#             return False


# # # ================================================================

# # # Classe : Pièce du manoir

# # # ================================================================

# class Piece:
#         def __init__(self, nom, couleur, rarete, cout_gemmes=0, effet=None):
#             self.nom = nom
#             self.couleur = couleur
#             self.rarete = rarete  # 0 à 3
#             self.cout_gemmes = cout_gemmes
#             self.effet = effet
#             self.portes = {}      # ex: {"haut": Porte(...), "droite": Porte(...)}
#             self.objets = []
        
#         def appliquer_effet(self, joueur):
#             """Applique l'effet spécial de la pièce si défini."""
#             if self.effet:
#                 self.effet(joueur)
        
#         def ajouter_porte(self, direction, niveau=0):
#             self.portes[direction] = Porte(direction, niveau)


# # # ================================================================

# # # Classe : Pioche de salles

# # # ================================================================

# class PiocheDeSalles:
#         def __init__(self):
#             self.catalogue = []
#             self.initialiser_catalogue()

#         def initialiser_catalogue(self):
#             """Crée quelques pièces de base pour démarrer."""
#             self.catalogue = [
#                 Piece("Entrée", "bleue", 0, 0),
#                 Piece("Couloir", "orange", 0, 0),
#                 Piece("Chambre", "violette", 1, 1, lambda j: setattr(j.inventaire, "pas", j.inventaire.pas + 10)),
#                 Piece("Jardin", "verte", 2, 2),
#                 Piece("Magasin", "jaune", 2, 0),
#                 Piece("Cave", "rouge", 1, 0)
#             ]
        
#         def tirer_pieces(self, nombre=3):
#             """Tire aléatoirement un certain nombre de pièces selon leur rareté."""
#             poids = [1 / (3 ** p.rarete) for p in self.catalogue]
#             return random.choices(self.catalogue, weights=poids, k=nombre)


# # # ================================================================

# # # Classe : Joueur

# # # ================================================================

# class Joueur:
#         def __init__(self, nom):
#             self.nom = nom
#             self.position = (4, 2)  # ligne 4, colonne 2 (bas du manoir)
#             self.inventaire = Inventaire()

# # # ================================================================

# # # Classe : Manoir (grille du jeu)

# # # ================================================================

# class Manoir:
#         def __init__(self, lignes=5, colonnes=9):
#             self.lignes = lignes
#             self.colonnes = colonnes
#             self.grille = [[None for _ in range(colonnes)] for _ in range(lignes)]
#             self.pioche = PiocheDeSalles()
#             self.initialiser_manoir()
        
#         def initialiser_manoir(self):
#             """Place la pièce d'entrée en bas du manoir."""
#             entree = next(p for p in self.pioche.catalogue if p.nom == "Entrée")
#             self.grille[self.lignes - 1][self.colonnes // 2] = entree
        
#         def ajouter_piece(self, piece, x, y):
#             self.grille[x][y] = piece


# # # ================================================================

# # # Classe : Jeu principal

# # # ================================================================

# class Jeu:
#         def __init__(self):
#             self.manoir = Manoir()
#             self.joueur = Joueur("Joueur 1")
#             self.en_cours = True
        
#         def boucle_principale(self):
#             """Boucle simplifiée (sans pygame pour l’instant)."""
#             print("=== Début du jeu Blue Prince simplifié ===")
#             while self.en_cours:
#                 self.afficher_etat()
#                 action = input("Action (z/q/s/d pour bouger, x pour quitter): ").lower()
#                 if action == "x":
#                     self.en_cours = False
#                 else:
#                     self.deplacer(action)

#         def afficher_etat(self):
#             print(f"Position : {self.joueur.position}")
#             self.joueur.inventaire.afficher()
        
#         def deplacer(self, direction):
#             x, y = self.joueur.position
#             if direction == "z" and x > 0:
#                 x -= 1
#             elif direction == "s" and x < self.manoir.lignes - 1:
#                 x += 1
#             elif direction == "q" and y > 0:
#                 y -= 1
#             elif direction == "d" and y < self.manoir.colonnes - 1:
#                 y += 1
#             else:
#                 print("Déplacement impossible.")
#                 return
        
#             self.joueur.position = (x, y)
#             self.joueur.inventaire.pas -= 1
#             print(f"Déplacement vers {self.joueur.position}. Pas restants : {self.joueur.inventaire.pas}")


# # # ================================================================

# # # Lancement du jeu (console)

# # # ================================================================

# # jeu = Jeu()
# # jeu.boucle_principale()

# import os
# import pygame
# import requests

# class Vue:
#     """Classe responsable de l'affichage graphique du manoir et de l'inventaire (avec images)."""

#     def __init__(self, ecran, manoir, joueur, inventaire):
#         self.ecran = ecran
#         self.manoir = manoir
#         self.joueur = joueur
#         self.inventaire = inventaire
#         self.taille_case = 80
#         self.police = pygame.font.SysFont("Arial", 20)
#         self.assets_dir = "assets"
#         os.makedirs(self.assets_dir, exist_ok=True)
#         self.images_pieces = {}
#         self.telecharger_images()
#         self.couleur_hud = (220, 220, 220)

#     def telecharger_images(self):
#         """Télécharge les images des pièces si elles n'existent pas encore."""
#         # ⚠️ Exemple : tu peux compléter avec les liens réels depuis le wiki Blue Prince
#         liens = {
#             "bleue": "https://static.wikia.nocookie.net/blue-prince/images/0/0a/BlueRoom.png",
#             "orange": "https://static.wikia.nocookie.net/blue-prince/images/2/23/CorridorRoom.png",
#             "verte": "https://static.wikia.nocookie.net/blue-prince/images/f/f7/GardenRoom.png",
#             "violette": "https://static.wikia.nocookie.net/blue-prince/images/9/90/Bedroom.png",
#             "jaune": "https://static.wikia.nocookie.net/blue-prince/images/b/b2/ShopRoom.png",
#             "rouge": "https://static.wikia.nocookie.net/blue-prince/images/5/59/TrapRoom.png",
#         }

#         for nom, url in liens.items():
#             chemin = os.path.join(self.assets_dir, f"{nom}.png")
#             if not os.path.exists(chemin):
#                 try:
#                     print(f"Téléchargement de {nom}...")
#                     r = requests.get(url, timeout=10)
#                     if r.status_code == 200:
#                         with open(chemin, "wb") as f:
#                             f.write(r.content)
#                 except Exception as e:
#                     print(f"Erreur téléchargement {nom}: {e}")
#             self.images_pieces[nom] = pygame.image.load(chemin).convert()

#     def render(self):
#         self.ecran.fill((255, 255, 255))
#         self.afficher_grille()
#         self.afficher_joueur()
#         self.afficher_hud()
#         pygame.display.flip()

#     def afficher_grille(self):
#         for i in range(self.manoir.lignes):
#             for j in range(self.manoir.colonnes):
#                 piece = self.manoir.grille[i][j]
#                 couleur = piece["couleur"]
#                 image = self.images_pieces.get(couleur)
#                 if image:
#                     image = pygame.transform.scale(image, (self.taille_case, self.taille_case))
#                     self.ecran.blit(image, (j * self.taille_case, i * self.taille_case))
#                 pygame.draw.rect(self.ecran, (0, 0, 0), (j * self.taille_case, i * self.taille_case, self.taille_case, self.taille_case), 1)

#     def afficher_joueur(self):
#         rect = pygame.Rect(
#             self.joueur["y"] * self.taille_case + 20,
#             self.joueur["x"] * self.taille_case + 20,
#             self.taille_case - 40,
#             self.taille_case - 40,
#         )
#         pygame.draw.rect(self.ecran, (0, 0, 255), rect)

#     def afficher_hud(self):
#         y_base = self.manoir.lignes * self.taille_case
#         pygame.draw.rect(self.ecran, self.couleur_hud, (0, y_base, self.manoir.colonnes * self.taille_case, 60))
#         texte = self.police.render(self.inventaire.afficher(), True, (0, 0, 0))
#         self.ecran.blit(texte, (10, y_base + 20))





# if __name__ == "__main__":
#     pygame.init()
#     manoir = Manoir()
#     joueur = {"x": 0, "y": 0}
#     inventaire = Inventaire()
#     taille_case = 80
#     largeur = manoir.colonnes * taille_case
#     hauteur = manoir.lignes * taille_case + 60
#     ecran = pygame.display.set_mode((largeur, hauteur))
#     vue = Vue(ecran, manoir, joueur, inventaire)

#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#         vue.render()
#     pygame.quit()
import os
import pygame
import random
import requests

# ================================================================
# Classe Inventaire
# ================================================================
class Inventaire:
    def __init__(self):
        self.pas = 70
        self.gemmes = 2
        self.cles = 0
        self.des = 0
        self.pieces = 0

    def afficher(self):
        return f"Pas: {self.pas} | Gemmes: {self.gemmes} | Clés: {self.cles} | Dés: {self.des} | Pièces: {self.pieces}"


# ================================================================
# Classe Manoir simplifiée
# ================================================================
class Manoir:
    def __init__(self, lignes=5, colonnes=9):
        self.lignes = lignes
        self.colonnes = colonnes
        couleurs = ["bleue", "orange", "verte", "violette", "jaune", "rouge"]
        self.grille = [[{"nom": "Salle", "couleur": random.choice(couleurs)} for _ in range(colonnes)] for _ in range(lignes)]


# ================================================================
# Classe Vue (avec gestion d’images)
# ================================================================
class Vue:
    def __init__(self, ecran, manoir, joueur, inventaire):
        self.ecran = ecran
        self.manoir = manoir
        self.joueur = joueur
        self.inventaire = inventaire
        self.taille_case = 80
        self.police = pygame.font.SysFont("Arial", 20)
        self.assets_dir = os.path.join(os.getcwd(), "assets")
        os.makedirs(self.assets_dir, exist_ok=True)
        self.couleur_hud = (230, 230, 230)
        self.couleurs_fallback = {
            "bleue": (80, 150, 255),
            "orange": (255, 160, 70),
            "verte": (80, 200, 120),
            "violette": (180, 100, 255),
            "jaune": (250, 230, 100),
            "rouge": (230, 80, 80),
        }

        self.images_pieces = self.telecharger_images()

    def telecharger_images(self):
        """Télécharge les images une fois et les charge dans pygame."""
        liens = {
            "bleue": "https://static.wikia.nocookie.net/blue-prince/images/0/0a/BlueRoom.png",
            "orange": "https://static.wikia.nocookie.net/blue-prince/images/2/23/CorridorRoom.png",
            "verte": "https://static.wikia.nocookie.net/blue-prince/images/f/f7/GardenRoom.png",
            "violette": "https://static.wikia.nocookie.net/blue-prince/images/9/90/Bedroom.png",
            "jaune": "https://static.wikia.nocookie.net/blue-prince/images/b/b2/ShopRoom.png",
            "rouge": "https://static.wikia.nocookie.net/blue-prince/images/5/59/TrapRoom.png",
        }

        images = {}
        for nom, url in liens.items():
            chemin = os.path.join(self.assets_dir, f"{nom}.png")

            # Téléchargement si absent
            if not os.path.exists(chemin):
                try:
                    print(f"Téléchargement de {nom}...")
                    r = requests.get(url, timeout=10)
                    if r.status_code == 200:
                        with open(chemin, "wb") as f:
                            f.write(r.content)
                    else:
                        print(f"Erreur {r.status_code} pour {nom}")
                except Exception as e:
                    print(f"Échec du téléchargement de {nom}: {e}")

            # Chargement dans pygame si le fichier existe
            if os.path.exists(chemin):
                try:
                    images[nom] = pygame.image.load(chemin).convert()
                except Exception as e:
                    print(f"Erreur chargement {nom}: {e}")
                    images[nom] = None
            else:
                images[nom] = None
        return images

    def render(self):
        self.ecran.fill((255, 255, 255))
        self.afficher_grille()
        self.afficher_joueur()
        self.afficher_hud()
        pygame.display.flip()

    def afficher_grille(self):
        for i in range(self.manoir.lignes):
            for j in range(self.manoir.colonnes):
                piece = self.manoir.grille[i][j]
                couleur = piece["couleur"]
                image = self.images_pieces.get(couleur)

                x, y = j * self.taille_case, i * self.taille_case
                rect = pygame.Rect(x, y, self.taille_case, self.taille_case)

                if image:
                    image_redim = pygame.transform.scale(image, (self.taille_case, self.taille_case))
                    self.ecran.blit(image_redim, (x, y))
                else:
                    pygame.draw.rect(self.ecran, self.couleurs_fallback[couleur], rect)

                pygame.draw.rect(self.ecran, (0, 0, 0), rect, 1)

    def afficher_joueur(self):
        rect = pygame.Rect(
            self.joueur["y"] * self.taille_case + 20,
            self.joueur["x"] * self.taille_case + 20,
            self.taille_case - 40,
            self.taille_case - 40,
        )
        pygame.draw.rect(self.ecran, (0, 0, 255), rect)

    def afficher_hud(self):
        y_base = self.manoir.lignes * self.taille_case
        pygame.draw.rect(
            self.ecran, self.couleur_hud,
            (0, y_base, self.manoir.colonnes * self.taille_case, 60)
        )
        texte = self.police.render(self.inventaire.afficher(), True, (0, 0, 0))
        self.ecran.blit(texte, (10, y_base + 20))


# ================================================================
# Programme principal
# ================================================================
if __name__ == "__main__":
    pygame.init()
    manoir = Manoir()
    joueur = {"x": 2, "y": 4}
    inventaire = Inventaire()
    taille_case = 80
    largeur = manoir.colonnes * taille_case
    hauteur = manoir.lignes * taille_case + 60
    ecran = pygame.display.set_mode((largeur, hauteur))
    pygame.display.set_caption("Blue Prince — avec images")

    vue = Vue(ecran, manoir, joueur, inventaire)

    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        vue.render()
        clock.tick(30)
    pygame.quit()
