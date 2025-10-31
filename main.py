# 


# -*- coding: utf-8 -*-
import pygame
import random

from catalogue import charger_catalogue, construire_pool
from inventaire import Inventaire
from manoir import Manoir
from affich_graph import Vue
from controle import Controleur
from effets import appliquer_effet, Contexte
from tirages import tirer_trois

# --- Initialisation Pygame ---
pygame.init()
TAILLE_CASE = 80
LIGNES, COLONNES = 5, 9
LARGEUR = COLONNES * TAILLE_CASE
HAUTEUR = LIGNES * TAILLE_CASE + 60
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Blue Prince - Projet POO")

# --- Chargement du catalogue et création du pool ---
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
        if manoir.peut_deplacer(manoir.joueur, actions["move"]):
            manoir.deplacer(manoir.joueur, actions["move"])
            inventaire.pas -= 1
            print(f"🚶 Déplacement vers {actions['move']} | Pas restants : {inventaire.pas}")

            if inventaire.pas <= 0:
                vue.afficher_fin("Vous avez épuisé vos pas !", perdu=True)
                break

            if manoir.est_victoire():
                vue.afficher_fin("Bravo ! Vous avez atteint l'Antechamber !", gagne=True)
                break

    if actions["ouvrir"]:
        if manoir.peut_ouvrir(manoir.joueur, vue.direction):
            manoir.options_courantes = tirer_trois(pool, rng)
            print("🔮 Tirage effectué :", [p["type"] for p in manoir.options_courantes])
            if manoir.options_courantes:
                etat_menu = True
                vue.afficher_menu_choix(manoir.options_courantes)

    if actions["reroll"] and etat_menu:
        if inventaire.des > 0:
            inventaire.des -= 1
            manoir.options_courantes = tirer_trois(pool, rng)
            print("🎲 Reroll effectué :", [p["type"] for p in manoir.options_courantes])
            vue.afficher_menu_choix(manoir.options_courantes)

    if actions["choix_index"] is not None and etat_menu:
        i = actions["choix_index"]
        if 0 <= i < len(manoir.options_courantes):
            piece = manoir.options_courantes[i]
            cout = piece.get("cout_gemmes", 0)

            if inventaire.gemmes >= cout:
                inventaire.gemmes -= cout
                if manoir.poser_devant(manoir.joueur, vue.direction, piece):
                    print(f"✅ Pièce posée : {piece['type']} | Gemmes restantes : {inventaire.gemmes}")
                    effet = appliquer_effet(piece, Contexte(inventaire, manoir))
                    if effet:
                        print("✨ Effet appliqué :", effet)
            else:
                print(f"❌ Pas assez de gemmes pour {piece['type']} (coût : {cout})")

        etat_menu = False

    if not etat_menu:
        vue.render()

    clock.tick(30)

pygame.quit()
