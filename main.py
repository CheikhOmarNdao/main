# -*- coding: utf-8 -*-
"""
Boucle principale (MVP) :
- Z/Q/S/D : déplacement (–1 pas)
- Flèches : tourner (met la direction sans bouger)
- ESPACE  : ouvrir (passe au menu de choix)
- 1/2/3/Entrée : choisir une option
- R : reroll pendant le menu (–1 dé)
"""

import random
import pygame

from affich_graph import Vue
from controle import Controleur
from inventaire import Inventaire
from manoir import Manoir
from tirages import tirer_trois
# from effets import appliquer_effet, Contexte  # si tu veux appliquer des effets à la pose

POOL = [
    {"type": "Galerie",       "couleur": "verte",    "rarete": 1, "cout_gemmes": 0},
    {"type": "Garage",        "couleur": "jaune",    "rarete": 2, "cout_gemmes": 1},
    {"type": "Observatoire",  "couleur": "violette", "rarete": 3, "cout_gemmes": 2},
    {"type": "Serre",         "couleur": "verte",    "rarete": 1, "cout_gemmes": 0},
    {"type": "Cuisine",       "couleur": "orange",   "rarete": 1, "cout_gemmes": 0},
    {"type": "Bibliotheque",  "couleur": "bleue",    "rarete": 2, "cout_gemmes": 1},
]

def main():
    pygame.init()
    pygame.display.set_caption("Blue Prince — MVP")

    rng = random.Random()
    inventaire = Inventaire(pas=75, or_=0, gemmes=2, cles=0, des=1)
    manoir = Manoir(lignes=5, colonnes=9, pool=POOL, rng=rng)
    joueur = manoir.joueur

    TCASE, H_HUD = 80, 60
    largeur = manoir.colonnes * TCASE
    hauteur = manoir.lignes * TCASE + H_HUD
    ecran = pygame.display.set_mode((largeur, hauteur))

    vue = Vue(ecran, manoir, joueur, inventaire, dossier_images="image_pieces")
    controleur = Controleur(joueur, inventaire, manoir)
    clock = pygame.time.Clock()

    etat = "jeu"                 # "jeu" / "choix"
    direction_ouverte = "droite"

    running = True
    while running:
        actions = controleur.handle_events()
        if actions == "quitter":
            break

        # ===================== ETAT CHOIX =====================
        if etat == "choix":
            vue.afficher_menu_choix(manoir.options_courantes)

            idx = actions.get("choix_index")
            if idx is not None and 0 <= idx < len(manoir.options_courantes):
                piece = manoir.options_courantes[idx]
                cout = int(piece.get("cout_gemmes", 0))
                if cout <= inventaire.gemmes and inventaire.depenser_gemmes(cout):
                    x, y = manoir._case_devant(joueur, direction_ouverte)
                    ok = manoir.poser_piece(x, y, piece)
                    print(f"[LOG] Pose {piece.get('type')} à {(x, y)} => {ok}, coût {cout} gemme(s)")
                    if ok:
                        # # Optionnel: appliquer l'effet
                        # ctx = Contexte(inventaire=inventaire, manoir=manoir)
                        # msg = appliquer_effet(piece, ctx)
                        # print("[EFFET]", msg)
                        manoir.options_courantes = []
                        etat = "jeu"
                else:
                    print("[WARN] Gemmes insuffisantes pour cette option.")

            if actions.get("reroll"):
                if inventaire.depenser_des(1):
                    manoir.options_courantes = tirer_trois(POOL, rng)
                    print("[LOG] Reroll des options (–1 dé).")
                else:
                    print("[WARN] Aucun dé disponible pour reroll.")

            clock.tick(60)
            continue  # ne pas dessiner la grille ici

        # ===================== ETAT JEU =====================
        # Tourner avec les flèches (ne bouge pas)
        if actions.get("tourner"):
            direction_ouverte = actions["tourner"]

        # Déplacement (ZQSD) — consomme 1 pas
        if actions.get("move"):
            d = actions["move"]
            if inventaire.depenser_pas(1) and manoir.peut_deplacer(joueur, d):
                manoir.deplacer(joueur, d)
                direction_ouverte = d
            else:
                print("[WARN] Mouvement impossible ou plus de pas.")

        # Ouverture (ESPACE) -> menu
        if actions.get("ouvrir"):
            if manoir.peut_ouvrir(joueur, direction_ouverte):
                manoir.options_courantes = tirer_trois(POOL, rng)
                etat = "choix"
                print(f"[LOG] Ouverture vers {direction_ouverte} → {len(manoir.options_courantes)} options.")
            else:
                print("[WARN] Hors de la grille : impossible d’ouvrir ici.")

        # MAJ direction dans la Vue + rendu
        vue.set_direction(direction_ouverte)
        vue.render()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
