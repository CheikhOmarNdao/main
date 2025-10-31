# # -*- coding: utf-8 -*-
import pygame
import random

from catalogue import charger_catalogue, construire_pool
from inventaire import Inventaire
from manoir import Manoir
from affich_graph import Vue
from controle import Controleur
from effets import appliquer_effet, Contexte

# --- Initialisation Pygame ---
pygame.init()
TAILLE_CASE = 80
LIGNES, COLONNES = 5, 9
LARGEUR = COLONNES * TAILLE_CASE
HAUTEUR = LIGNES * TAILLE_CASE + 60
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Exploration du Manoir")

# --- Chargement du catalogue ---
catalogue = charger_catalogue("catalogue.json")
pool = construire_pool(catalogue, multiplicateur=2)
rng = random.Random()

# --- Création des objets principaux ---
inventaire = Inventaire()
manoir = Manoir(lignes=LIGNES, colonnes=COLONNES, pool=pool, rng=rng, inventaire=inventaire)
vue = Vue(ecran, manoir, manoir.joueur, inventaire)
controleur = Controleur(manoir.joueur, inventaire, manoir)

# --- Boucle principale ---
clock = pygame.time.Clock()
etat_menu = False
running = True

while running:
    actions = controleur.handle_events()
    if actions == "quitter":
        break

    if actions["tourner"]:
        vue.set_direction(actions["tourner"])

    if actions["move"]:
        vue.set_direction(actions["move"])
        manoir.deplacer(manoir.joueur, actions["move"])

        # Détection de victoire
        if manoir.est_victoire():
            vue.afficher_fin("Bravo ! Vous avez atteint l'Antechamber !", gagne=True)
            break

    if actions["ouvrir"]:
        manoir.ouvrir(manoir.joueur, vue.direction)
        if manoir.options_courantes:
            etat_menu = True
            vue.afficher_menu_choix(manoir.options_courantes)

    if actions["reroll"] and etat_menu:
        manoir.options_courantes = manoir.rng.sample(pool, 3)
        vue.afficher_menu_choix(manoir.options_courantes)

    if actions["choix_index"] is not None and etat_menu:
        i = actions["choix_index"]
        if 0 <= i < len(manoir.options_courantes):
            piece = manoir.options_courantes[i]
            if inventaire.depenser_gemmes(piece.get("cout_gemmes", 0)):
                if manoir.poser_devant(manoir.joueur, vue.direction, piece):
                    effet = appliquer_effet(piece, Contexte(inventaire, manoir))
                    print("Effet appliqué :", effet)
        etat_menu = False

    if not etat_menu:
        vue.render()

    clock.tick(30)

pygame.quit()
