# # -*- coding: utf-8 -*-
"""
manoir.py — Grille 5x9 par défaut : chaque case est un dictionnaire {"type": str, "couleur": str}
- Portes (niveaux 0/1/2)
- Déplacements, ouverture (prépare 3 options), placement d'une pièce
"""

from typing import List, Dict, Tuple
import random
from tirages import tirer_trois
from inventaire import Inventaire

Direction = str      # "haut", "bas", "gauche", "droite"
Piece = Dict[str, object]  # dictionnaire représentant une pièce

class Manoir:
    def __init__(self, lignes: int = 5, colonnes: int = 9, pool=None, rng=None, inventaire=None):
        self.lignes = lignes
        self.colonnes = colonnes
        self.inventaire = inventaire
        self.pool = pool or []
        self.rng = rng or random.Random()

        # Grille initialisée avec des cases vides
        self.grille: List[List[Piece]] = [
            [{"type": "vide", "couleur": "noir"} for _ in range(colonnes)]
            for _ in range(lignes)
        ]

        # Position initiale du joueur
        self.joueur: Dict[str, int] = {"x": lignes - 1, "y": colonnes // 2}

        # Fixer l'Entrance Hall à la position de départ
        self.grille[self.joueur["x"]][self.joueur["y"]] = {
            "type": "Entrance Hall",
            "couleur": "bleue",
            "cout_gemmes": 0
        }

        # Fixer l'Antechamber en haut au centre
        self.antechamber_pos = (0, colonnes // 2)
        self.grille[self.antechamber_pos[0]][self.antechamber_pos[1]] = {
            "type": "Antechamber",
            "couleur": "bleue",
            "cout_gemmes": 0
        }

        # Portes (niveau 0 à 2)
        self.portes: Dict[Direction, int] = {"haut": 0, "bas": 0, "gauche": 0, "droite": 0}

        # Options proposées après ouverture
        self.options_courantes: List[Piece] = []

    # --- Déplacements ---
    def _delta(self, direction: Direction) -> Tuple[int, int]:
        return {
            "haut": (-1, 0),
            "bas": (1, 0),
            "gauche": (0, -1),
            "droite": (0, 1),
        }.get(direction, (0, 0))

    def _dans_grille(self, x: int, y: int) -> bool:
        return 0 <= x < self.lignes and 0 <= y < self.colonnes

    def peut_deplacer(self, joueur: Dict[str, int], direction: Direction) -> bool:
        dx, dy = self._delta(direction)
        nx, ny = joueur["x"] + dx, joueur["y"] + dy
        return self._dans_grille(nx, ny)

    def deplacer(self, joueur: Dict[str, int], direction: Direction) -> None:
        if self.peut_deplacer(joueur, direction):
            dx, dy = self._delta(direction)
            joueur["x"] += dx
            joueur["y"] += dy

    # --- Portes ---
    def porte(self, direction: Direction) -> int:
        return int(self.portes.get(direction, 0))

    def peut_ouvrir(self, joueur: Dict[str, int], direction: Direction) -> bool:
        inventaire = self.inventaire
        dx, dy = self._delta(direction)
        nx, ny = joueur["x"] + dx, joueur["y"] + dy
        if not self._dans_grille(nx, ny):
            return False

        niveau = self.portes.get(direction, 0)
        if niveau == 1 and "kitdecrochetage" in inventaire.permanents:
            return True
        if niveau == 2:
            return inventaire.cles >= 1
        return True

    def ouvrir(self, joueur: Dict[str, int], direction: Direction) -> None:
        if not self.peut_ouvrir(joueur, direction):
            self.options_courantes = []
            return
        self.options_courantes = tirer_trois(self.pool, self.rng)

    # --- Placement de pièce ---
    def _case_devant(self, joueur: Dict[str, int], direction: Direction) -> Tuple[int, int]:
        dx, dy = self._delta(direction)
        return joueur["x"] + dx, joueur["y"] + dy

    def ok_placement(self, piece: Piece, x: int, y: int) -> bool:
        return self._dans_grille(x, y) and self.grille[x][y]["type"] == "vide"

    def poser_piece(self, x: int, y: int, piece: Piece) -> bool:
        if self.ok_placement(piece, x, y):
            self.grille[x][y] = {
                "type": str(piece.get("type", "inconnue")),
                "couleur": str(piece.get("couleur", "gris")),
                "cout_gemmes": int(piece.get("cout_gemmes", 0)),
            }
            return True
        return False

    def poser_devant(self, joueur: Dict[str, int], direction: Direction, piece: Piece) -> bool:
        x, y = self._case_devant(joueur, direction)
        ok = self.poser_piece(x, y, piece)
        if ok:
            self.options_courantes = []
        return ok

    # --- Détection de victoire ---
    def est_victoire(self) -> bool:
        return (
            self.joueur["x"] == self.antechamber_pos[0]
            and self.joueur["y"] == self.antechamber_pos[1]
        )
