# -*- coding: utf-8 -*-
#tirages.py c'est génération des 3 options de pièces. pool : liste de dicts pièce {"type","couleur","rarete","cout_gemmes"}
#contrainte : au moins 1 pièce avec cout_gemmes = 0

from __future__ import annotations
from typing import List, Dict, Sequence
import random

Piece = Dict[str, object]

#helpers 
def _poids_rarete(rarete: int) -> float: 
#Convertit une rareté (1 commun, 2 rare, 3 épique) en poids de tirage. + la rareté est grande + le poids est petit (+ rare).  
    return 1.0 / float(max(1, rarete))# ça peut etre + dure si on fait rareté au carre

def _tirage_pondere(pool: Sequence[Piece], rng: random.Random) -> Piece: #Tire 1 pièce selon poids_rarete
    
    poids = [_poids_rarete(int(p.get("rarete", 1))) for p in pool]
    total = sum(poids)
    r = rng.random() * total
    cumul = 0.0
    for p, w in zip(pool, poids):
        cumul += w
        if r <= cumul:
            return dict(p)       #copie en evitant de modifier l'original
    return dict(pool[-1])  #si arrondi/flotteurs renvoyer dernière pièce


#API publique 
def tirer_trois(pool: Sequence[Piece], rng: random.Random) -> List[Piece]:  #Tire 3 pièces ds pool selon rareté
   
    if len(pool) == 0:
        return []

    # au moins une gratuite
    gratuites = [p for p in pool if int(p.get("cout_gemmes", 0)) == 0]
    if gratuites:
        choix = [dict(rng.choice(gratuites))]
    else:                  # si aucune gratuite dans le pool, on force une gratuite
        forcee = dict(_tirage_pondere(pool, rng))
        forcee["cout_gemmes"] = 0
        choix = [forcee]

    #compléter jusqu'à 3 tirages
    while len(choix) < 3:
        choix.append(_tirage_pondere(pool, rng))
    return choix

def reroll_options(pool: Sequence[Piece], rng: random.Random) -> List[Piece]:
    #Retire 3 nouvelles options 
    return tirer_trois(pool, rng)
