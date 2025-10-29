# -*- coding: utf-8 -*-
"""
Created on Wed Oct 29 05:03:28 2025

@author: 7KAKSACOD
"""

import pygame
"""Gère les entrées clavier du joueur."""
class Controleur:


    def __init__(self, joueur, inventaire, manoir):
        self.joueur = joueur
        self.inventaire = inventaire
        self.manoir = manoir
    
    def handle_events(self):
        actions = {"move": None, "ouvrir": False, "choisir": False, "reroll": False}
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quitter"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z: actions["move"] = "haut"
                elif event.key == pygame.K_s: actions["move"] = "bas"
                elif event.key == pygame.K_q: actions["move"] = "gauche"
                elif event.key == pygame.K_d: actions["move"] = "droite"
                elif event.key == pygame.K_SPACE: actions["ouvrir"] = True
                elif event.key == pygame.K_RETURN: actions["choisir"] = True
                elif event.key == pygame.K_r: actions["reroll"] = True
        return actions

