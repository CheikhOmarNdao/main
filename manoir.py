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

        # ----- NOUVEAU : niveaux de verrouillage des portes -----
        # Clé : (x, y, direction) -> niveau 0, 1 ou 2
        self.verrous: Dict[Tuple[int, int, Direction], int] = {}

        # ----- NOUVEAU : modificateurs de probas de tirage de pièces -----
        # utilisés par des effets de pièces (Greenhouse, Furnace, etc.)
        # facteur multiplicatif (1.0 = pas de changement)
        self.modif_proba_couleurs: Dict[str, float] = {}
        self.modif_proba_types: Dict[str, float] = {}

        # ----- NOUVEAU : ressources cachées dans certaines cases -----
        # (effet Patio / Office : ressources dispersées)
        # clé : (x, y) -> dict {"or": n, "gemmes": n, "pas": n, ...}
        self.ressources_cachees: Dict[Tuple[int, int], Dict[str, int]] = {}

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

    def deplacer(self, j: Dict[str, int], direction: Direction, inventaire=None) -> bool:
        """
        Applique effectivement le déplacement si autorisé.
        Si un inventaire est fourni, tient compte du niveau de verrouillage
        de la porte et du kit de crochetage / des clés.
        """
        # D’abord, on vérifie qu'il y a bien une porte des deux côtés
        if not self.peut_deplacer(j, direction):
            return False

        # Gestion des niveaux de verrouillage si on a accès à l'inventaire
        if inventaire is not None:
            niveau = self.niveau_verrou(j["x"], j["y"], direction)

            if niveau == 1:
                # Porte niveau 1 : le kit de crochetage permet de passer gratuitement
                if not getattr(inventaire, "kit_crochetage", False):
                    # Sans kit, il faut une clé
                    if not inventaire.depenser_cles(1):
                        return False
            elif niveau == 2:
                # Porte niveau 2 : le kit ne marche pas, il faut une clé
                if not inventaire.depenser_cles(1):
                    return False
            # niveau 0 : rien de spécial

        # Si on arrive ici, on peut effectivement se déplacer
        dx, dy = self._delta(direction)
        j["x"] += dx
        j["y"] += dy

        # Une fois qu'on a bougé horizontalement, on lève la contrainte de détour
        if self.detour_oblige and direction in ("gauche", "droite"):
            self.detour_oblige = False
        return True

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

    def ouvrir(self, j: Dict[str, int], direction: Direction, ressources_dispo: int) -> bool:
        """
        Tire et propose des pièces jouables dans la direction indiquée.
        Utilise maintenant la pioche (pièces restantes) au lieu du pool complet.

        `ressources_dispo` peut représenter, par exemple, le total
        (gemmes + clés) côté inventaire, pour déterminer si l'on
        autorise l'apparition de pièces coûteuses.
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
            # Le joueur a des ressources (gemmes OU clés) pour acheter des pièces chères
            joueur_a_gemmes=(ressources_dispo > 0),
            # Modificateurs de probas de tirage (effets spéciaux)
            modif_couleurs=self.modif_proba_couleurs,
            modif_types=self.modif_proba_types,
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

    # ---------- Niveaux de verrouillage ----------

    def _tirer_niveau_verrou(self, ligne: int) -> int:
        """
        Tire un niveau de verrou (0, 1, 2) en fonction de la ligne dans le manoir.
        - ligne de l'Entrance Hall : toujours 0
        - ligne de l'Antechamber : toujours 2
        - lignes intermédiaires : mélange 0/1/2, plus de verrouillage en s'approchant de l'Antechamber.
        """
        if ligne == self.entrance_x:
            return 0
        if ligne == self.ante_x:
            return 2

        # Normalisation entre 0 (près de l'Entrance) et 1 (près de l'Antechamber)
        denom = max(1, self.entrance_x - self.ante_x)
        ratio = (self.entrance_x - ligne) / denom  # 0 près Entrance, 1 près Antechamber

        # Exemple de paliers simples en fonction de ratio
        if ratio < 1/3:
            # zone assez proche de l'Entrance → plutôt niveau 0
            probs = (0.7, 0.3, 0.0)   # (p0, p1, p2)
        elif ratio < 2/3:
            # zone intermédiaire
            probs = (0.3, 0.5, 0.2)
        else:
            # zone proche de l'Antechamber → plutôt niveau 2
            probs = (0.1, 0.4, 0.5)

        r = self.rng.random()
        p0, p1, p2 = probs
        if r < p0:
            return 0
        if r < p0 + p1:
            return 1
        return 2

    def niveau_verrou(self, x: int, y: int, direction: Direction) -> int:
        """
        Renvoie (et initialise au besoin) le niveau de verrouillage de la porte
        située à partir de (x, y) dans 'direction'.

        Le niveau est commun aux deux côtés de la porte.
        """
        key = (x, y, direction)
        if key in self.verrous:
            return self.verrous[key]

        dx, dy = self._delta(direction)
        nx, ny = x + dx, y + dy

        if not self._dans_grille(nx, ny):
            # Hors de la grille : on considère déverrouillé par sécurité
            self.verrous[key] = 0
            return 0

        # On choisit une ligne représentative pour le tirage :
        # la plus "haute" des deux (plus proche de l'Antechamber)
        ligne_ref = min(x, nx)
        niveau = self._tirer_niveau_verrou(ligne_ref)

        # On enregistre le niveau pour les deux sens de la porte
        self.verrous[(x, y, direction)] = niveau
        self.verrous[(nx, ny, OPPOSITE[direction])] = niveau

        return niveau

    # ---------- Modificateurs de probas de tirage ----------

    def ajuster_proba_couleur(self, couleur: str, facteur: float):
        """Multiplie la probabilité de tirer des pièces d'une certaine couleur."""
        c = (couleur or "").strip().lower()
        if not c:
            return
        self.modif_proba_couleurs[c] = self.modif_proba_couleurs.get(c, 1.0) * float(facteur)

    def ajuster_proba_type(self, type_piece: str, facteur: float):
        """Multiplie la probabilité de tirer un certain type de pièce."""
        t = (type_piece or "").strip().lower()
        if not t:
            return
        self.modif_proba_types[t] = self.modif_proba_types.get(t, 1.0) * float(facteur)

    # ---------- Gestion de la pioche (ajout de nouvelles pièces) ----------

    def ajouter_pieces_a_la_pioche(self, nouvelles_pieces: List[Piece]):
        """
        Ajoute des pièces supplémentaires au catalogue/pioche.
        Utilisé par des pièces spéciales (Chamber of Mirrors, Pool, ...).
        """
        for p in nouvelles_pieces or []:
            # On stocke une copie pour éviter les effets de bord
            self.pioche.append(dict(p))

    # ---------- Ressources cachées / dispersées ----------

    def deposer_ressource(self, positions: List[Tuple[int, int]], type_ressource: str, quantite: int):
        """
        Dépose une ressource (or, gemmes, pas, ...) sur plusieurs cases.
        Utilisé par des pièces comme Patio / Office.
        """
        t = (type_ressource or "").strip().lower()
        if not t or quantite == 0:
            return
        for (x, y) in positions:
            if not self._dans_grille(x, y):
                continue
            d = self.ressources_cachees.setdefault((x, y), {})
            d[t] = d.get(t, 0) + int(quantite)

    def ramasser_ressources_case(self, x: int, y: int, inventaire) -> str:
        """
        Si des ressources sont cachées sur (x, y), les donne à l'inventaire
        et renvoie un petit message de log. Sinon, renvoie "".
        """
        data = self.ressources_cachees.pop((x, y), None)
        if not data:
            return ""

        logs = []
        if "or" in data and data["or"] > 0:
            inventaire.ajouter_or(data["or"])
            logs.append(f"+{data['or']} or caché")
        if "gemmes" in data and data["gemmes"] > 0:
            inventaire.ajouter_gemmes(data["gemmes"])
            logs.append(f"+{data['gemmes']} gemme(s) cachée(s)")
        if "pas" in data and data["pas"] > 0:
            inventaire.ajouter_pas(data["pas"])
            logs.append(f"+{data['pas']} pas cachés")
        if "cles" in data and data["cles"] > 0:
            inventaire.ajouter_cles(data["cles"])
            logs.append(f"+{data['cles']} clé(s) cachée(s)")
        if "des" in data and data["des"] > 0:
            inventaire.ajouter_des(data["des"])
            logs.append(f"+{data['des']} dé(s) caché(s)")

        return " | ".join(logs)
