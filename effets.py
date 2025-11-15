# -*- coding: utf-8 -*-
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Callable
import random
from inventaire import Inventaire
from manoir import Manoir

Piece = Dict[str, object]

@dataclass
class Contexte:
    inventaire: Inventaire
    manoir: Manoir

def _norm(n: str) -> str:
    return "".join(ch.lower() for ch in str(n) if ch.isalnum())

# ---------------------------------------------------------------------
# Modificateurs globaux pour les loots (Veranda, Maid's Chamber, ...)
# ---------------------------------------------------------------------
LOOT_MODIFIERS = {
    "food": 1.0,
    "or": 1.0,
    "gemme": 1.0,
    "cle": 1.0,
    "de": 1.0,
    "permanent": 1.0,
}

def _mult_loot(key: str, factor: float):
    key = key.lower()
    if key in LOOT_MODIFIERS:
        LOOT_MODIFIERS[key] *= float(factor)


# ---------------------------------------------------------------------
# Effets immédiats quand on POSE la pièce
# ---------------------------------------------------------------------

# ---- Effets de base
def _effet_serre(piece: Piece, ctx: Contexte) -> str:
    ctx.inventaire.ajouter_pas(5)
    return "Serre : +5 pas"

def _effet_fournaise(piece: Piece, ctx: Contexte) -> str:
    """
    Fournaise : effet mixte
    - +1 dé
    - augmente un peu la probabilité de tirer des pièces rouges
    """
    inv = ctx.inventaire
    manoir = ctx.manoir
    inv.ajouter_des(1)
    manoir.ajuster_proba_couleur("rouge", 1.3)
    return "Fournaise : +1 dé et augmente la probabilité des pièces rouges"

def _effet_observatoire(piece: Piece, ctx: Contexte) -> str:
    ctx.inventaire.ajouter_cles(1)
    return "Observatoire : +1 clé"

# ---- Effets de magasins (pièces jaunes)
def _effet_kitchen1(piece: Piece, ctx: Contexte) -> str:
    """
    Kitchen1 (jaune) : magasin simple
    - Si le joueur a au moins 3 pièces d’or :
        -3 or, +10 pas
    - Sinon : rien
    """
    inv = ctx.inventaire
    if inv.or_ >= 3:
        inv.or_ -= 3
        inv.ajouter_pas(10)
        return "Kitchen : -3 or, +10 pas"
    return "Kitchen : pas assez d’or"

def _effet_laundryroom(piece: Piece, ctx: Contexte) -> str:
    """
    Laundry Room (jaune) :
    - Si le joueur a au moins 2 pièces d’or :
        -2 or, +1 clé
    - Sinon : rien
    """
    inv = ctx.inventaire
    if inv.or_ >= 2:
        inv.or_ -= 2
        inv.ajouter_cles(1)
        return "Laundry Room : -2 or, +1 clé"
    return "Laundry Room : pas assez d’or"

def _effet_mailroom(piece: Piece, ctx: Contexte) -> str:
    """
    Mail Room (jaune) :
    - Si le joueur a au moins 2 pièces d’or :
        -2 or, +1 dé
    - Sinon : rien
    """
    inv = ctx.inventaire
    if inv.or_ >= 2:
        inv.or_ -= 2
        inv.ajouter_des(1)
        return "Mail Room : -2 or, +1 dé"
    return "Mail Room : pas assez d’or"

def _effet_pantry(piece: Piece, ctx: Contexte) -> str:
    """
    Pantry (jaune) :
    - Si le joueur a au moins 1 pièce d’or :
        -1 or, +3 pas
    - Sinon : rien
    """
    inv = ctx.inventaire
    if inv.or_ >= 1:
        inv.or_ -= 1
        inv.ajouter_pas(3)
        return "Pantry : -1 or, +3 pas"
    return "Pantry : pas assez d’or"

# ---- Pièce qui donne / retire des ressources quand on la TIRE (Weight Room)
def _effet_weightroom(piece: Piece, ctx: Contexte) -> str:
    """
    Weight Room :
      - 50% : bon entraînement → +5 pas
      - 50% : blessure → -3 pas si possible
    """
    inv = ctx.inventaire
    r = random.random()
    if r < 0.5:
        inv.ajouter_pas(5)
        return "Weight Room : +5 pas (entraînement réussi)"
    else:
        if inv.depenser_pas(3):
            return "Weight Room : -3 pas (blessure)"
        return "Weight Room : rien (pas assez de pas pour en perdre)"

# ---- Pièces qui dispersent des ressources dans le manoir (Patio / Office)
def _effet_patio(piece: Piece, ctx: Contexte) -> str:
    """
    Patio :
      - disperse quelques pièces d'or dans 3 cases aléatoires du manoir.
    """
    m = ctx.manoir
    positions = []
    for _ in range(3):
        x = random.randrange(m.lignes)
        y = random.randrange(m.colonnes)
        positions.append((x, y))
    m.deposer_ressource(positions, "or", 1)
    return "Patio : disperse 3 pièces d'or dans le manoir"

