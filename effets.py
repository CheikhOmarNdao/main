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

def _effet_pomme(piece: Piece, ctx: Contexte) -> str:
    ctx.inventaire.ajouter_pas(2)
    return "Pomme : +2 pas"

def _effet_banane(piece: Piece, ctx: Contexte) -> str:
    ctx.inventaire.ajouter_pas(3)
    return "Banane : +3 pas"

def _effet_sandwich(piece: Piece, ctx: Contexte) -> str:
    ctx.inventaire.ajouter_pas(10)
    return "Sandwich : +10 pas"

def _effet_salade(piece: Piece, ctx: Contexte) -> str:
    ctx.inventaire.ajouter_pas(5)
    return "Salade : +5 pas"

def _effet_repas(piece: Piece, ctx: Contexte) -> str:
    ctx.inventaire.ajouter_pas(25)
    return "Repas : +25 pas"

def _effet_coffre(piece: Piece, ctx: Contexte) -> str:
    if ctx.inventaire.depenser_cles(1):
        ctx.inventaire.ajouter_gemmes(1)
        ctx.inventaire.ajouter_pas(5)
        return "Coffre ouvert : +1 gemme, +5 pas"
    return "Coffre fermé : clé manquante"

def _effet_endroitacreuser(piece: Piece, ctx: Contexte) -> str:
    if "pelle" in ctx.inventaire.permanents:
        ctx.inventaire.ajouter_pas(3)
        return "Creusé : +3 pas"
    return "Impossible de creuser : pelle manquante"

def _effet_casier(piece: Piece, ctx: Contexte) -> str:
    if ctx.inventaire.depenser_cles(1):
        ctx.inventaire.ajouter_pas(4)
        return "Casier ouvert : +4 pas"
    return "Casier fermé : clé manquante"

# mapping  (clé = nom normalisé en minuscules)
# EFFETS_PAR_TYPE = {
#     "serre": _effet_serre,
#     "fournaise": _effet_fournaise,
#     "observatoire": _effet_observatoire,
# }
def _effet_casier(piece: Piece, ctx: Contexte) -> str:
    if ctx.inventaire.depenser_cles(1):
        ctx.inventaire.ajouter_pas(4)
        return "Casier ouvert avec clé : +4 pas"
    return "Casier fermé : clé manquante"

EFFETS_PAR_TYPE = {
    "serre": _effet_serre,
    "fournaise": _effet_fournaise,
    "observatoire": _effet_observatoire,
    "pomme": _effet_pomme,
    "banane": _effet_banane,
    "sandwich": _effet_sandwich,
    "salade": _effet_salade,
    "repas": _effet_repas,
    "coffre": _effet_coffre,
    "endroitacreuser": _effet_endroitacreuser,
    "casier": _effet_casier,
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
