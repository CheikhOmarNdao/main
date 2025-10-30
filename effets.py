# -*- coding: utf-8 -*-
# effets.py — Application des effets de pièce (MVP)

from __future__ import annotations
from typing import Dict
from dataclasses import dataclass

from inventaire import Inventaire
from manoir import Manoir

Piece = Dict[str, object]

@dataclass
class Contexte:
    inventaire: Inventaire
    manoir: Manoir


#  règles d'effet
def _effet_serre(piece: Piece, ctx: Contexte) -> str:    # Exple les pièces "vertes" donnent des pas 
    ctx.inventaire.ajouter_pas(5)
    return "Serre : +5 pas"

def _effet_fournaise(piece: Piece, ctx: Contexte) -> str:  # Exple fournaise donne 1 dé
    ctx.inventaire.ajouter_des(1)
    return "Fournaise : +1 dé"

def _effet_observatoire(piece: Piece, ctx: Contexte) -> str: # Exple observatoire donne 1 clé
    ctx.inventaire.ajouter_cles(1)
    return "Observatoire : +1 clé"


# mapping  (clé = nom normalisé en minuscules)
EFFETS_PAR_TYPE = {
    "serre": _effet_serre,
    "fournaise": _effet_fournaise,
    "observatoire": _effet_observatoire,
}


def _norm(n: str) -> str:
    """Normalise un nom de type pour lookup (minuscule / alnum)."""
    return "".join(ch.lower() for ch in str(n) if ch.isalnum())


# API
def appliquer_effet(piece: Piece, ctx: Contexte) -> str:
    """
    Applique l'effet associé au 'type' de la pièce. Retourne un petit résumé.
    Si aucun effet n'est défini, ne fait rien (MVP).
    """
    t = piece.get("type", "")
    f = EFFETS_PAR_TYPE.get(_norm(t))
    if f is None:
        return f"Aucun effet défini pour '{t}'"
    return f(piece, ctx)
