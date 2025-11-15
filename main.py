# -*- coding: utf-8 -*-
import random
import pygame

from affich_graph import Vue
from controle import Controleur
from inventaire import Inventaire
from manoir import Manoir, OPPOSITE
from effets import appliquer_effet, appliquer_effet_entree, Contexte, tirage_objets

POOL = [
    # Etage / pièces spéciales (hors Entrance / Antechamber) 
    {"type": "Attic",               "couleur": "rouge",    "rarete": 2, "cout_gemmes": 1, "portes": {"bas"}},
    {"type": "Bedroom",             "couleur": "violette", "rarete": 2, "cout_gemmes": 1, "portes": {"gauche", "droite"}},
    {"type": "Chamber_of_Mirrors",  "couleur": "bleue",    "rarete": 3, "cout_gemmes": 3, "portes": {"haut", "bas", "gauche", "droite"}},
    {"type": "Chamber_of_Mirrors1", "couleur": "bleue",    "rarete": 3, "cout_gemmes": 3, "portes": {"haut", "bas", "gauche", "droite"}},
    {"type": "Closet",              "couleur": "rouge",    "rarete": 1, "cout_gemmes": 0, "portes": {"haut"}},
    # autres 
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
    {"type": "Greenhouse",          "couleur": "verte",    "rarete": 2, "cout_gemmes": 1, "portes": {"gauche", "droite"}},
    #{"type": "Morning_Room"
     {"type": "Patio",               "couleur": "verte",    "rarete": 2, "cout_gemmes": 1, "portes": {"haut", "bas"}},
    {"type": "Secret_Garden",       "couleur": "verte",    "rarete": 2, "cout_gemmes": 1, "portes": {"gauche", "droite"}},
    {"type": "Terrace",             "couleur": "verte",    "rarete": 2, "cout_gemmes": 1, "portes": {"bas", "droite"}},
    {"type": "Veranda",             "couleur": "verte",    "rarete": 2, "cout_gemmes": 2, "portes": {"haut", "gauche"}},
     #autres
    {"type": "Kitchen1",            "couleur": "jaune",    "rarete": 1, "cout_gemmes": 0, "portes": {"haut"}},
    {"type": "Laundry_Room",        "couleur": "jaune",    "rarete": 1, "cout_gemmes": 0, "portes": {"gauche"}},
    {"type": "Mail_Room",           "couleur": "jaune",    "rarete": 2, "cout_gemmes": 1, "portes": {"haut", "bas"}},
    {"type": "Pantry",              "couleur": "jaune",    "rarete": 2, "cout_gemmes": 1, "portes": {"gauche"}},
    {"type": "Passageway",          "couleur": "orange",   "rarete": 1, "cout_gemmes": 0, "portes": {"gauche", "droite"}},
    {"type": "Passageway1",         "couleur": "orange",   "rarete": 1, "cout_gemmes": 0, "portes": {"gauche", "droite"}},
    {"type": "The_Armory",          "couleur": "orange",   "rarete": 2, "cout_gemmes": 1, "portes": {"haut", "bas"}},
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

        #  MENU CHOIX 
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

        #     ETAT JEU 
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

                    # Ressources cachées éventuelles sur la case (Patio / Office ..)
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

        # rendu et HUD
        vue.render(direction_ouverte)

        # victoire / défaites
        if manoir.est_antechamber(joueur["x"], joueur["y"]):
            _show_end(ecran, "Victoire ! Projet 4 SYSCOM vous félicite")
            break
        if inventaire.pas <= 0:
            _show_end(ecran, "Défaite : pas=0 Projet 4 SYSCOM vous invite à une autre partie")
            i=0
            while i<10000000:  # pour gagner du temps pour lire 
                  i+=1
            break
        if manoir.aucun_coup_possible(joueur) and inventaire.des <= 0 and inventaire.gemmes <= 0 and inventaire.cles <= 0:
            _show_end(ecran, "Défaite : aucun coup possible")
            break

        clock.tick(60)   #60 FPS

    pygame.quit()


def _show_end(ecran, message: str):
    import os
    import random
    import pygame

   
    pygame.display.set_caption("Blue Prince — Fin")

    W, H = ecran.get_size()
    clock = pygame.time.Clock()

    # --- 1) extinction d'une grille 5x9 style "manoir" ---
    rows, cols = 5, 9
    cell_w = W // cols
    cell_h = H // rows
    all_cells = [(i, j) for i in range(rows) for j in range(cols)]
    random.shuffle(all_cells)
    lit_cells = set(all_cells)

    # --- 2) chute du joueur (un petit cercle qui tombe) ---
    player_x = W // 2
    player_y = H // 3
    player_r = max(10, W // 50)
    player_vy = H // 120

    # --- 3) texte final en fondu ---
    title_text = "Vous n’étiez pas le Prince Bleu…"
    subtitle_text = message
    title_font = pygame.font.SysFont("Arial", 42, bold=True)
    subtitle_font = pygame.font.SysFont("Arial", 26)

    alpha = 0
    alpha_step = 4
    phase = 0      # 0 = extinction, 1 = chute, 2 = fade texte, 3 = pause
    phase_timer = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        ecran.fill((0, 0, 0))

        # PHASE 0 : extinction cellule par cellule
        if phase == 0:
            for _ in range(4):
                if all_cells:
                    cell = all_cells.pop()
                    if cell in lit_cells:
                        lit_cells.remove(cell)

            for i in range(rows):
                for j in range(cols):
                    x = j * cell_w
                    y = i * cell_h
                    if (i, j) in lit_cells:
                        col = (40, 40, 80)
                    else:
                        col = (5, 5, 10)
                    pygame.draw.rect(ecran, col, (x, y, cell_w + 1, cell_h + 1))

            if not lit_cells:
                phase = 1

        # PHASE 1 : chute du joueur
        elif phase == 1:
            ecran.fill((0, 0, 0))
            pygame.draw.circle(ecran, (220, 220, 255), (player_x, int(player_y)), player_r)
            player_y += player_vy
            if player_y - player_r > H + 20:
                phase = 2

        # PHASE 2 : texte en fondu
        elif phase == 2:
            ecran.fill((0, 0, 0))

            if alpha < 255:
                alpha = min(255, alpha + alpha_step)

            title_surf = title_font.render(title_text, True, (255, 255, 255)).convert_alpha()
            subtitle_surf = subtitle_font.render(subtitle_text, True, (200, 200, 200)).convert_alpha()
            title_surf.set_alpha(alpha)
            subtitle_surf.set_alpha(alpha)

            rect_title = title_surf.get_rect(center=(W // 2, H // 2 - 20))
            rect_sub = subtitle_surf.get_rect(center=(W // 2, H // 2 + 30))

            ecran.blit(title_surf, rect_title)
            ecran.blit(subtitle_surf, rect_sub)

            if alpha >= 255:
                phase_timer += clock.get_time()
                if phase_timer > 2500:
                    phase = 3
                    phase_timer = 0

        # PHASE 3 : écran figé quelques secondes
        elif phase == 3:
            ecran.fill((0, 0, 0))
            title_surf = title_font.render(title_text, True, (255, 255, 255))
            subtitle_surf = subtitle_font.render(subtitle_text, True, (200, 200, 200))
            rect_title = title_surf.get_rect(center=(W // 2, H // 2 - 20))
            rect_sub = subtitle_surf.get_rect(center=(W // 2, H // 2 + 30))
            ecran.blit(title_surf, rect_title)
            ecran.blit(subtitle_surf, rect_sub)

            phase_timer += clock.get_time()
            if phase_timer > 4000:
                running = False

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
