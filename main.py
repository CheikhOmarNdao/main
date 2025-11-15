# -*- coding: utf-8 -*-
import random
import pygame

from affich_graph import Vue
from controle import Controleur
from inventaire import Inventaire
from manoir import Manoir, OPPOSITE
from effets import appliquer_effet, appliquer_effet_entree, Contexte, tirage_objets

POOL = [
    # --- Etage / pièces spéciales (hors Entrance / Antechamber) ---
    {"type": "Attic",               "couleur": "rouge",    "rarete": 2, "cout_gemmes": 1, "portes": {"bas"}},
    {"type": "Bedroom",             "couleur": "violette", "rarete": 2, "cout_gemmes": 1, "portes": {"gauche", "droite"}},
    {"type": "Chamber_of_Mirrors",  "couleur": "bleue",    "rarete": 3, "cout_gemmes": 3, "portes": {"haut", "bas", "gauche", "droite"}},
    {"type": "Chamber_of_Mirrors1", "couleur": "bleue",    "rarete": 3, "cout_gemmes": 3, "portes": {"haut", "bas", "gauche", "droite"}},
    {"type": "Closet",              "couleur": "rouge",    "rarete": 1, "cout_gemmes": 0, "portes": {"haut"}},

    # --- Couleur bleue / neutres ---
    {"type": "Foyer",               "couleur": "bleue",    "rarete": 1, "cout_gemmes": 0, "portes": {"haut", "bas"}},
    {"type": "Freezer",             "couleur": "bleue",    "rarete": 2, "cout_gemmes": 1, "portes": {"haut"}},
    {"type": "Gallery",             "couleur": "bleue",    "rarete": 2, "cout_gemmes": 1, "portes": {"gauche", "droite"}},
    {"type": "Garage",              "couleur": "bleue",    "rarete": 1, "cout_gemmes": 0, "portes": {"haut"}},
    {"type": "Gymnasium",           "couleur": "bleue",    "rarete": 2, "cout_gemmes": 1, "portes": {"haut", "bas"}},
    {"type": "Library",             "couleur": "bleue",    "rarete": 2, "cout_gemmes": 1, "portes": {"gauche", "droite"}},
    {"type": "Office",              "couleur": "bleue",    "rarete": 2, "cout_gemmes": 1, "portes": {"haut", "bas"}},
    {"type": "Parlor",              "couleur": "bleue",    "rarete": 2, "cout_gemmes": 1, "portes": {"bas"}},
    {"type": "Room_46",             "couleur": "bleue",    "rarete": 1, "cout_gemmes": 0, "portes": {"haut"}},
    {"type": "Study",               "couleur": "bleue",    "rarete": 1, "cout_gemmes": 0, "portes": {"bas"}},
    {"type": "The_Foundation",      "couleur": "bleue",    "rarete": 3, "cout_gemmes": 2, "portes": {"haut", "bas"}},
    {"type": "The_Pool",            "couleur": "bleue",    "rarete": 3, "cout_gemmes": 2, "portes": {"haut", "bas"}},
    {"type": "Trophy_Room",         "couleur": "bleue",    "rarete": 2, "cout_gemmes": 1, "portes": {"haut", "bas"}},
    {"type": "Vault",               "couleur": "bleue",    "rarete": 3, "cout_gemmes": 3, "portes": {"haut", "bas", "gauche", "droite"}},
    {"type": "Vault1",              "couleur": "bleue",    "rarete": 3, "cout_gemmes": 3, "portes": {"haut", "bas", "gauche", "droite"}},
    {"type": "Vault2",              "couleur": "bleue",    "rarete": 3, "cout_gemmes": 3, "portes": {"haut", "bas", "gauche", "droite"}},

    # --- Vertes ---
    {"type": "Greenhouse",          "couleur": "verte",    "rarete": 2, "cout_gemmes": 1, "portes": {"gauche", "droite"}},
    #{"type": "Morning_Room",        "couleur": "verte",    "rarete": 1, "cout_gemmes": 0, "portes": {"droite"}},
    {"type": "Patio",               "couleur": "verte",    "rarete": 2, "cout_gemmes": 1, "portes": {"haut", "bas"}},
    {"type": "Secret_Garden",       "couleur": "verte",    "rarete": 2, "cout_gemmes": 1, "portes": {"gauche", "droite"}},
    {"type": "Terrace",             "couleur": "verte",    "rarete": 2, "cout_gemmes": 1, "portes": {"bas", "droite"}},
    {"type": "Veranda",             "couleur": "verte",    "rarete": 2, "cout_gemmes": 2, "portes": {"haut", "gauche"}},

    # --- Jaunes ---
    {"type": "Kitchen1",            "couleur": "jaune",    "rarete": 1, "cout_gemmes": 0, "portes": {"haut"}},
    {"type": "Laundry_Room",        "couleur": "jaune",    "rarete": 1, "cout_gemmes": 0, "portes": {"gauche"}},
    {"type": "Mail_Room",           "couleur": "jaune",    "rarete": 2, "cout_gemmes": 1, "portes": {"haut", "bas"}},
    {"type": "Pantry",              "couleur": "jaune",    "rarete": 2, "cout_gemmes": 1, "portes": {"gauche"}},

    # --- Oranges / passages ---
    {"type": "Passageway",          "couleur": "orange",   "rarete": 1, "cout_gemmes": 0, "portes": {"gauche", "droite"}},
    {"type": "Passageway1",         "couleur": "orange",   "rarete": 1, "cout_gemmes": 0, "portes": {"gauche", "droite"}},
    {"type": "The_Armory",          "couleur": "orange",   "rarete": 2, "cout_gemmes": 1, "portes": {"haut", "bas"}},

    # --- Rouges / violettes ---
    {"type": "Lavatory",            "couleur": "rouge",    "rarete": 1, "cout_gemmes": 0, "portes": {"droite"}},
    {"type": "Lavatory1",           "couleur": "rouge",    "rarete": 1, "cout_gemmes": 0, "portes": {"gauche"}},
    {"type": "Nursery",             "couleur": "violette", "rarete": 1, "cout_gemmes": 0, "portes": {"gauche"}},
    {"type": "Sauna",               "couleur": "rouge",    "rarete": 2, "cout_gemmes": 1, "portes": {"haut"}},
    {"type": "Security",            "couleur": "rouge",    "rarete": 2, "cout_gemmes": 1, "portes": {"haut", "bas"}},
    {"type": "Utility_Closet",      "couleur": "rouge",    "rarete": 1, "cout_gemmes": 0, "portes": {"haut"}},
    {"type": "Utility_Closet1",     "couleur": "rouge",    "rarete": 1, "cout_gemmes": 0, "portes": {"bas"}},
    {"type": "Weight_Room",         "couleur": "rouge",    "rarete": 2, "cout_gemmes": 1, "portes": {"gauche", "droite"}},
]


