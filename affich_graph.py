# -*- coding: utf-8 -*-
"""
Created on Wed Oct 29 05:24:30 2025

@author: 7KAKSACOD
"""

import pygame

class Vue:
    """Classe responsable de l'affichage graphique du manoir et de l'inventaire."""

    def __init__(self, ecran, manoir, joueur, inventaire):
        self.ecran = ecran
        self.manoir = manoir
        self.joueur = joueur
        self.inventaire = inventaire
        self.taille_case = 80
        self.police = pygame.font.SysFont("Arial", 20)
        self.couleurs = {
            "bleue": (80, 150, 255),
            "orange": (255, 160, 70),
            "verte": (80, 200, 120),
            "violette": (180, 100, 255),
            "jaune": (250, 230, 100),
            "rouge": (230, 80, 80),
            "gris": (200, 200, 200),
        }

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
                couleur = self.couleurs.get(piece["couleur"], (220, 220, 220))
                rect = pygame.Rect(j * self.taille_case, i * self.taille_case, self.taille_case, self.taille_case)
                pygame.draw.rect(self.ecran, couleur, rect)
                pygame.draw.rect(self.ecran, (0, 0, 0), rect, 2)

    def afficher_joueur(self):
        rect = pygame.Rect(
            self.joueur["y"] * self.taille_case + 10,
            self.joueur["x"] * self.taille_case + 10,
            self.taille_case - 20,
            self.taille_case - 20,
        )
        pygame.draw.rect(self.ecran, (0, 0, 255), rect)

    def afficher_hud(self):
        barre = pygame.Rect(
            0,
            self.manoir.lignes * self.taille_case,
            self.manoir.colonnes * self.taille_case,
            60
        )
        pygame.draw.rect(self.ecran, self.couleurs["gris"], barre)
        texte = self.police.render(self.inventaire.afficher(), True, (0, 0, 0))
        self.ecran.blit(texte, (10, self.manoir.lignes * self.taille_case + 20))
        
    def afficher_menu_choix(self, options):
        self.ecran.fill((240, 240, 240))
        for i, piece in enumerate(options):
            texte = self.police.render(f"{i+1}. {piece['type']}", True, (0, 0, 0))
            self.ecran.blit(texte, (50, 50 + i * 40))
        pygame.display.flip()

    def afficher_fin(self, message, perdu=False, gagne=False):
        # Détermination de la couleur de fond
        if perdu:
            couleur_fond = self.couleurs["rouge"]     # Rouge pour défaite
        elif gagne:
            couleur_fond = self.couleurs["verte"]     # Vert pour victoire
        else:
            couleur_fond = (0, 0, 0)                  # Noir par défaut

        # Remplissage de l'écran
        self.ecran.fill(couleur_fond)

        # Rendu du texte
        texte = self.police.render(message, True, (255, 255, 255))
        rect = texte.get_rect(center=(self.ecran.get_width() // 2, self.ecran.get_height() // 2))

        # Affichage du texte
        self.ecran.blit(texte, rect)
        pygame.display.flip()
        pygame.time.wait(3000)
