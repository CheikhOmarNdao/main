# # -*- coding: utf-8 -*-
# """
# Created on Tue Oct 28 17:17:40 2025

# @author: 7KAKSACOD
# """

# import pygame
# import sys
# import random

# # ================================================================

# # Classes du jeu (simplifiées pour intégration avec pygame)

# # ================================================================

# class Piece:
#     def __init__(self, nom, couleur):
#         self.nom = nom
#         self.couleur = couleur

# class Joueur:
#         def __init__(self, x, y):
#             self.x = x
#             self.y = y
#             self.pas = 70

# class Manoir:
#         def __init__(self, lignes=5, colonnes=9):
#             self.lignes = lignes
#             self.colonnes = colonnes
#             self.grille = [[None for _ in range(colonnes)] for _ in range(lignes)]
#             self.initialiser_manoir()
            
#         def initialiser_manoir(self):
#             couleurs = ["blue", "orange", "purple", "green", "yellow", "red"]
#             for i in range(self.lignes):
#                 for j in range(self.colonnes):
#                     self.grille[i][j] = Piece("Salle", random.choice(couleurs))


# # ================================================================

# # Classe : Jeu avec pygame

# # ================================================================

# class JeuPygame:
#         def __init__(self):
#             pygame.init()
#             self.largeur_case = 80
#             self.hauteur_case = 80
#             self.manoir = Manoir()
#             self.joueur = Joueur(4, 4)
#             self.ecran = pygame.display.set_mode(
#             (self.manoir.colonnes * self.largeur_case, self.manoir.lignes * self.hauteur_case + 60)
#             )
#             pygame.display.set_caption("Blue Prince Simplifié")
#             self.police = pygame.font.SysFont("Arial", 20)
#             self.couleurs = {
#             "blue": (80, 150, 255),
#             "orange": (255, 160, 70),
#             "purple": (180, 100, 255),
#             "green": (80, 200, 120),
#             "yellow": (250, 230, 100),
#             "red": (230, 80, 80),
#             "gris": (200, 200, 200),
#             }

#             def dessiner_grille(self):
#                 for i in range(self.manoir.lignes):
#                     for j in range(self.manoir.colonnes):
#                         piece = self.manoir.grille[i][j]
#                         couleur = self.couleurs[piece.couleur]
#                         rect = pygame.Rect(j * self.largeur_case, i * self.hauteur_case, self.largeur_case, self.hauteur_case)
#                         pygame.draw.rect(self.ecran, couleur, rect)
#                         pygame.draw.rect(self.ecran, (0, 0, 0), rect, 2)
            
#                 # Dessiner le joueur
#                 joueur_rect = pygame.Rect(
#                     self.joueur.y * self.largeur_case + 10,
#                     self.joueur.x * self.hauteur_case + 10,
#                     self.largeur_case - 20,
#                     self.hauteur_case - 20,
#                 )
#                 pygame.draw.rect(self.ecran, (0, 0, 255), joueur_rect)
            
#             def dessiner_interface(self):
#                 barre = pygame.Rect(0, self.manoir.lignes * self.hauteur_case, self.manoir.colonnes * self.largeur_case, 60)
#                 pygame.draw.rect(self.ecran, self.couleurs["gris"], barre)
#                 texte = self.police.render(f"Pas restants : {self.joueur.pas}", True, (0, 0, 0))
#                 self.ecran.blit(texte, (10, self.manoir.lignes * self.hauteur_case + 20))
            
#             def deplacer_joueur(self, direction):
#                 if direction == "z" and self.joueur.x > 0:
#                     self.joueur.x -= 1
#                 elif direction == "s" and self.joueur.x < self.manoir.lignes - 1:
#                     self.joueur.x += 1
#                 elif direction == "q" and self.joueur.y > 0:
#                     self.joueur.y -= 1
#                 elif direction == "d" and self.joueur.y < self.manoir.colonnes - 1:
#                     self.joueur.y += 1
#                 self.joueur.pas -= 1
            
#             def boucle_principale(self):
#                 clock = pygame.time.Clock()
#                 en_cours = True
#                 while en_cours:
#                     for event in pygame.event.get():
#                         if event.type == pygame.QUIT:
#                             en_cours = False
#                         if event.type == pygame.KEYDOWN:
#                             if event.key == pygame.K_z:
#                                 self.deplacer_joueur("z")
#                             elif event.key == pygame.K_s:
#                                 self.deplacer_joueur("s")
#                             elif event.key == pygame.K_q:
#                                 self.deplacer_joueur("q")
#                             elif event.key == pygame.K_d:
#                                 self.deplacer_joueur("d")
            
