# -*- coding: utf-8 -*-
"""
manoir
- Grille 5x9 par défaut : chaque case est un dictionnaire {"type": str, "couleur": str}
- Portes autour du joueur (niveaux 0/1/2)
- Déplacements, ouverture (prépare 3 options), placement d une pièce
"""

from typing import List, Dict, Tuple

Direction = str       # haut,bas,gauche,droite
Piece = Dict[str, object]       # dict represente 1 pièce

class Manoir:
    """Pour grille,portes et les actions de base"""

    def __init__(self, lignes: int = 5, colonnes: int = 9):
        self.lignes = lignes
        self.colonnes = colonnes

        # Grille initiale :cases vides
        self.grille: List[List[Piece]] = [
            [{"type": "vide", "couleur": "gris"} for _ in range(colonnes)] #la Vue lit 'type' et 'couleur'
            for _ in range(lignes)
        ]

        # Joueur : indices de case
        self.joueur: Dict[str, int] = {"x": lignes - 1, "y": colonnes // 2}#derniere ligne en bas x=ligne-1

        # Portes autour du joueur (niveaux 0à2). MVP : suivi local autour du joueur
        self.portes: Dict[Direction, int] = {"haut": 0, "bas": 0, "gauche": 0, "droite": 0}

        # Options proposées après une ouverture de porte (3 pièces)
        self.options_courantes: List[Piece] = []

    # Déplacements

    def _delta(self, direction: Direction) -> Tuple[int, int]:
        return {
            "haut": (-1, 0),
            "bas": (1, 0),
            "gauche": (0, -1),
            "droite": (0, 1),
        }.get(direction, (0, 0)) #si direction non connue ça reste 

    def _dans_grille(self, x: int, y: int) -> bool:
        return 0 <= x < self.lignes and 0 <= y < self.colonnes #pour vérifier si on est dans la grille
    # pour voir si le joueur peut se déplacer ds 1 direction donné on fait:
    def peut_deplacer(self, joueur: Dict[str, int], direction: Direction) -> bool:
        dx, dy = self._delta(direction)
        nx, ny = joueur["x"] + dx, joueur["y"] + dy
        return self._dans_grille(nx, ny)
    
    def deplacer(self, joueur: Dict[str, int], direction: Direction) -> None:
        if self.peut_deplacer(joueur, direction): # s'il peut se deplacer on fait 
            dx, dy = self._delta(direction)
            joueur["x"] += dx
            joueur["y"] += dy

    # Portes
    
    def porte(self, direction: Direction) -> int:
        return int(self.portes.get(direction, 0)) #Retourne le niveau de la porte ds la direction donnée

    def peut_ouvrir(self, joueur: Dict[str, int], direction: Direction) -> bool: #on peut ouvrir si la case visée existe dans la grille
        dx, dy = self._delta(direction)
        nx, ny = joueur["x"] + dx, joueur["y"] + dy
        return self._dans_grille(nx, ny)

    def ouvrir(self, joueur: Dict[str, int], direction: Direction) -> None:
       # Ouvre la porte et prépare trois options de pièces.  
        if not self.peut_ouvrir(joueur, direction):
            self.options_courantes = []
            return
        #les 3 pieces 
        self.options_courantes = [
            {"type": "Serre",         "couleur": "verte",   "cout_gemmes": 0},
            {"type": "Fournaise",     "couleur": "orange",  "cout_gemmes": 1},
            {"type": "Observatoire",  "couleur": "violette","cout_gemmes": 2},
        ]


    # Placement d’une pièce
 
    def _case_devant(self, joueur: Dict[str, int], direction: Direction) -> Tuple[int, int]:
        dx, dy = self._delta(direction)
        return joueur["x"] + dx, joueur["y"] + dy

    def ok_placement(self, piece: Piece, x: int, y: int) -> bool:
        #il faut la case soitdans la grille et encore vide
        return self._dans_grille(x, y) and self.grille[x][y]["type"] == "vide"

    def poser_piece(self, x: int, y: int, piece: Piece) -> bool:
        """Place la pièce si possible. Retourne True si posée, False sinon."""
        if self.ok_placement(piece, x, y):
            self.grille[x][y] = {
                "type": str(piece.get("type", "inconnue")),
                "couleur": str(piece.get("couleur", "gris")),
                "cout_gemmes": int(piece.get("cout_gemmes", 0)),
            }
            return True
        return False

    def poser_devant(self, joueur: Dict[str, int], direction: Direction, piece: Piece) -> bool:
        #Place la pièce sur la case devant le joueur dans la direction donnée
         x, y = self._case_devant(joueur, direction)
         ok = self.poser_piece(x, y, piece)
         if ok:
            self.options_courantes = []   # pour qire que le choix est consommé
         return ok
    
   