def opposite(d):
    return OPPOSITE[d]


def main():
    pygame.init()
    pygame.display.set_caption("Blue Prince — MVP")

    rng = random.Random()
    inventaire = Inventaire(pas=70, or_=0, gemmes=2, cles=0, des=0, bananes=0)
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
        if actions == "quitter":
            break

        # --------- MENU CHOIX ---------
        if etat == "choix":
            vue.afficher_menu_choix(manoir.options_courantes, inventaire)

            idx = actions.get("choix_index")
            if idx is not None and 0 <= idx < len(manoir.options_courantes):
                piece = manoir.options_courantes[idx]
                cout = int(piece.get("cout_gemmes", 0))

                # On peut payer le coût avec gemmes + clés (gemmes d'abord, puis clés)
                total_ressources = inventaire.gemmes + inventaire.cles
                if cout <= total_ressources:
                    gem_a_payer = min(cout, inventaire.gemmes)
                    cle_a_payer = cout - gem_a_payer

                    if gem_a_payer > 0:
                        inventaire.depenser_gemmes(gem_a_payer)
                    if cle_a_payer > 0:
                        inventaire.depenser_cles(cle_a_payer)

                    x, y = manoir._case_devant(joueur, direction_ouverte)
                    if manoir.poser_piece(x, y, piece, back_dir=opposite(direction_ouverte)):
                        ctx = Contexte(inventaire, manoir)
                        log1 = appliquer_effet(piece, ctx)
                        log2 = tirage_objets(piece, ctx, rng)
                        if log1:
                            print("[EFFET]", log1)
                        if log2:
                            print("[LOOT]", log2)
                        etat = "jeu"
                    else:
                        print("[WARN] Pièce non posable (porte retour manquante ?).")
                else:
                    print("[WARN] Gemmes/Clés insuffisantes.")

            if actions.get("reroll"):
                if inventaire.depenser_des(1):
                    # ouverture possible si au moins une ressource (gemme ou clé)
                    manoir.ouvrir(joueur, direction_ouverte, inventaire.gemmes + inventaire.cles)
                    print("[LOG] Reroll des options (–1 dé).")
                else:
                    print("[WARN] Pas de dé.")
            clock.tick(60)
            continue

        # --------- ETAT JEU ---------
        if actions.get("orient"):
            direction_ouverte = actions["orient"]

        if actions.get("move"):
            d = actions["move"]
            if inventaire.depenser_pas(1):
                # on passe aussi l'inventaire à deplacer (verrous, etc.)
                ok = manoir.deplacer(joueur, d, inventaire)
                print(f"[MOVE] {d} -> pos=({joueur['x']}, {joueur['y']})")
                if ok:
                    # Effet éventuel quand on ENTRE dans la nouvelle pièce
                    piece_actuelle = manoir._piece(joueur["x"], joueur["y"])
                    ctx = Contexte(inventaire, manoir)
                    log_entree = appliquer_effet_entree(piece_actuelle, ctx)
                    if log_entree:
                        print("[EFFET ENTREE]", log_entree)

                    # Ressources cachées éventuelles sur la case (Patio / Office ...)
                    log_cache = manoir.ramasser_ressources_case(joueur["x"], joueur["y"], inventaire)
                    if log_cache:
                        print("[CACHE]", log_cache)
                else:
                    print("[WARN] Pas de porte / case non posée / détour obligatoire / porte verrouillée.")
            else:
                print("[WARN] Plus de pas.")

        if actions.get("ouvrir"):
            # ouverture possible si au moins une ressource (gemme ou clé)
            ok = manoir.ouvrir(joueur, direction_ouverte, inventaire.gemmes + inventaire.cles)
            if ok and manoir.options_courantes:
                print(f"[LOG] Ouverture vers {direction_ouverte} -> options: {len(manoir.options_courantes)}")
                etat = "choix"
            else:
                print("[WARN] Impossible d’ouvrir (case non vide / hors grille / détour / aucune pièce posable).")

        # rendu & HUD
        vue.render(direction_ouverte)

        # victoire / défaites
        if manoir.est_antechamber(joueur["x"], joueur["y"]):
            _show_end(ecran, "Victoire ! Projet 4 SYSCOM vous félicite")
            break
        if inventaire.pas <= 0:
            _show_end(ecran, "Défaite : plus de pas.")
            break
        if manoir.aucun_coup_possible(joueur) and inventaire.des <= 0 and inventaire.gemmes <= 0 and inventaire.cles <= 0:
            _show_end(ecran, "Défaite : aucun coup possible.")
            break

        clock.tick(60)

    pygame.quit()


def _show_end(ecran, message: str):
    pygame.display.set_caption("Blue Prince — Fin")
    surf = pygame.Surface(ecran.get_size())
    surf.fill((10, 10, 10))
    font = pygame.font.SysFont("Arial", 48, bold=True)
    txt = font.render(message, True, (255, 255, 255))
    rect = txt.get_rect(center=(surf.get_width() // 2, surf.get_height() // 2))
    surf.blit(txt, rect)
    ecran.blit(surf, (0, 0))
    pygame.display.flip()
    pygame.time.wait(2500)


if __name__ == "__main__":
    main()
