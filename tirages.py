# -*- coding: utf-8 -*-
import random

#Calcule un poids à partir de la rareté d’une pièce
def _poids_rarete(p):
    # rarete 0..3 -> poids 1, 1/3, 1/9, 1/27
    r = int(p.get("rarete", 0))
    r = max(0, min(3, r))
    return 1.0 / (3 ** r)

#À partir du pool de pièces, construit la liste des pièces posables qui repectent les contraintes
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

#tout le tirage des 3 options de salles
def tirer_trois(
    pool,
    rng=None,
    back_dir=None,
    sur_bordure=False,
    joueur_a_gemmes=True,
    modif_couleurs=None,
    modif_types=None,
):
    """Tirage pondéré de 3 options.
       d'abord filtre posable (porte back_dir + 'bordure')
       ensuite pondération par rareté
       puis prise en compte éventuelle de modificateurs par couleur / type
       et si pas de gemmes, garantit ≥1 option coût 0 si possible
    """
    rng = rng or random.Random()
    cand = _filtre_posable(pool, back_dir, sur_bordure) if back_dir else list(pool)
    if not cand:
        return []

    modif_couleurs = modif_couleurs or {}
    modif_types = modif_types or {}

    poids = []
    for p in cand:
        w = _poids_rarete(p)

        # ajustement par couleur (effets de Greenhouse, etc.)
        couleur = str(p.get("couleur", "")).strip().lower()
        if couleur in modif_couleurs:
            w *= float(modif_couleurs[couleur])

        # ajustement par type de pièce (effets de Furnace, etc.)
        type_norm = str(p.get("type", "")).strip().lower()
        if type_norm in modif_types:
            w *= float(modif_types[type_norm])

        poids.append(w)

    total = sum(poids) or 1.0
    probs = [w / total for w in poids]

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
