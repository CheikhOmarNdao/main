# -*- coding: utf-8 -*-
import pygame

class Controleur:
    """Gère les entrées clavier du joueur."""

    def __init__(self, joueur, inventaire, manoir):
        self.joueur = joueur
        self.inventaire = inventaire
        self.manoir = manoir

    def handle_events(self):
        actions = {
            "move": None,         # "haut"/"bas"/"gauche"/"droite" (ZQSD)
            "tourner": None,      # idem, mais NE BOUGE PAS (flèches)
            "ouvrir": False,      # SPACE
            "reroll": False,      # R
            "choix_index": None,  # 0/1/2 via 1/2/3/Enter
        }

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quitter"

            if event.type == pygame.KEYDOWN:
                # Déplacements (ZQSD)
                if event.key == pygame.K_z:
                    actions["move"] = "haut"
                elif event.key == pygame.K_s:
                    actions["move"] = "bas"
                elif event.key == pygame.K_q:
                    actions["move"] = "gauche"
                elif event.key == pygame.K_d:
                    actions["move"] = "droite"

                # Tourner (flèches) — MAJ direction sans se déplacer
                elif event.key == pygame.K_UP:
                    actions["tourner"] = "haut"
                elif event.key == pygame.K_DOWN:
                    actions["tourner"] = "bas"
                elif event.key == pygame.K_LEFT:
                    actions["tourner"] = "gauche"
                elif event.key == pygame.K_RIGHT:
                    actions["tourner"] = "droite"

                # Ouvrir / Reroll
                elif event.key == pygame.K_SPACE:
                    actions["ouvrir"] = True
                elif event.key == pygame.K_r:
                    actions["reroll"] = True

                # Sélection du menu (1/2/3 + Enter = 1)
                elif event.key in (pygame.K_1, pygame.K_KP1):
                    actions["choix_index"] = 0
                elif event.key in (pygame.K_2, pygame.K_KP2):
                    actions["choix_index"] = 1
                elif event.key in (pygame.K_3, pygame.K_KP3):
                    actions["choix_index"] = 2
                elif event.key == pygame.K_RETURN:
                    actions["choix_index"] = 0

                # Quitter
                elif event.key == pygame.K_ESCAPE:
                    return "quitter"

        return actions
