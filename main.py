# -*- coding: utf-8 -*-
import random
import pygame

from affich_graph import Vue
from controle import Controleur
from inventaire import Inventaire
from manoir import Manoir, OPPOSITE
from effets import appliquer_effet, Contexte, tirage_objets

POOL = [
    {"type": "Galerie",      "couleur": "bleue",   "rarete": 0, "cout_gemmes": 0, "portes": {"haut","bas","gauche","droite"}},
    {"type": "Kitchen",      "couleur": "orange",  "rarete": 1, "cout_gemmes": 0, "portes": {"haut"}},
    {"type": "Bibliotheque", "couleur": "bleue",   "rarete": 1, "cout_gemmes": 1, "portes": {"gauche","droite"}},
    {"type": "Serre",        "couleur": "verte",   "rarete": 0, "cout_gemmes": 0, "portes": {"haut","bas"}},
    {"type": "Garage",       "couleur": "jaune",   "rarete": 1, "cout_gemmes": 1, "portes": {"bas","droite"}},
    {"type": "Observatoire", "couleur": "violette","rarete": 2, "cout_gemmes": 2, "portes": {"gauche","haut"}},
    {"type": "Fournaise",    "couleur": "rouge",   "rarete": 1, "cout_gemmes": 1, "portes": {"bas"}},
    # Exemple contrainte:
    # {"type":"Veranda","couleur":"verte","rarete":2,"cout_gemmes":0,"portes":{"haut","gauche"},"contrainte_placement":"bordure"},
]

def opposite(d): return OPPOSITE[d]

def main():
    pygame.init()
    pygame.display.set_caption("Blue Prince — MVP")

    rng = random.Random()
    inventaire = Inventaire(pas=75, or_=0, gemmes=2, cles=0, des=1, bananes=0)
    manoir = Manoir(lignes=5, colonnes=9, pool=POOL, rng=rng)
    joueur = manoir.joueur

    ecran = pygame.display.set_mode((1100, 800), pygame.RESIZABLE)
    vue = Vue(ecran, manoir, joueur, inventaire, dossier_images="image_pieces")

    controleur = Controleur(joueur, inventaire, manoir)
    clock = pygame.time.Clock()

    etat = "jeu"
    direction_ouverte = "haut"

    running = True
    while running:
        actions = controleur.handle_events()
        if actions == "quitter": break

        # --------- MENU CHOIX ---------
        if etat == "choix":
            vue.afficher_menu_choix(manoir.options_courantes, inventaire)

            idx = actions.get("choix_index")
            if idx is not None and 0 <= idx < len(manoir.options_courantes):
                piece = manoir.options_courantes[idx]
                cout = int(piece.get("cout_gemmes", 0))
                if cout <= inventaire.gemmes and inventaire.depenser_gemmes(cout):
                    x, y = manoir._case_devant(joueur, direction_ouverte)
                    if manoir.poser_piece(x, y, piece, back_dir=opposite(direction_ouverte)):
                        ctx = Contexte(inventaire, manoir)
                        log1 = appliquer_effet(piece, ctx)
                        log2 = tirage_objets(piece, ctx, rng)
                        if log1: print("[EFFET]", log1)
                        if log2: print("[LOOT]", log2)
                        etat = "jeu"
                    else:
                        print("[WARN] Pièce non posable (porte retour manquante ?).")
                else:
                    print("[WARN] Gemmes insuffisantes.")

            if actions.get("reroll"):
                if inventaire.depenser_des(1):
                    manoir.ouvrir(joueur, direction_ouverte, inventaire.gemmes)
                    print("[LOG] Reroll des options (–1 dé).")
                else:
                    print("[WARN] Pas de dé.")
            clock.tick(60); continue

        # --------- ETAT JEU ---------
        if actions.get("orient"):
            direction_ouverte = actions["orient"]

        if actions.get("move"):
            d = actions["move"]
            if inventaire.depenser_pas(1):
                ok = manoir.deplacer(joueur, d)
                print(f"[MOVE] {d} -> pos={joueur['x'], joueur['y']}")
                if not ok: print("[WARN] Pas de porte / case non posée / détour obligatoire.")
            else:
                print("[WARN] Plus de pas.")

        if actions.get("ouvrir"):
            ok = manoir.ouvrir(joueur, direction_ouverte, inventaire.gemmes)
            if ok and manoir.options_courantes:
                print(f"[LOG] Ouverture vers {direction_ouverte} -> options: {len(manoir.options_courantes)}")
                etat = "choix"
            else:
                print("[WARN] Impossible d’ouvrir (case non vide / hors grille / détour / aucune pièce posable).")

        # rendu & HUD
        vue.render(direction_ouverte)

        # victoire / défaites
        if manoir.est_antechamber(joueur["x"], joueur["y"]):
            _show_end(ecran, "Victoire ! Vous avez atteint l'Antechamber."); break
        if inventaire.pas <= 0:
            _show_end(ecran, "Défaite : plus de pas."); break
        if manoir.aucun_coup_possible(joueur) and inventaire.des <= 0 and inventaire.gemmes <= 0 and inventaire.cles <= 0:
            _show_end(ecran, "Défaite : aucun coup possible."); break

        clock.tick(60)

    pygame.quit()

def _show_end(ecran, message):
    pygame.display.set_caption("Blue Prince — Fin")
    surf = pygame.Surface(ecran.get_size()); surf.fill((10,10,10))
    font = pygame.font.SysFont("Arial", 48, bold=True)
    txt = font.render(message, True, (255,255,255))
    rect = txt.get_rect(center=(surf.get_width()//2, surf.get_height()//2))
    surf.blit(txt, rect); ecran.blit(surf, (0,0)); pygame.display.flip()
    pygame.time.wait(2500)

if __name__ == "__main__":
    main()
