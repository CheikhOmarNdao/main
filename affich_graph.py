# -*- coding: utf-8 -*-
import os, glob
import pygame

# alias sprites
ALIAS_SPRITES = {
    "serre": "greenhouse",
    "observatoire": "observatory",
    "galerie": "gallery",
    "garage": "garage",
    "bibliotheque": "library",
    "cuisine": "kitchen",
    "entrancehall": "entrancehall",
    "antechamber": "antechamber",
}
DARK_BG_TYPES = {"antechamber", "entrancehall"}

# palette (fond noir)
CLR_BG         = (10, 10, 10)
CLR_TILE       = (28, 28, 28)
CLR_TILE_DARK  = (12, 12, 12)
CLR_GRID       = (90, 90, 90)
CLR_DOOR       = (230, 230, 230)
CLR_ARROW      = (255, 230, 0)
CLR_ARROW_OUT  = (255, 255, 255)
CLR_HUD_BG     = (22, 22, 22)
CLR_TEXT       = (240, 240, 240)
CLR_SUBTEXT    = (200, 200, 200)

class Vue:
    def __init__(self, ecran, manoir, joueur, inventaire, dossier_images="image_pieces"):
        self.ecran = ecran
        self.manoir = manoir
        self.joueur = joueur
        self.inventaire = inventaire
        self.dossier_images = dossier_images

        # bandeau HUD( on addiche les gemmes ...) + marges autour de la grille
        self.h_hud = 70 # hauteur en bas du fénetre 
        self.pad_top = 14 #hauteur verticale en haut pour ne pas coller le haut de l'écran au bord
        self.pad_bottom = 10 # marge au dessus du HUD
        self.pad_left = 14 # marge à gauche de la grille 
        self.pad_right = 14 # marge à droite de la grille 

        # offsets de dessin (calculés à chaque frame)
        self.offset_x = 0
        self.offset_y = 0

        pygame.font.init()   #Initialise le module des polices de caractères de Pygame
        self.font = pygame.font.SysFont("Arial", 20) #Police “normale” pour le HUD, les textes d’info, etc. Taille 20
        self.font_big = pygame.font.SysFont("Arial", 64, bold=True) #Grande police en gras comme texte de fin

        self.taille_case = self._calc_taille_case() #pour calculer la taille d'1 piece en f(nombre de ligend et de colones du manoir)

        self._sprites_src = {} #mages originales chargées depuis le dossier
        self._sprites = {} #mêmes images mais redimensionnées à taille_case pour l’affichage.
        self._charger_images_originaux(self.dossier_images) #charge tout les png et les met dans -sprite_rc
        self._rescale_sprites()

    #    tailles :choisir automatiquement la taille d’1 case de la grille pour que tout le manoir tienne bien dans la fenêtre
    def _calc_taille_case(self) -> int:
        W, H = self.ecran.get_width(), self.ecran.get_height()
        if getattr(self.manoir, "lignes", 0) <= 0 or getattr(self.manoir, "colonnes", 0) <= 0:
            return 80
        # on réserve HUD + paddings vertical
        vertical_margin = self.h_hud + self.pad_top + self.pad_bottom
        H_dispo = max(1, H - vertical_margin)
        t_x = max(1, (W - (self.pad_left + self.pad_right)) // self.manoir.colonnes)
        t_y = max(1, H_dispo // self.manoir.lignes)
        return max(48, min(128, min(t_x, t_y)))

    def _update_offsets(self):  #calculer où dessiner la grille dans la fenêtre
        """Centre horizontalement, ajoute la marge haute pour éviter la 'découpe' en haut."""
        W, H = self.ecran.get_width(), self.ecran.get_height()
        grid_w = self.manoir.colonnes * self.taille_case
        self.offset_x = max(self.pad_left, (W - grid_w) // 2) # offset horizontal centré (au moins pad_left)
        self.offset_y = self.pad_top  # offset vertical = marge haute

# Ensuite on scanne dossier d’images, charge ttes les png, les indexe par un nom nettoyé , et les garde dans self._sprites_src pour qu’ensuite _rescale_sprites() puisse les redimensionner et que _sprite() puisse les afficher sur la grille.
    # sprites 
    @staticmethod
    def _norm(s: str) -> str:
        return "".join(ch.lower() for ch in s if ch.isalnum())

    def _charger_images_originaux(self, dossier):
        self._sprites_src.clear()
        if not os.path.isdir(dossier): return
        for p in glob.glob(os.path.join(dossier, "*.png")):
            name = os.path.splitext(os.path.basename(p))[0]
            key = self._norm(name)
            try:
                img = pygame.image.load(p).convert_alpha()
                self._sprites_src[key] = img
            except Exception:
                pass

    def _rescale_sprites(self):
        self._sprites.clear()
        t = self.taille_case
        for key, surf in self._sprites_src.items():
            try:
                self._sprites[key] = pygame.transform.smoothscale(surf, (t, t))
            except Exception:
                pass

    def _sprite(self, type_piece: str):
        k = self._norm(type_piece)
        if k in ALIAS_SPRITES:
            ak = self._norm(ALIAS_SPRITES[k])
            if ak in self._sprites: return self._sprites[ak]
        if k in self._sprites: return self._sprites[k]
        for kk, surf in self._sprites.items():
            if k and k in kk: return surf
        return None

    # rendu 
    #à chaque tour de boucle, on appelle render(...) pour tout redessiner
    def render(self, direction_ouverte: str):
        new_t = self._calc_taille_case()
        if new_t != self.taille_case:
            self.taille_case = new_t
            self._rescale_sprites()

        self._update_offsets()

        self.ecran.fill(CLR_BG)
        self._afficher_grille()
        self._afficher_joueur(direction_ouverte)
        self._afficher_hud()
        pygame.display.flip()

#Pour dessiner toute la grille du manoir case par case
    def _afficher_grille(self):
        t = self.taille_case
        ox, oy = self.offset_x, self.offset_y
        for i in range(self.manoir.lignes):
            for j in range(self.manoir.colonnes):
                rect = pygame.Rect(ox + j*t, oy + i*t, t, t)
                piece = self.manoir.grille[i][j]
                typ = self._norm(piece["type"])

                if piece["type"] != "vide":
                    bg = CLR_TILE_DARK if typ in DARK_BG_TYPES else CLR_TILE
                    pygame.draw.rect(self.ecran, bg, rect, border_radius=8)

                pygame.draw.rect(self.ecran, CLR_GRID, rect, 2, border_radius=8)

                if piece["type"] != "vide":
                    sp = self._sprite(piece["type"])
                    if sp: self.ecran.blit(sp, rect.topleft)

                portes = piece.get("portes", set())
                ep = max(6, t//12)
                if "haut" in portes:   pygame.draw.rect(self.ecran, CLR_DOOR, (ox + j*t + t//2-6, oy + i*t, 12, ep))
                if "bas" in portes:    pygame.draw.rect(self.ecran, CLR_DOOR, (ox + j*t + t//2-6, oy + i*t + t-ep, 12, ep))
                if "gauche" in portes: pygame.draw.rect(self.ecran, CLR_DOOR, (ox + j*t, oy + i*t + t//2-6, ep, 12))
                if "droite" in portes: pygame.draw.rect(self.ecran, CLR_DOOR, (ox + j*t + t-ep, oy + i*t + t//2-6, ep, 12))
#Pour dessiner le joueur, sous forme d’une petite flèche orientée
    def _afficher_joueur(self, direction_ouverte):
        """Affiche UNIQUEMENT une petite flèche au centre de la case du joueur."""
        t = self.taille_case
        ox, oy = self.offset_x, self.offset_y
        x, y = self.joueur["x"], self.joueur["y"]

        # centre de la case (avec offset)
        cx = ox + y * t + t // 2
        cy = oy + x * t + t // 2
        s  = max(12, t // 4)

        if direction_ouverte == "haut":
            tri = [(cx, cy - s), (cx - s, cy + s), (cx + s, cy + s)]
        elif direction_ouverte == "bas":
            tri = [(cx, cy + s), (cx - s, cy - s), (cx + s, cy - s)]
        elif direction_ouverte == "gauche":
            tri = [(cx - s, cy), (cx + s, cy - s), (cx + s, cy + s)]
        else:  # droite
            tri = [(cx + s, cy), (cx - s, cy - s), (cx - s, cy + s)]

        pygame.draw.polygon(self.ecran, CLR_ARROW_OUT, tri, width=max(2, t//24))
        pygame.draw.polygon(self.ecran, CLR_ARROW, tri)

# HUD pleine largeur en bas de la grille 
    def _afficher_hud(self):
        W, H = self.ecran.get_size()
        grid_h = self.manoir.lignes * self.taille_case
        y = self.offset_y + grid_h
        pygame.draw.rect(self.ecran, CLR_HUD_BG, (0, y, W, self.h_hud))
        txt = self.font.render(self.inventaire.afficher(), True, CLR_TEXT)
        self.ecran.blit(txt, (16, y + self.h_hud//2 - 10))

    # menu 
    #tt l’écran de “draft” des salles, autrement dit le menu où on choisit 1 des 3 pièces proposées après avoir ouvert une porte
    def afficher_menu_choix(self, options, inventaire):
        W, H = self.ecran.get_width(), self.ecran.get_height()
        self.ecran.fill(CLR_BG)

        title_px = max(32, min(80, int(H*0.08)))
        title_font = pygame.font.SysFont("Arial", title_px, bold=True)
        title = title_font.render("Choose a room to draft", True, CLR_TEXT)
        self.ecran.blit(title, (int(W*0.06), int(H*0.06)))

        permas = inventaire.liste_permanents()
        left_lines = ["Inventory:"] + (permas if permas else ["(none)"])
        right_lines = [
            f"Pas: {inventaire.pas}",
            f"Or: {inventaire.or_}",
            f"Gemmes: {inventaire.gemmes}",
            f"Clés: {inventaire.cles}",
            f"Dés: {inventaire.des}",
            f"Bananes: {inventaire.bananes}",
            "Reroll: R (–1 dé)",
        ]
        info_font = pygame.font.SysFont("Arial", max(18, int(H*0.03)))
        line_h = info_font.get_height() + 2
        box_w_left = max(info_font.size(s)[0] for s in left_lines) + 16
        box_w_right = max(info_font.size(s)[0] for s in right_lines) + 16
        box_h = max(len(left_lines), len(right_lines)) * line_h + 16
        panel = pygame.Surface((box_w_left + 12 + box_w_right, box_h), pygame.SRCALPHA)
        panel.fill((20, 20, 20, 230))
        panel_x = W - panel.get_width() - 24
        panel_y = int(H*0.14)
        self.ecran.blit(panel, (panel_x, panel_y))
        for i, s in enumerate(left_lines):
            color = CLR_TEXT if i > 0 else (255,255,255)
            self.ecran.blit(info_font.render(s, True, color), (panel_x+8, panel_y+8+i*line_h))
        for i, s in enumerate(right_lines):
            self.ecran.blit(info_font.render(s, True, CLR_SUBTEXT),
                            (panel_x + 8 + box_w_left + 12, panel_y + 8 + i*line_h))

        # cartes
        margin_x = int(W*0.06); top_y = max(int(H*0.28), panel_y + box_h + 20)
        avail_w = W - 2*margin_x; gap = max(24, int(W*0.04)); frame_pad = 16
        card_w = int((avail_w - 2*gap - 3*frame_pad) / 3)
        card_w = max(120, min(260, card_w))
        while (card_w + frame_pad)*3 + gap*2 > avail_w and gap > 10: gap -= 2
        while (card_w + frame_pad)*3 + gap*2 > avail_w and card_w > 110: card_w -= 2
        card_h = card_w; border = max(4, card_w//36)
        total_row_w = (card_w + frame_pad)*3 + gap*2
        start_x = max(margin_x, (W - total_row_w)//2)

        for i, piece in enumerate(options[:3]):
            x = start_x + i*(card_w + frame_pad + gap); y = top_y
            typ = self._norm(piece.get("type", ""))
            card_bg = CLR_TILE_DARK if typ in DARK_BG_TYPES else CLR_TILE

            pygame.draw.rect(self.ecran, (0,140,220),
                             (x - frame_pad//2, y - frame_pad//2, card_w + frame_pad, card_h + frame_pad),
                             width=border, border_radius=12)
            pygame.draw.rect(self.ecran, card_bg, (x, y, card_w, card_h), border_radius=12)

            sp = self._sprite(piece.get("type",""))
            if sp:
                big = pygame.transform.smoothscale(sp, (card_w, card_h))
                self.ecran.blit(big, (x, y))

            name = f"{i+1}. {piece.get('type','?')}"
            cost = f"cost: {int(piece.get('cout_gemmes', 0))} ♦"
            name_font = pygame.font.SysFont("Arial", max(22, int(card_w*0.12)), bold=True)
            cost_font = pygame.font.SysFont("Arial", max(18, int(card_w*0.10)))
            name_color = (240,240,240)
            cost_color = (200,200,200)
            name_s = name_font.render(name, True, name_color)
            cost_s = cost_font.render(cost, True, cost_color)
            self.ecran.blit(name_s, (x, y + card_h + 14))
            self.ecran.blit(cost_s, (x, y + card_h + 14 + name_s.get_height() + 6))

        pygame.display.flip()