def _effet_office(piece: Piece, ctx: Contexte) -> str:
    """
    Office :
      - disperse des gemmes dans 2 cases aléatoires.
    """
    m = ctx.manoir
    positions = []
    for _ in range(2):
        x = random.randrange(m.lignes)
        y = random.randrange(m.colonnes)
        positions.append((x, y))
    m.deposer_ressource(positions, "gemmes", 1)
    return "Office : disperse 2 gemmes cachées dans le manoir"

# ---- Pièces qui modifient la probabilité de TIRER certaines pièces
def _effet_greenhouse(piece: Piece, ctx: Contexte) -> str:
    """
    Greenhouse :
      - augmente la probabilité de tirer des pièces vertes
      - diminue un peu la proba des pièces rouges
    """
    m = ctx.manoir
    m.ajuster_proba_couleur("verte", 1.5)
    m.ajuster_proba_couleur("rouge", 0.8)
    return "Greenhouse : booste les pièces vertes, réduit un peu les rouges"

# (Fournaise est déjà gérée plus haut, en mixant +1 dé et proba rouges)

# ---- Pièces qui modifient la probabilité de trouver certains OBJETS (loots)
def _effet_veranda(piece: Piece, ctx: Contexte) -> str:
    """
    Veranda :
      - augmente les chances de trouver or et gemmes dans les loots.
    """
    _mult_loot("or", 1.4)
    _mult_loot("gemme", 1.6)
    return "Veranda : augmente les chances d'or et de gemmes dans les loots"

def _effet_maidschamber(piece: Piece, ctx: Contexte) -> str:
    """
    Maid's Chamber (pas forcément dans le pool, mais prêt si tu l'ajoutes) :
      - augmente un peu la nourriture
      - diminue légèrement les objets permanents
    """
    _mult_loot("food", 1.4)
    _mult_loot("permanent", 0.8)
    return "Maid's Chamber : plus de nourriture, moins d'objets permanents"

# ---- Pièces qui ajoutent des salles au catalogue (Chamber of Mirrors, Pool)
def _effet_chamberofmirrors(piece: Piece, ctx: Contexte) -> str:
    """
    Chamber of Mirrors :
      - ajoute quelques pièces supplémentaires (copies de salles existantes)
        à la pioche pour augmenter la variété.
    """
    m = ctx.manoir
    extras = [
        # copies de pièces existantes, pour ne pas nécessiter de nouvelles images
        {"type": "Passageway", "couleur": "orange", "rarete": 1, "cout_gemmes": 0,
         "portes": {"gauche", "droite"}},
        {"type": "Gymnasium", "couleur": "bleue", "rarete": 2, "cout_gemmes": 1,
         "portes": {"haut", "bas"}},
    ]
    m.ajouter_pieces_a_la_pioche(extras)
    return "Chamber of Mirrors : ajoute des pièces supplémentaires au catalogue"

def _effet_pool(piece: Piece, ctx: Contexte) -> str:
    """
    The Pool :
      - ajoute quelques pièces supplémentaires (copies) au catalogue.
    """
    m = ctx.manoir
    extras = [
        {"type": "Room_46", "couleur": "bleue", "rarete": 1, "cout_gemmes": 0,
         "portes": {"haut"}},
        {"type": "Greenhouse", "couleur": "verte", "rarete": 2, "cout_gemmes": 1,
         "portes": {"gauche", "droite"}},
    ]
    m.ajouter_pieces_a_la_pioche(extras)
    return "Pool : ajoute des pièces supplémentaires au catalogue"

# ---------------------------------------------------------------------
# Table des effets à la POSE de la pièce
# ---------------------------------------------------------------------
EFFETS_PAR_TYPE = {
    "serre": _effet_serre,
    "fournaise": _effet_fournaise,
    "observatoire": _effet_observatoire,

    # magasins (pièces jaunes de ton POOL)
    "kitchen1": _effet_kitchen1,
    "laundryroom": _effet_laundryroom,
    "mailroom": _effet_mailroom,
    "pantry": _effet_pantry,

    # donne / retire des ressources quand on tire la pièce
    "weightroom": _effet_weightroom,

    # dispersion de ressources
    "patio": _effet_patio,
    "office": _effet_office,

    # modification des probas de tirage de pièces
    "greenhouse": _effet_greenhouse,

    # modification des probas de loots
    "veranda": _effet_veranda,
    "maidschamber": _effet_maidschamber,

    # ajout de pièces au catalogue
    "chamberofmirrors": _effet_chamberofmirrors,
    "chamberofmirrors1": _effet_chamberofmirrors,
    "the_pool": _effet_pool,
}

def appliquer_effet(piece: Piece, ctx: Contexte) -> str:
    f = EFFETS_PAR_TYPE.get(_norm(piece.get("type", "")))
    return f(piece, ctx) if f else ""


# ---------------------------------------------------------------------
# Effets déclenchés lorsqu'on ENTRE dans certaines pièces
# ---------------------------------------------------------------------

