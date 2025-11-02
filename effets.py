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

# ---- Effets immédiats de quelques pièces (démo)
def _effet_serre(piece: Piece, ctx: Contexte) -> str:
    ctx.inventaire.ajouter_pas(5); return "Serre : +5 pas"

def _effet_fournaise(piece: Piece, ctx: Contexte) -> str:
    ctx.inventaire.ajouter_des(1); return "Fournaise : +1 dé"

def _effet_observatoire(piece: Piece, ctx: Contexte) -> str:
    ctx.inventaire.ajouter_cles(1); return "Observatoire : +1 clé"

EFFETS_PAR_TYPE = {
    "serre": _effet_serre,
    "fournaise": _effet_fournaise,
    "observatoire": _effet_observatoire,
}

def appliquer_effet(piece: Piece, ctx: Contexte) -> str:
    f = EFFETS_PAR_TYPE.get(_norm(piece.get("type", "")))
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
    if inv.detecteur_metaux: p["or"] += 0.10; p["cle"] += 0.08
    if inv.patte_lapin: p["permanent"] += 0.06
    return p

def _choose(rng, table):
    total = sum(w for w,_ in table) or 1.0
    x = rng.random() * total; acc = 0.0
    for w, act in table:
        acc += w
        if x <= acc: return act
    return table[-1][1]

def tirage_objets(piece: Piece, ctx: Contexte, rng=None) -> str:
    rng = rng or random.Random()
    inv = ctx.inventaire

    # probas de base
    p = {"rien":0.40, "food":0.25, "or":0.15, "gemme":0.10, "cle":0.06, "de":0.04, "permanent":0.00}
    p = _ajuster_probas_par_couleur(p, str(piece.get("couleur", "")))
    p = _ajuster_probas_par_permanents(p, inv)

    total = sum(max(0.0,v) for v in p.values()) or 1.0
    for k in p: p[k] = max(0.0, p[k]) / total

    logs: List[str] = []

    def act_rien(): pass

    def act_food():
        r = rng.random()
        if r < 0.30: inv.ajouter_pas(2); logs.append("+2 pas (pomme)")
        elif r < 0.55: inv.ajouter_pas(3); inv.ajouter_bananes(1); logs.append("+3 pas (banane)")
        elif r < 0.75: inv.ajouter_pas(10); logs.append("+10 pas (gâteau)")
        elif r < 0.92: inv.ajouter_pas(15); logs.append("+15 pas (sandwich)")
        else: inv.ajouter_pas(25); logs.append("+25 pas (repas)")

    def act_or(): inv.ajouter_or(rng.randint(2, 6)); logs.append("+or")
    def act_gemme(): inv.ajouter_gemmes(1); logs.append("+1 gemme")
    def act_cle(): inv.ajouter_cles(1); logs.append("+1 clé")
    def act_de(): inv.ajouter_des(1); logs.append("+1 dé")

    def act_perm():
        candidates = []
        if not inv.pelle: candidates.append("pelle")
        if not inv.marteau: candidates.append("marteau")
        if not inv.kit_crochetage: candidates.append("kit de crochetage")
        if not inv.detecteur_metaux: candidates.append("détecteur de métaux")
        if not inv.patte_lapin: candidates.append("patte de lapin")
        if not candidates: return
        nom = rng.choice(candidates)
        if inv.donner_permanent(nom):
            nice = {"pelle":"Shovel","marteau":"Hammer","kit de crochetage":"Lockpick Kit",
                    "détecteur de métaux":"Metal Detector","patte de lapin":"Lucky Rabbit's Foot"}[nom]
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
