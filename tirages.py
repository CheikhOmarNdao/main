# -*- coding: utf-8 -*-
import random

def _poids_rarete(p):
    # rarete 0..3 -> poids 1, 1/3, 1/9, 1/27
    r = int(p.get("rarete", 0))
    r = max(0, min(3, r))
    return 1.0 / (3 ** r)

def _filtre_posable(pool, back_dir, sur_bordure: bool):
    """Pièces posables: doivent avoir une porte vers back_dir et respecter contrainte 'bordure'."""
    out = []
    for p in pool:
        portes = set(p.get("portes", []))
        if back_dir not in portes:
            continue
        c = (p.get("contrainte_placement") or "").lower().strip()
        if c == "bordure" and not sur_bordure:
            continue
        out.append(p)
    return out

def tirer_trois(pool, rng=None, back_dir=None, sur_bordure=False, joueur_a_gemmes=True):
    """Tirage pondéré de 3 options.
       - filtre posable (porte back_dir + 'bordure')
       - pondération par rareté
       - si pas de gemmes, garantit ≥1 option coût 0 si possible
    """
    rng = rng or random.Random()
    cand = _filtre_posable(pool, back_dir, sur_bordure) if back_dir else list(pool)
    if not cand:
        return []

    poids = [_poids_rarete(p) for p in cand]
    total = sum(poids) or 1.0
    probs = [w/total for w in poids]

    def choice():
        x = rng.random()
        acc = 0.0
        for p, pr in zip(cand, probs):
            acc += pr
            if x <= acc:
                return p.copy()
        return cand[-1].copy()

    opts = [choice(), choice(), choice()]

    if not joueur_a_gemmes and all(int(o.get("cout_gemmes", 0)) > 0 for o in opts):
        zero_cost = [p for p in cand if int(p.get("cout_gemmes", 0)) == 0]
        if zero_cost:
            import random as _r
            opts[_r.randrange(3)] = _r.choice(zero_cost).copy()

    return opts