def _effet_bedroom_entree(piece: Piece, ctx: Contexte) -> str:
    """
    Effet spécial de la pièce Bedroom lorsqu'on entre dedans.

    Exemple :
      - 40% : repos, on gagne des pas
      - 30% : mauvais rêve, on perd des pas si possible
      - 30% : on trouve une gemme
    """
    inv = ctx.inventaire
    r = random.random()
    if r < 0.40:
        inv.ajouter_pas(4)
        return "Bedroom : +4 pas (repos)"
    elif r < 0.70:
        if inv.depenser_pas(2):
            return "Bedroom : -2 pas (mauvais rêve)"
        else:
            return "Bedroom : rien (trop peu de pas pour en perdre)"
    else:
        inv.ajouter_gemmes(1)
        return "Bedroom : +1 gemme (objet trouvé)"

EFFETS_ENTREE_PAR_TYPE = {
    "bedroom": _effet_bedroom_entree,
    # tu peux ajouter d'autres pièces ici plus tard
}

def appliquer_effet_entree(piece: Piece, ctx: Contexte) -> str:
    """
    Applique l'effet lié AU FAIT D'ENTRER dans une pièce (si défini).
    """
    f = EFFETS_ENTREE_PAR_TYPE.get(_norm(piece.get("type", "")))
    return f(piece, ctx) if f else ""


# ---------------------------------------------------------------------
# Tirage d’objets à la pose d’une salle
# ---------------------------------------------------------------------
def _ajuster_probas_par_couleur(base, couleur: str):
    c = (couleur or "").strip().lower()
    p = dict(base)
    if c == "verte":
        p["gemme"] += 0.10; p["permanent"] += 0.05
    elif c == "violette":
        p["food"] += 0.15
    elif c == "jaune":
        p["or"] += 0.20
    elif c == "rouge":
        p["food"] -= 0.05; p["gemme"] -= 0.05
    return p

def _ajuster_probas_par_permanents(p, inv: Inventaire):
    if inv.detecteur_metaux:
        p["or"] += 0.10
        p["cle"] += 0.08
    if inv.patte_lapin:
        p["permanent"] += 0.06
    return p

def _choose(rng, table):
    total = sum(w for w, _ in table) or 1.0
    x = rng.random() * total
    acc = 0.0
    for w, act in table:
        acc += w
        if x <= acc:
            return act
    return table[-1][1]

def tirage_objets(piece: Piece, ctx: Contexte, rng=None) -> str:
    rng = rng or random.Random()
    inv = ctx.inventaire

    # probas de base
    p = {
        "rien": 0.40,
        "food": 0.25,
        "or": 0.15,
        "gemme": 0.10,
        "cle": 0.06,
        "de": 0.04,
        "permanent": 0.00
    }
    p = _ajuster_probas_par_couleur(p, str(piece.get("couleur", "")))
    p = _ajuster_probas_par_permanents(p, inv)

    # prise en compte des modifs globales (Veranda / Maid's Chamber, etc.)
    for key in ("food", "or", "gemme", "cle", "de", "permanent"):
        if key in p:
            p[key] *= LOOT_MODIFIERS.get(key, 1.0)

    total = sum(max(0.0, v) for v in p.values()) or 1.0
    for k in p:
        p[k] = max(0.0, p[k]) / total

    logs: List[str] = []

    def act_rien():
        pass

    def act_food():
        r = rng.random()
        if r < 0.30:
            inv.ajouter_pas(2); logs.append("+2 pas (pomme)")
        elif r < 0.55:
            inv.ajouter_pas(3); inv.ajouter_bananes(1); logs.append("+3 pas (banane)")
        elif r < 0.75:
            inv.ajouter_pas(10); logs.append("+10 pas (gâteau)")
        elif r < 0.92:
            inv.ajouter_pas(15); logs.append("+15 pas (sandwich)")
        else:
            inv.ajouter_pas(25); logs.append("+25 pas (repas)")

    def act_or():
        inv.ajouter_or(rng.randint(2, 6)); logs.append("+or")

    def act_gemme():
        inv.ajouter_gemmes(1); logs.append("+1 gemme")

    def act_cle():
        inv.ajouter_cles(1); logs.append("+1 clé")

    def act_de():
        inv.ajouter_des(1); logs.append("+1 dé")

    def act_perm():
        candidates = []
        if not inv.pelle: candidates.append("pelle")
        if not inv.marteau: candidates.append("marteau")
        if not inv.kit_crochetage: candidates.append("kit de crochetage")
        if not inv.detecteur_metaux: candidates.append("détecteur de métaux")
        if not inv.patte_lapin: candidates.append("patte de lapin")
        if not candidates:
            return
        nom = rng.choice(candidates)
        if inv.donner_permanent(nom):
            nice = {
                "pelle": "Shovel",
                "marteau": "Hammer",
                "kit de crochetage": "Lockpick Kit",
                "détecteur de métaux": "Metal Detector",
                "patte de lapin": "Lucky Rabbit's Foot"
            }[nom]
            logs.append(f"Objet permanent: {nice}")

    table = [
        (p["rien"], act_rien),
        (p["food"], act_food),
        (p["or"], act_or),
        (p["gemme"], act_gemme),
        (p["cle"], act_cle),
        (p["de"], act_de),
        (p["permanent"], act_perm),
    ]
    _choose(rng, table)()
    return " | ".join(logs)
