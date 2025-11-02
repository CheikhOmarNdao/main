# -*- coding: utf-8 -*-
import os, glob
import pygame

# alias pour retrouver les bons sprites d'après le nom de pièce
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

# pièces à fond très sombre (leurs cartes sont sombres)
DARK_BG_TYPES = {"antechamber", "entrancehall"}

# --- PALETTE (fond noir)
CLR_BG         = (10, 10, 10)     # fond global
CLR_TILE       = (28, 28, 28)     # fond des cases posées
CLR_TILE_DARK  = (12, 12, 12)     # fond pour pièces "sombres"
CLR_GRID       = (90, 90, 90)     # bordure de case
CLR_DOOR       = (230, 230, 230)  # portes (clair)
CLR_ARROW      = (255, 230, 0)    # flèche du joueur
CLR_ARROW_OUT  = (255, 255, 255)  # contour de la flèche
CLR_HUD_BG     = (22, 22, 22)     # bandeau HUD
CLR_TEXT       = (240, 240, 240)  # texte clair
CLR_SUBTEXT    = (200, 200, 200)

class Vue:
    def __init__(self, ecran, manoir, joueur, inventaire, dossier_images="image_pieces"):
        self.ecran = ecran
        self.manoir = manoir
        self.joueur = joueur
        self.inventaire = inventaire
        self.dossier_images = dossier_images

        self.h_hud = 70

        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 20)
        self.font_big = pygame.font.SysFont("Arial", 64, bold=True)

        self.taille_case = self._calc_taille_case()

        self._sprites_src = {}
        self._sprites = {}
        self._charger_images_originaux(self.dossier_images)
        self._rescale_sprites()

    # tailles ------------------------------------------------------------------
    def _calc_taille_case(self) -> int:
        W, H = self.ecran.get_width(), self.ecran.get_height()
        if getattr(self.manoir, "lignes", 0) <= 0 or getattr(self.manoir, "colonnes", 0) <= 0:
            return 80
        H_dispo = max(1, H - self.h_hud - 8)
        t_x = max(1, W // self.manoir.colonnes)
        t_y = max(1, H_dispo // self.manoir.lignes)
        return max(48, min(128, min(t_x, t_y)))

    # sprites ------------------------------------------------------------------
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

    # rendu --------------------------------------------------------------------
    def render(self, direction_ouverte: str):
        new_t = self._calc_taille_case()
        if new_t != self.taille_case:
            self.taille_case = new_t
            self._rescale_sprites()

        # fond noir
        self.ecran.fill(CLR_BG)

        self._afficher_grille()
        self._afficher_joueur(direction_ouverte)
        self._afficher_hud()
        pygame.display.flip()

    def _afficher_grille(self):
        t = self.taille_case
        for i in range(self.manoir.lignes):
            for j in range(self.manoir.colonnes):
                rect = pygame.Rect(j*t, i*t, t, t)
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
                if "haut" in portes:   pygame.draw.rect(self.ecran, CLR_DOOR, (j*t + t//2-6, i*t, 12, ep))
                if "bas" in portes:    pygame.draw.rect(self.ecran, CLR_DOOR, (j*t + t//2-6, i*t + t-ep, 12, ep))
                if "gauche" in portes: pygame.draw.rect(self.ecran, CLR_DOOR, (j*t, i*t + t//2-6, ep, 12))
                if "droite" in portes: pygame.draw.rect(self.ecran, CLR_DOOR, (j*t + t-ep, i*t + t//2-6, ep, 12))

    def _afficher_joueur(self, direction_ouverte):
        """Affiche UNIQUEMENT une petite flèche au centre de la case du joueur."""
        t = self.taille_case
        x, y = self.joueur["x"], self.joueur["y"]

        # centre de la case
        cx = y * t + t // 2
        cy = x * t + t // 2
        s  = max(12, t // 4)  # taille de la flèche

        # triangles selon l’orientation
        if direction_ouverte == "haut":
            tri = [(cx, cy - s), (cx - s, cy + s), (cx + s, cy + s)]
        elif direction_ouverte == "bas":
            tri = [(cx, cy + s), (cx - s, cy - s), (cx + s, cy - s)]
        elif direction_ouverte == "gauche":
            tri = [(cx - s, cy), (cx + s, cy - s), (cx + s, cy + s)]
        else:  # "droite"
            tri = [(cx + s, cy), (cx - s, cy - s), (cx - s, cy + s)]

        # contour blanc (lisible sur fond sombre) puis remplissage jaune
        pygame.draw.polygon(self.ecran, CLR_ARROW_OUT, tri, width=max(2, t//24))
        pygame.draw.polygon(self.ecran, CLR_ARROW, tri)

    def _afficher_hud(self):
        w = self.manoir.colonnes * self.taille_case
        y = self.manoir.lignes * self.taille_case
        pygame.draw.rect(self.ecran, CLR_HUD_BG, (0, y, w, self.h_hud), border_radius=18)
        txt = self.font.render(self.inventaire.afficher(), True, CLR_TEXT)
        self.ecran.blit(txt, (16, y + self.h_hud//2 - 10))

    # menu (fond noir ; inventaire 2 colonnes ; cartes)
    def afficher_menu_choix(self, options, inventaire):
        W, H = self.ecran.get_width(), self.ecran.get_height()
        self.ecran.fill(CLR_BG)

        title_px = max(32, min(80, int(H*0.08)))
        title_font = pygame.font.SysFont("Arial", title_px, bold=True)
        title = title_font.render("Choose a room to draft", True, CLR_TEXT)
        self.ecran.blit(title, (int(W*0.06), int(H*0.06)))

        # panneau inventaire
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
            color = CLR_TEXT if i > 0 else (255, 255, 255)
            self.ecran.blit(info_font.render(s, True, color), (panel_x+8, panel_y+8+i*line_h))
        for i, s in enumerate(right_lines):
            self.ecran.blit(info_font.render(s, True, CLR_SUBTEXT),
                            (panel_x + 8 + box_w_left + 12, panel_y + 8 + i*line_h))

        # cartes ----------------------------------------------------------------
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
