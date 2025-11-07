# -*- coding: utf-8 -*-
from typing import List, Dict, Tuple, Optional
import random
from tirages import tirer_trois

Direction = str
Piece = Dict[str, object]

OPPOSITE = {
    "haut": "bas",
    "bas": "haut",
    "gauche": "droite",
    "droite": "gauche"
}


class Manoir:
    def __init__(self, lignes: int = 5, colonnes: int = 9, pool=None, rng=None):
        self.lignes = lignes
        self.colonnes = colonnes
        self.pool = pool or []
        self.rng = rng or random.Random()

        # Grille initialisée avec des cases vides
        self.grille: List[List[Piece]] = [
            [{"type": "vide", "couleur": "gris", "portes": set()} for _ in range(colonnes)]
            for _ in range(lignes)
        ]

        # Coordonnées Entrance Hall / Antechamber
        self.entrance_x = lignes - 1
        self.entrance_y = colonnes // 2
        self.ante_x = 0
        self.ante_y = colonnes // 2

        # Placement fixe des deux pièces spéciales
        # Entrance : portes gauche/droite pour forcer le détour initial
        self._poser_fixe(
            self.entrance_x,
            self.entrance_y,
            "Entrance Hall",      # ou "Entrance_Hall" selon le nom de ton image
            "bleue",
            portes={"gauche", "droite", "haut"}
        )

        # Antechamber : porte vers le bas uniquement
        self._poser_fixe(
            self.ante_x,
            self.ante_y,
            "Antechamber",
            "bleue",
            portes={"bas"}
        )

        # Position du joueur (démarre sur l'Entrance Hall)
        self.joueur: Dict[str, int] = {
            "x": self.entrance_x,
            "y": self.entrance_y
        }

        # Options de pièces proposées après une ouverture
        self.options_courantes: List[Piece] = []

        # Contraintes de détour : on interdit de monter tout droit au début
        self.colonne_axe = self.ante_y
        self.detour_oblige = True  # il faut au moins un déplacement horizontal

        # ----- NOUVEAU : pioche finie -----
        # Copie modifiable du pool : on enlèvera les pièces au fur et à mesure.
        # (Par sécurité, on exclut les pièces fixes si elles étaient dans le pool.)
        self.pioche: List[Piece] = [
            p for p in self.pool
            if p.get("type") not in ("Entrance Hall", "Antechamber")
        ]

    # ---------- Outils internes ----------

    @staticmethod
    def _delta(direction: Direction) -> Tuple[int, int]:
        return {
            "haut": (-1, 0),
            "bas": (1, 0),
            "gauche": (0, -1),
            "droite": (0, 1),
        }.get(direction, (0, 0))

    def _dans_grille(self, x: int, y: int) -> bool:
        return 0 <= x < self.lignes and 0 <= y < self.colonnes

    def _piece(self, x: int, y: int) -> Piece:
        return self.grille[x][y]

    def _poser_fixe(self, x: int, y: int, type_: str, couleur: str, portes=None):
        self.grille[x][y] = {
            "type": type_,
            "couleur": couleur,
            "portes": set(portes or set())
        }

    def _case_devant(self, j: Dict[str, int], direction: Direction) -> Tuple[int, int]:
        dx, dy = self._delta(direction)
        return j["x"] + dx, j["y"] + dy

    def _est_bordure(self, x: int, y: int) -> bool:
        return (
            x == 0
            or y == 0
            or x == self.lignes - 1
            or y == self.colonnes - 1
        )

    # ---------- Règles de mouvement / ouverture ----------

    def _blocage_detour(self, j: Dict[str, int], direction: Direction) -> bool:
        """
        Bloque temporairement la montée tout droit tant que le détour
        horizontal imposé n’a pas été réalisé.
        """
        return (
            self.detour_oblige
            and direction == "haut"
            and j["y"] == self.colonne_axe
        )

    def peut_deplacer(self, j: Dict[str, int], direction: Direction) -> bool:
        if self._blocage_detour(j, direction):
            return False

        dx, dy = self._delta(direction)
        nx, ny = j["x"] + dx, j["y"] + dy

        if not self._dans_grille(nx, ny):
            return False

        p_src = self._piece(j["x"], j["y"])
        p_dst = self._piece(nx, ny)

        if p_dst["type"] == "vide":
            return False

        return (
            direction in p_src["portes"]
            and OPPOSITE[direction] in p_dst["portes"]
        )

    def deplacer(self, j: Dict[str, int], direction: Direction) -> bool:
        """
        Applique effectivement le déplacement si autorisé.
        """
        if self.peut_deplacer(j, direction):
            dx, dy = self._delta(direction)
            j["x"] += dx
            j["y"] += dy

            # Une fois qu'on a bougé horizontalement, on lève la contrainte de détour
            if self.detour_oblige and direction in ("gauche", "droite"):
                self.detour_oblige = False
            return True

        return False

    def peut_ouvrir(self, j: Dict[str, int], direction: Direction) -> bool:
        if self._blocage_detour(j, direction):
            return False

        x, y = self._case_devant(j, direction)

        if not self._dans_grille(x, y):
            return False

        if self._piece(x, y)["type"] != "vide":
            return False

        p_src = self._piece(j["x"], j["y"])
        return direction in p_src["portes"]

    def ouvrir(self, j: Dict[str, int], direction: Direction, gemmes_dispo: int) -> bool:
        """
        Tire et propose des pièces jouables dans la direction indiquée.
        Utilise maintenant la pioche (pièces restantes) au lieu du pool complet.
        """
        if not self.peut_ouvrir(j, direction):
            self.options_courantes = []
            return False

        # Si la pioche est vide, aucune nouvelle pièce possible
        if not self.pioche:
            self.options_courantes = []
            return False

        x, y = self._case_devant(j, direction)
        back_dir = OPPOSITE[direction]

        # On tire parmi les cartes restantes (self.pioche)
        self.options_courantes = tirer_trois(
            self.pioche,
            self.rng,
            back_dir=back_dir,
            sur_bordure=self._est_bordure(x, y),
            joueur_a_gemmes=(gemmes_dispo > 0),
        )

        return bool(self.options_courantes)

    # ---------- Placement de pièce ----------

    def ok_placement(self, x: int, y: int) -> bool:
        return self._dans_grille(x, y) and self._piece(x, y)["type"] == "vide"

    def poser_piece(
        self,
        x: int,
        y: int,
        piece: Piece,
        back_dir: Optional[Direction] = None
    ) -> bool:
        """
        Place définitivement une pièce choisie sur la grille.
        Vérifie la présence de la porte de retour back_dir si nécessaire.
        Enlève aussi cette pièce de la pioche pour éviter de la re-tirer.
        """
        if not self.ok_placement(x, y):
            return False

        portes = set(piece.get("portes", []))

        if back_dir and back_dir not in portes:
            return False

        self.grille[x][y] = {
            "type": str(piece.get("type", "Inconnue")),
            "couleur": str(piece.get("couleur", "gris")),
            "portes": portes,
        }

        # On supprime cette carte de la pioche si elle s'y trouve encore
        # (on ignore silencieusement si elle n'y est pas).
        try:
            self.pioche.remove(piece)
        except ValueError:
            pass

        self.options_courantes = []
        return True

    # ---------- Vérifs de blocage ----------

    def _voisins(self, x: int, y: int):
        """
        Génère les cases voisines valides (direction, nx, ny).
        """
        for d, (dx, dy) in {
            "haut": (-1, 0),
            "bas": (1, 0),
            "gauche": (0, -1),
            "droite": (0, 1),
        }.items():
            nx, ny = x + dx, y + dy
            if self._dans_grille(nx, ny):
                yield d, nx, ny

    def aucun_coup_possible(self, j: Dict[str, int]) -> bool:
        """
        Test local :
        - aucun déplacement possible depuis la case du joueur
        - aucune ouverture possible depuis cette même case
        Utilisé dans la condition de défaite.
        """
        # essayer de bouger
        for d, _, _ in self._voisins(j["x"], j["y"]):
            if self.peut_deplacer(j, d):
                return False

        # essayer d’ouvrir
        for d, _, _ in self._voisins(j["x"], j["y"]):
            if self.peut_ouvrir(j, d):
                return False

        return True

    # ---------- Objectif ----------

    def est_antechamber(self, x: int, y: int) -> bool:
        return (x, y) == (self.ante_x, self.ante_y)
