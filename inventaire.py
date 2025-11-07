# -*- coding: utf-8 -*-

class Inventaire:
    def __init__(self, pas=70, or_=0, gemmes=2, cles=0, des=0, bananes=0):
        # consommables
        self.pas = int(pas)
        self.or_ = int(or_)
        self.gemmes = int(gemmes)
        self.cles = int(cles)
        self.des = int(des)
        self.bananes = int(bananes)

        # permanents (bool)
        self.pelle = False
        self.marteau = False
        self.kit_crochetage = False
        self.detecteur_metaux = False
        self.patte_lapin = False

    # ---- dépenses (consommables)
    def depenser_pas(self, n=1):
        if self.pas >= n:
            self.pas -= n
            return True
        return False

    def depenser_gemmes(self, n=1):
        if self.gemmes >= n:
            self.gemmes -= n
            return True
        return False

    def depenser_des(self, n=1):
        if self.des >= n:
            self.des -= n
            return True
        return False

    # ---- gains (consommables)
    def ajouter_pas(self, n=1): self.pas += n
    def ajouter_or(self, n=1): self.or_ += n
    def ajouter_gemmes(self, n=1): self.gemmes += n
    def ajouter_cles(self, n=1): self.cles += n
    def ajouter_des(self, n=1): self.des += n
    def ajouter_bananes(self, n=1): self.bananes += n

    # ---- permanents
    def donner_permanent(self, nom: str) -> bool:
        nom = (nom or "").strip().lower()
        if nom == "pelle" and not self.pelle:
            self.pelle = True; return True
        if nom == "marteau" and not self.marteau:
            self.marteau = True; return True
        if nom == "kit de crochetage" and not self.kit_crochetage:
            self.kit_crochetage = True; return True
        if nom == "détecteur de métaux" and not self.detecteur_metaux:
            self.detecteur_metaux = True; return True
        if nom == "patte de lapin" and not self.patte_lapin:
            self.patte_lapin = True; return True
        return False

    def liste_permanents(self):
        lst = []
        if self.kit_crochetage: lst.append("Lockpick Kit")
        if self.patte_lapin:    lst.append("Lucky Rabbit's Foot")
        if self.pelle:          lst.append("Shovel")
        if self.marteau:        lst.append("Hammer")
        if self.detecteur_metaux: lst.append("Metal Detector")
        return lst

    # ---- affichage HUD (consommables à droite)
    def afficher(self):
        return (f"Pas: {self.pas} | Or: {self.or_} | Gemmes: {self.gemmes} | "
                f"Clés: {self.cles} | Dés: {self.des} | Bananes: {self.bananes}")
