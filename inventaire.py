
class Inventaire:
    """Classe gérant les ressources du joueur."""

    def __init__(self, pas=70, or_=0, gemmes=2, cles=0, des=0, permanents=None):
        self.pas = pas
        self.or_ = or_
        self.gemmes = gemmes
        self.cles = cles
        self.des = des
        self.permanents = permanents if permanents else set()

    # ---- Méthodes d’ajout ----
    def ajouter_pas(self, n):
        self.pas += n

    def ajouter_or(self, n):
        self.or_ += n

    def ajouter_gemmes(self, n):
        self.gemmes += n

    def ajouter_cles(self, n):
        self.cles += n

    def ajouter_des(self, n):
        self.des += n

    def ajouter_permanent(self, nom):
        self.permanents.add(nom)

    # ---- Méthodes de dépense ----
    def depenser_pas(self, n=1):
        if self.pas >= n:
            self.pas -= n
            return True
        return False

    def depenser_gemmes(self, n):
        if self.gemmes >= n:
            self.gemmes -= n
            return True
        return False

    def depenser_cles(self, n=1):
        if self.cles >= n:
            self.cles -= n
            return True
        return False

    def depenser_des(self, n=1):
        if self.des >= n:
            self.des -= n
            return True
        return False

    def afficher(self):
        """Retourne une chaîne formatée de l'état de l'inventaire."""
        return (
            f"Pas: {self.pas} | Or: {self.or_} | Gemmes: {self.gemmes} | "
            f"Clés: {self.cles} | Dés: {self.des}"
        )

if __name__ == "__main__":
    inv = Inventaire()

    print("=== Inventaire initial ===")
    print(inv.afficher())

    print("\n--- Ajouts ---")
    inv.ajouter_or(50)
    inv.ajouter_gemmes(3)
    inv.ajouter_cles(1)
    inv.ajouter_des(2)
    inv.ajouter_permanent("Carte magique")

    print(inv.afficher())

    print("\n--- Dépenses ---")
    inv.depenser_pas(5)
    inv.depenser_gemmes(2)
    inv.depenser_cles()
    inv.depenser_des()

    print(inv.afficher())

    print("\nObjets permanents :", inv.permanents)
    