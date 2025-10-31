# 


# -*- coding: utf-8 -*-
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

# --- Effets directs ---
def _effet_vault(piece, ctx): ctx.inventaire.ajouter_pieces(40); return "Vault : +40 pièces"
def _effet_gymnasium(piece, ctx): ctx.inventaire.ajouter_des(1); return "Gymnasium : +1 dé"
def _effet_weightroom(piece, ctx): ctx.inventaire.ajouter_des(1); return "Weight Room : +1 dé"
def _effet_security(piece, ctx): ctx.inventaire.ajouter_cles(1); return "Security : +1 clé"
def _effet_greenhouse(piece, ctx): ctx.inventaire.ajouter_gemmes(1); ctx.inventaire.bonus_jardin += 1; return "Greenhouse : +1 gemme, boost jardin"
def _effet_foyer(piece, ctx): ctx.inventaire.ajouter_gemmes(1); return "Foyer : +1 gemme"
def _effet_patioroom(piece, ctx): ctx.inventaire.dispersion_active = True; return "Patio : dispersion activée"
def _effet_veranda(piece, ctx): ctx.inventaire.bonus_vertes += 1; return "Veranda : boost pièces vertes"
def _effet_chambermirrors(piece, ctx): ctx.inventaire.catalogue_bonus += 1; return "Chamber of Mirrors : catalogue enrichi"
def _effet_nursery(piece, ctx): ctx.inventaire.ajouter_pas(5); ctx.inventaire.bonus_objets += 1; return "Nursery : +5 pas, boost objets"
def _effet_bedroom(piece, ctx): ctx.inventaire.ajouter_pas(10); return "Bedroom : +10 pas"
def _effet_kitchen(piece, ctx): ctx.inventaire.ajouter_pas(5); return "Kitchen : +5 pas"
def _effet_morningroom(piece, ctx): ctx.inventaire.ajouter_pas(5); return "Morning Room : +5 pas"
def _effet_seriessecret(piece, ctx): ctx.inventaire.retirer_gemmes(1); return "Series Secret : -1 gemme"
def _effet_attic(piece, ctx): ctx.inventaire.retirer_pas(2); return "Attic : -2 pas"
def _effet_laundry(piece, ctx): ctx.inventaire.retirer_pas(2); return "Laundry Room : -2 pas"
def _effet_closet(piece, ctx): ctx.inventaire.retirer_pas(1); return "Closet : -1 pas"
def _effet_lavatory(piece, ctx): ctx.inventaire.retirer_pas(1); return "Lavatory : -1 pas"
def _effet_utilitycloset(piece, ctx): ctx.inventaire.retirer_pas(1); return "Utility Closet : -1 pas"
def _effet_salon(piece, ctx): ctx.inventaire.ajouter_pas(3); return "Salon : +3 pas"
def _effet_parlor(piece, ctx): ctx.inventaire.ajouter_pas(3); return "Parlor : +3 pas"
def _effet_library(piece, ctx): ctx.inventaire.ajouter_pas(2); return "Library : +2 pas"
def _effet_study(piece, ctx): ctx.inventaire.ajouter_pas(2); return "Study : +2 pas"
def _effet_gallery(piece, ctx): return "Gallery : pas d'effet direct"
def _effet_fresco(piece, ctx): return "Fresco : pas d'effet direct"
def _effet_office(piece, ctx): ctx.inventaire.dispersion_active = True; return "Office : dispersion activée"
def _effet_thearms(piece, ctx): ctx.inventaire.retirer_pas(2); return "The Arms : -2 pas"
def _effet_thepool(piece, ctx): ctx.inventaire.catalogue_bonus += 1; return "The Pool : catalogue enrichi"
def _effet_trophyroom(piece, ctx): ctx.inventaire.ajouter_pieces(10); return "Trophy Room : +10 pièces"
def _effet_room46(piece, ctx): return "Room 46 : neutre"
def _effet_passageway(piece, ctx): return "Passageway : couloir"
def _effet_passageroom(piece, ctx): return "Passage Room : couloir"
def _effet_seriesgarage(piece, ctx): return "Series Garage : couloir"
def _effet_garage(piece, ctx): return "Garage : couloir"
def _effet_mallroom(piece, ctx): return "Mall Room : magasin (à implémenter)"
def _effet_entrancehall(piece, ctx): return "Entrance Hall : départ"
def _effet_antechamber(piece, ctx): return "Antechamber : arrivée"

# --- Objets alimentaires ---
def _effet_banana(piece, ctx): ctx.inventaire.ajouter_pas(3); return "Banane : +3 pas"
def _effet_pomme(piece, ctx): ctx.inventaire.ajouter_pas(2); return "Pomme : +2 pas"
def _effet_sandwich(piece, ctx): ctx.inventaire.ajouter_pas(10); return "Sandwich : +10 pas"
def _effet_repas(piece, ctx): ctx.inventaire.ajouter_pas(25); return "Repas : +25 pas"

# --- Mapping complet ---
EFFETS_PAR_TYPE = {
    "vault": _effet_vault, "vault1": _effet_vault, "vault2": _effet_vault,
    "gymnasium": _effet_gymnasium, "weightroom": _effet_weightroom,
    "security": _effet_security, "greenhouse": _effet_greenhouse,
    "foyer": _effet_foyer, "patio": _effet_patioroom, "veranda": _effet_veranda,
    "chamberofmirrors": _effet_chambermirrors, "chamberofmirrors1": _effet_chambermirrors, "chamberofmirrors2": _effet_chambermirrors,
    "nursery": _effet_nursery, "bedroom": _effet_bedroom,
    "kitchen": _effet_kitchen, "kitchen1": _effet_kitchen, "kitchen2": _effet_kitchen,
    "morningroom": _effet_morningroom, "seriessecret": _effet_seriessecret,
    "attic": _effet_attic, "laundryroom": _effet_laundry,
    "closet": _effet_closet, "lavatory1": _effet_lavatory, "lavatory2": _effet_lavatory,
    "utilitycloset": _effet_utilitycloset, "utilitycloset1": _effet_utilitycloset,
    "salon": _effet_salon, "parlor": _effet_parlor,
    "library": _effet_library, "study": _effet_study,
    "gallery": _effet_gallery, "fresco": _effet_fresco,
    "office": _effet_office, "thearms": _effet_thearms,
    "thepool": _effet_thepool, "trophyroom": _effet_trophyroom,
    "room46": _effet_room46, "passageway": _effet_passageway,
    "passageroom": _effet_passageroom, "seriesgarage": _effet_seriesgarage,
    "garage": _effet_garage, "mallroom": _effet_mallroom,
    "entrancehall": _effet_entrancehall, "antechamber": _effet_antechamber,
    "banana": _effet_banana, "pomme": _effet_pomme,
    "sandwich": _effet_sandwich, "repas": _effet_repas
}

def _norm(n: str) -> str:
    return "".join(ch.lower() for ch in str(n) if ch.isalnum())

def appliquer_effet(piece: Piece, ctx: Contexte) -> str:
    t = piece.get("type", "")
    f = EFFETS_PAR_TYPE.get(_norm(t))
    if f is None:
        return f"Aucun effet défini pour '{t}'"
    return f(piece, ctx)