#                     self.ecran.fill((255, 255, 255))
#                     self.dessiner_grille()
#                     self.dessiner_interface()
#                     pygame.display.flip()
            
#                     if self.joueur.pas <= 0:
#                         en_cours = False
#                     clock.tick(30)
            
# pygame.quit()
# sys.exit()


# # ================================================================

# # Lancement du jeu

# # ================================================================
# if __name__ == "__main__":
#     jeu = JeuPygame()
#     jeu.boucle_principale()
import pygame
import sys
import random

class Piece:
    def __init__(self, nom, couleur):
        self.nom = nom
        self.couleur = couleur

class Joueur:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pas = 70

class Manoir:
    def __init__(self, lignes=5, colonnes=9):
        self.lignes = lignes
        self.colonnes = colonnes
        self.grille = [[None for _ in range(colonnes)] for _ in range(lignes)]
        self.initialiser_manoir()
    
    def initialiser_manoir(self):
        couleurs = ["blue", "orange", "purple", "green", "yellow", "red"]
        for i in range(self.lignes):
            for j in range(self.colonnes):
                self.grille[i][j] = Piece("Salle", random.choice(couleurs))

class JeuPygame:
    def __init__(self):
        pygame.init()
        self.largeur_case = 80
        self.hauteur_case = 80
        self.manoir = Manoir()
        self.joueur = Joueur(4, 4)
        self.ecran = pygame.display.set_mode(
            (self.manoir.colonnes * self.largeur_case, self.manoir.lignes * self.hauteur_case + 60)
        )
        pygame.display.set_caption("Blue Prince Simplifié")
        self.police = pygame.font.SysFont("Arial", 20)
        self.couleurs = {
            "blue": (80, 150, 255),
            "orange": (255, 160, 70),
            "purple": (180, 100, 255),
            "green": (80, 200, 120),
            "yellow": (250, 230, 100),
            "red": (230, 80, 80),
            "gris": (200, 200, 200),
        }

    def dessiner_grille(self):
        for i in range(self.manoir.lignes):
            for j in range(self.manoir.colonnes):
                piece = self.manoir.grille[i][j]
                couleur = self.couleurs[piece.couleur]
                rect = pygame.Rect(j * self.largeur_case, i * self.hauteur_case, self.largeur_case, self.hauteur_case)
                pygame.draw.rect(self.ecran, couleur, rect)
                pygame.draw.rect(self.ecran, (0, 0, 0), rect, 2)

        joueur_rect = pygame.Rect(
            self.joueur.y * self.largeur_case + 10,
            self.joueur.x * self.hauteur_case + 10,
            self.largeur_case - 20,
            self.hauteur_case - 20,
        )
        pygame.draw.rect(self.ecran, (0, 0, 255), joueur_rect)

    def dessiner_interface(self):
        barre = pygame.Rect(0, self.manoir.lignes * self.hauteur_case, self.manoir.colonnes * self.largeur_case, 60)
        pygame.draw.rect(self.ecran, self.couleurs["gris"], barre)
        texte = self.police.render(f"Pas restants : {self.joueur.pas}", True, (0, 0, 0))
        self.ecran.blit(texte, (10, self.manoir.lignes * self.hauteur_case + 20))

    def deplacer_joueur(self, direction):
        if direction == "z" and self.joueur.x > 0:
            self.joueur.x -= 1
        elif direction == "s" and self.joueur.x < self.manoir.lignes - 1:
            self.joueur.x += 1
        elif direction == "q" and self.joueur.y > 0:
            self.joueur.y -= 1
        elif direction == "d" and self.joueur.y < self.manoir.colonnes - 1:
            self.joueur.y += 1
        self.joueur.pas -= 1

    def boucle_principale(self):
        clock = pygame.time.Clock()
        en_cours = True
        while en_cours:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    en_cours = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        self.deplacer_joueur("z")
                    elif event.key == pygame.K_s:
                        self.deplacer_joueur("s")
                    elif event.key == pygame.K_q:
                        self.deplacer_joueur("q")
                    elif event.key == pygame.K_d:
                        self.deplacer_joueur("d")

            self.ecran.fill((255, 255, 255))
            self.dessiner_grille()
            self.dessiner_interface()
            pygame.display.flip()

            if self.joueur.pas <= 0:
                en_cours = False
            clock.tick(30)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    jeu = JeuPygame()
    jeu.boucle_principale()
