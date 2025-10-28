class Inventaire:
    def __init__(self):
        self.pas = 70
        self.gemmes = 2
        self.cles = 0
        self.des = 0
        self.objets_permanents = set()

    def ajouter_objet(self, objet):
        if objet.type == "permanent":
            self.objets_permanents.add(objet.nom)
        elif objet.nom == "clé":
            self.cles += 1
        elif objet.nom == "pas":
            self.pas += objet.valeur
