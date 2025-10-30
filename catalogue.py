# -*- coding: utf-8 -*-
"""
catalogue.py — Chargement/normalisation de la pioche (pool) de pièces.

Format attendu (YAML ou JSON):
- Soit une liste directe de pièces: 
    - [{"type": "...", "couleur": "...", "rarete": 1, "cout_gemmes": 0}, ...]
- Soit un objet avec une clé "pieces":
    - {"pieces": [ ... ]}

Chaque pièce est normalisée:
- type (str), couleur (str)
- rarete (int >= 1)
- cout_gemmes (int >= 0)
"""

from __future__ import annotations
from typing import List, Dict, Sequence
import json
import os

# yaml optionnel
try:
    import yaml  # type: ignore
    _HAVE_YAML = True
except Exception:
    _HAVE_YAML = False

Piece = Dict[str, object]


# ----------------------- Normalisation -----------------------

def _coerce_int_ge(value, default: int, minimum: int = 0) -> int:
    """Convertit en int, applique un minimum; fallback sur default si conversion impossible."""
    try:
        v = int(value)
    except Exception:
        v = default
    return max(minimum, v)

def _normalize_piece(p: Dict[str, object]) -> Piece:
    """Fixe les valeurs manquantes et convertit les types."""
    t = str(p.get("type", "Inconnue"))
    c = str(p.get("couleur", "gris"))
    r = _coerce_int_ge(p.get("rarete", 1), default=1, minimum=1)        # >= 1
    g = _coerce_int_ge(p.get("cout_gemmes", 0), default=0, minimum=0)   # >= 0

    return {
        "type":        t,
        "couleur":     c,
        "rarete":      r,
        "cout_gemmes": g,
    }

def _normalize_list(lst: Sequence[Dict[str, object]]) -> List[Piece]:
    return [_normalize_piece(p) for p in lst]


# ----------------------- Chargement -----------------------

def _extract_list(data) -> List[Dict[str, object]]:
    """
    Accepte soit une liste directe, soit un dict ayant la clé 'pieces'.
    Léger garde-fou pour éviter les erreurs de format.
    """
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and "pieces" in data:
        pieces = data.get("pieces")
        if isinstance(pieces, list):
            return pieces
    raise ValueError("Le fichier doit contenir une liste de pièces ou un objet avec la clé 'pieces'.")

def charger_catalogue(path: str) -> List[Piece]:
    """
    Charge un catalogue YAML (si PyYAML dispo) ou JSON, puis normalise.
    Lève FileNotFoundError si le fichier n'existe pas, ValueError si le format est invalide.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(path)

    ext = os.path.splitext(path)[1].lower()
    with open(path, "r", encoding="utf-8") as f:
        if ext in (".yaml", ".yml"):
            if not _HAVE_YAML:
                raise RuntimeError("PyYAML non installé (pip install pyyaml).")
            raw = yaml.safe_load(f) or []
        else:
            # fallback JSON
            raw = json.load(f)

    pieces_raw = _extract_list(raw)
    return _normalize_list(pieces_raw)


# ----------------------- Utilitaires pool -----------------------

def construire_pool(catalogue: Sequence[Piece], multiplicateur: int = 1) -> List[Piece]:
    """
    Duplique éventuellement le catalogue pour grossir la pioche (MVP).
    Si multiplicateur = n, chaque pièce apparaît n fois dans le pool.
    """
    base = _normalize_list(catalogue)
    m = max(1, int(multiplicateur))
    return base * m
