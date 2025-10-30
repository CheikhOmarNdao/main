# -*- coding: utf-8 -*-
"""
Affichage : grille, HUD, menu + flèche de direction du joueur.
Fond noir initial + cases non explorées en gris foncé.
"""

import os
import glob
import pygame

ALIAS_SPRITES = {
    "serre": "greenhouse",
    "observatoire": "observatory",
    "galerie": "gallery",
    "garage": "garage",
    "bibliotheque": "library",
    "cuisine": "kitchen",
    "couloir": "passageway",
    "salleamanger": "diningroom",
    "chambre": "bedroom",
    "atelier": "workshop",
    "patio": "patio",
    "foyer": "foyer",
}


class Vue:
    """Classe responsable de l'affichage graphique du manoir et de l'inventaire."""

    def __init__(self, ecran, manoir, joueur, inventaire, dossier_images="image_pieces"):
        self.ecran = ecran
        self.manoir = manoir
        self.joueur = joueur
        self.inventaire = inventaire
        self.taille_case = 80
        self.police = pygame.font.SysFont("Arial", 20)

        self.couleurs = {
            "bleue": (80, 150, 255), "orange": (255, 160, 70), "verte": (80, 200, 120),
            "violette": (180, 100, 255), "jaune": (250, 230, 100), "rouge": (230, 80, 80),
            "gris": (200, 200, 200), "gris_fonce": (60, 60, 60)
        }

        self.direction = "droite"   # direction affichée par la flèche

        # cache d’images
        self._sprites = {}
        self._charger_images(dossier_images)

    # --- direction (appelée depuis main) ---
    def set_direction(self, d: str):
        if d in ("haut", "bas", "gauche", "droite"):
            self.direction = d

    # --- assets ---
    @staticmethod
    def _norm(nom: str) -> str:
        return "".join(ch.lower() for ch in nom if ch.isalnum())

    def _charger_images(self, dossier_images: str):
        if not os.path.isdir(dossier_images):
            return
        for path in glob.glob(os.path.join(dossier_images, "*.png")):
            nom_fichier = os.path.splitext(os.path.basename(path))[0]
            cle = self._norm(nom_fichier)
            try:
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.smoothscale(img, (self.taille_case, self.taille_case))
                self._sprites[cle] = img
            except Exception:
                pass

    def _sprite_pour_type(self, type_piece: str):
        k = self._norm(type_piece)
        if k in ALIAS_SPRITES:
            alias_k = self._norm(ALIAS_SPRITES[k])
            if alias_k in self._sprites:
                return self._sprites[alias_k]
        if k in self._sprites:
            return self._sprites[k]
        for cle, surf in self._sprites.items():
            if k and k in cle:
                return surf
        return None

    # --- rendu ---
    def render(self):
        # fond noir initial
        self.ecran.fill((0, 0, 0))
        self.afficher_grille()
        self.afficher_joueur()
        self.afficher_hud()
        pygame.display.flip()

    def afficher_grille(self):
        for i in range(self.manoir.lignes):
            for j in range(self.manoir.colonnes):
                piece = self.manoir.grille[i][j]
                rect = pygame.Rect(
                    j * self.taille_case,
                    i * self.taille_case,
                    self.taille_case,
                    self.taille_case
                )

                # Dessin bordure
                pygame.draw.rect(self.ecran, (0, 0, 0), rect, 2)

                # Si la case est vide ou non explorée
                if not piece or not piece.get("type"):
                    pygame.draw.rect(self.ecran, self.couleurs["gris_fonce"], rect.inflate(-4, -4))
                    continue

                # Sinon, dessiner la pièce (sprite ou couleur)
                sp = self._sprite_pour_type(piece.get("type", ""))
                if sp is not None:
                    self.ecran.blit(sp, rect.topleft)
                else:
                    couleur = self.couleurs.get(piece.get("couleur", "gris"), (220, 220, 220))
                    pygame.draw.rect(self.ecran, couleur, rect.inflate(-4, -4))

    def afficher_joueur(self):
        rect = pygame.Rect(
            self.joueur["y"] * self.taille_case + 10,
            self.joueur["x"] * self.taille_case + 10,
            self.taille_case - 20,
            self.taille_case - 20,
        )
        pygame.draw.rect(self.ecran, (0, 0, 255), rect)

        # --- flèche de direction ---
        cx = rect.centerx
        cy = rect.centery
        t = 12  # taille du triangle
        if self.direction == "haut":
            pts = [(cx, cy - t - 10), (cx - t, cy - 10), (cx + t, cy - 10)]
        elif self.direction == "bas":
            pts = [(cx, cy + t + 10), (cx - t, cy + 10), (cx + t, cy + 10)]
        elif self.direction == "gauche":
            pts = [(cx - t - 10, cy), (cx - 10, cy - t), (cx - 10, cy + t)]
        else:  # droite
            pts = [(cx + t + 10, cy), (cx + 10, cy - t), (cx + 10, cy + t)]

        pygame.draw.polygon(self.ecran, (30, 30, 30), pts)
        pygame.draw.polygon(self.ecran, (250, 250, 0), pts, 2)

    def afficher_hud(self):
        barre = pygame.Rect(
            0,
            self.manoir.lignes * self.taille_case,
            self.manoir.colonnes * self.taille_case,
            60
        )
        pygame.draw.rect(self.ecran, self.couleurs["gris"], barre)
        texte = self.police.render(self.inventaire.afficher(), True, (0, 0, 0))
        self.ecran.blit(texte, (10, self.manoir.lignes * self.taille_case + 20))

    def afficher_menu_choix(self, options):
        self.ecran.fill((0, 0, 0))
        y0 = 50
        for i, piece in enumerate(options):
            txt = f"{i+1}. {piece['type']}  (gemmes: {piece.get('cout_gemmes',0)})"
            surf_txt = self.police.render(txt, True, (255, 255, 255))
            self.ecran.blit(surf_txt, (120, y0 + i * 80))

            sp = self._sprite_pour_type(piece.get("type", ""))
            if sp:
                vignette = pygame.transform.smoothscale(sp, (64, 64))
                self.ecran.blit(vignette, (40, y0 + i * 80 - 10))
        pygame.display.flip()

    def afficher_fin(self, message, perdu=False, gagne=False):
        if perdu:
            couleur_fond = self.couleurs["rouge"]
        elif gagne:
            couleur_fond = self.couleurs["verte"]
        else:
            couleur_fond = (0, 0, 0)

        self.ecran.fill(couleur_fond)
        texte = self.police.render(message, True, (255, 255, 255))
        rect = texte.get_rect(center=(self.ecran.get_width() // 2, self.ecran.get_height() // 2))
        self.ecran.blit(texte, rect)
        pygame.display.flip()
        pygame.time.wait(3000)
