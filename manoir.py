# -*- coding: utf-8 -*-
from typing import List, Dict, Tuple, Optional
import random
from tirages import tirer_trois

Direction = str
Piece = Dict[str, object]

OPPOSITE = {"haut": "bas", "bas": "haut", "gauche": "droite", "droite": "gauche"}

class Manoir:
    def __init__(self, lignes: int = 5, colonnes: int = 9, pool=None, rng=None):
        self.lignes = lignes
        self.colonnes = colonnes
        self.pool = pool or []
        self.rng = rng or random.Random()

        self.grille: List[List[Piece]] = [
            [{"type": "vide", "couleur": "gris", "portes": set()} for _ in range(colonnes)]
            for _ in range(lignes)
        ]

        self.entrance_x = lignes - 1
        self.entrance_y = colonnes // 2
        self.ante_x = 0
        self.ante_y = colonnes // 2

        # Entrance : gauche/droite pour forcer le détour initial
        self._poser_fixe(self.entrance_x, self.entrance_y, "Entrance Hall", "bleue", portes={"gauche", "droite"})
        self._poser_fixe(self.ante_x, self.ante_y, "Antechamber", "bleue", portes={"bas"})

        self.joueur: Dict[str, int] = {"x": self.entrance_x, "y": self.entrance_y}
        self.options_courantes: List[Piece] = []

        self.colonne_axe = self.ante_y
        self.detour_oblige = True  # au moins un déplacement horizontal

    # --- outils
    @staticmethod
    def _delta(direction: Direction) -> Tuple[int, int]:
        return {"haut": (-1, 0), "bas": (1, 0), "gauche": (0, -1), "droite": (0, 1)}.get(direction, (0, 0))

    def _dans_grille(self, x: int, y: int) -> bool:
        return 0 <= x < self.lignes and 0 <= y < self.colonnes

    def _piece(self, x: int, y: int) -> Piece:
        return self.grille[x][y]

    def _poser_fixe(self, x: int, y: int, type_: str, couleur: str, portes=None):
        self.grille[x][y] = {"type": type_, "couleur": couleur, "portes": set(portes or set())}

    def _case_devant(self, j: Dict[str, int], direction: Direction) -> Tuple[int, int]:
        dx, dy = self._delta(direction)
        return j["x"] + dx, j["y"] + dy

    def _est_bordure(self, x, y) -> bool:
        return x == 0 or y == 0 or x == self.lignes-1 or y == self.colonnes-1

    # --- règles
    def _blocage_detour(self, j: Dict[str, int], direction: Direction) -> bool:
        return self.detour_oblige and direction == "haut" and j["y"] == self.colonne_axe

    def peut_deplacer(self, j: Dict[str, int], direction: Direction) -> bool:
        if self._blocage_detour(j, direction): return False
        dx, dy = self._delta(direction)
        nx, ny = j["x"] + dx, j["y"] + dy
        if not self._dans_grille(nx, ny): return False
        p_src = self._piece(j["x"], j["y"])
        p_dst = self._piece(nx, ny)
        if p_dst["type"] == "vide": return False
        return (direction in p_src["portes"]) and (OPPOSITE[direction] in p_dst["portes"])

    def deplacer(self, j: Dict[str, int], direction: Direction) -> bool:
        if self.peut_deplacer(j, direction):
            dx, dy = self._delta(direction)
            j["x"] += dx; j["y"] += dy
            if self.detour_oblige and direction in ("gauche", "droite"):
                self.detour_oblige = False
            return True
        return False

    def peut_ouvrir(self, j: Dict[str, int], direction: Direction) -> bool:
        if self._blocage_detour(j, direction): return False
        x, y = self._case_devant(j, direction)
        if not self._dans_grille(x, y): return False
        if self._piece(x, y)["type"] != "vide": return False
        p_src = self._piece(j["x"], j["y"])
        return direction in p_src["portes"]

    def ouvrir(self, j: Dict[str, int], direction: Direction, gemmes_dispo: int) -> bool:
        if not self.peut_ouvrir(j, direction):
            self.options_courantes = []; return False
        x, y = self._case_devant(j, direction)
        back_dir = OPPOSITE[direction]
        self.options_courantes = tirer_trois(
            self.pool, self.rng,
            back_dir=back_dir,
            sur_bordure=self._est_bordure(x, y),
            joueur_a_gemmes=(gemmes_dispo > 0)
        )
        return bool(self.options_courantes)

    def ok_placement(self, x: int, y: int) -> bool:
        return self._dans_grille(x, y) and self._piece(x, y)["type"] == "vide"

    def poser_piece(self, x: int, y: int, piece: Piece, back_dir: Optional[Direction] = None) -> bool:
        if not self.ok_placement(x, y): return False
        portes = set(piece.get("portes", []))
        if back_dir and back_dir not in portes: return False
        self.grille[x][y] = {
            "type": str(piece.get("type", "Inconnue")),
            "couleur": str(piece.get("couleur", "gris")),
            "portes": portes
        }
        self.options_courantes = []
        return True

    # état blocage
    def _voisins(self, x, y):
        for d,(dx,dy) in {"haut":(-1,0),"bas":(1,0),"gauche":(0,-1),"droite":(0,1)}.items():
            nx, ny = x+dx, y+dy
            if self._dans_grille(nx, ny): yield d, nx, ny

    def aucun_coup_possible(self, j: Dict[str, int]) -> bool:
        for d, _, _ in self._voisins(j["x"], j["y"]):
            if self.peut_deplacer(j, d): return False
        for d, _, _ in self._voisins(j["x"], j["y"]):
            if self.peut_ouvrir(j, d): return False
        return True

    def est_antechamber(self, x, y) -> bool:
        return (x, y) == (self.ante_x, self.ante_y)
