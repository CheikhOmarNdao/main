# -*- coding: utf-8 -*-
"""
manoir
- Grille 5x9 par défaut : chaque case est un dictionnaire {"type": str, "couleur": str}
- Portes (niveaux 0/1/2)
- Déplacements, ouverture (prépare 3 options), placement d'une pièce
"""

from typing import List, Dict, Tuple
import random
from tirages import tirer_trois

Direction = str      #haut,bas,gauche,droite
Piece = Dict[str, object]       #dictionnaire représentant une pièce


class Manoir:
    #Grille, portes et actions de base

    def __init__(self, lignes: int = 5, colonnes: int = 9, pool=None, rng=None):
        self.lignes = lignes
        self.colonnes = colonnes

        # Pioche et RNG
        self.pool = pool or []      # liste de dicts pièce
        self.rng = rng or random.Random()       #générateur aléatoire

        # Grille init cases vides 
        self.grille: List[List[Piece]] = [
            [{"type": "vide", "couleur": "gris"} for _ in range(colonnes)]
            for _ in range(lignes)
        ]

        # Joueur indices de case
        self.joueur: Dict[str, int] = {"x": lignes - 1, "y": colonnes // 2}# indice bas(ligne-1 pour x) 

        # Portes (niveau 0 à 2)
        self.portes: Dict[Direction, int] = {"haut": 0, "bas": 0, "gauche": 0, "droite": 0}

        # Options proposées après ouverture d'une porte (3 pièces)
        self.options_courantes: List[Piece] = []

    # Déplacements
    def _delta(self, direction: Direction) -> Tuple[int, int]:
        return {
            "haut": (-1, 0),
            "bas": (1, 0),
            "gauche": (0, -1),
            "droite": (0, 1),
        }.get(direction, (0, 0)) # si direction non reconnue ça reste 

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

    # Porte
    def porte(self, direction: Direction) -> int:
        #Niveau de la porte (0,1,2)
        return int(self.portes.get(direction, 0))

    def peut_ouvrir(self, joueur: Dict[str, int], direction: Direction) -> bool:
        #on peut ouvrir si la case visée existe dans la grille
        dx, dy = self._delta(direction)
        nx, ny = joueur["x"] + dx, joueur["y"] + dy
        return self._dans_grille(nx, ny)

    def ouvrir(self, joueur: Dict[str, int], direction: Direction) -> None:
        #Ouvre la porte et prépare trois options de pièces via tirages.tirer_trois
        if not self.peut_ouvrir(joueur, direction):
            self.options_courantes = []
            return
        self.options_courantes = tirer_trois(self.pool, self.rng)

    #Placement d’une pièce
    def _case_devant(self, joueur: Dict[str, int], direction: Direction) -> Tuple[int, int]:
        dx, dy = self._delta(direction)
        return joueur["x"] + dx, joueur["y"] + dy

    def ok_placement(self, piece: Piece, x: int, y: int) -> bool:
        """Case dans la grille et encore 'vide'."""
        return self._dans_grille(x, y) and self.grille[x][y]["type"] == "vide"

    def poser_piece(self, x: int, y: int, piece: Piece) -> bool:
        #Place la pièce si possible. True si posée, sinon False
        if self.ok_placement(piece, x, y):
            self.grille[x][y] = {
                "type": str(piece.get("type", "inconnue")),
                "couleur": str(piece.get("couleur", "gris")),
                "cout_gemmes": int(piece.get("cout_gemmes", 0)),
            }
            return True
        return False

    def poser_devant(self, joueur: Dict[str, int], direction: Direction, piece: Piece) -> bool:
        #Place la pièce sur la case devant le joueur ; vide les options si succès
        x, y = self._case_devant(joueur, direction)
        ok = self.poser_piece(x, y, piece)
        if ok:
            self.options_courantes = []   # le choix est consommé
        return ok
