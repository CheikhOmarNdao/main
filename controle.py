# -*- coding: utf-8 -*-
import pygame

class Controleur:
    def __init__(self, joueur, inventaire, manoir):
        self.joueur = joueur
        self.inventaire = inventaire
        self.manoir = manoir

    def handle_events(self):
        actions = {"move": None, "orient": None, "ouvrir": False, "reroll": False, "choix_index": None}
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quitter"
            if event.type == pygame.KEYDOWN:
                k = event.key
                if k == pygame.K_z: actions["move"] = "haut"
                elif k == pygame.K_s: actions["move"] = "bas"
                elif k == pygame.K_q: actions["move"] = "gauche"
                elif k == pygame.K_d: actions["move"] = "droite"
                elif k == pygame.K_UP: actions["orient"] = "haut"
                elif k == pygame.K_DOWN: actions["orient"] = "bas"
                elif k == pygame.K_LEFT: actions["orient"] = "gauche"
                elif k == pygame.K_RIGHT: actions["orient"] = "droite"
                elif k == pygame.K_SPACE: actions["ouvrir"] = True
                elif k == pygame.K_r: actions["reroll"] = True
                elif k in (pygame.K_1, pygame.K_KP1): actions["choix_index"] = 0
                elif k in (pygame.K_2, pygame.K_KP2): actions["choix_index"] = 1
                elif k in (pygame.K_3, pygame.K_KP3): actions["choix_index"] = 2
                elif k == pygame.K_RETURN: actions["choix_index"] = 0
                elif k == pygame.K_ESCAPE: return "quitter"
        return actions
