class Inventaire:
    def __init__(self, pas=70, or_=0, gemmes=2, cles=0, des=0, permanents=None):
        self.pas = pas
        self.or_ = or_
        self.gemmes = gemmes
        self.cles = cles
        self.des = des
        self.permanents = permanents if permanents else set()

    def depenser_pas(self, n=1):
        if self.pas >= n:
            self.pas -= n
            return True
        return False

    def afficher(self):
        return f"Pas: {self.pas} | Or: {self.or_} | Gemmes: {self.gemmes} | Clés: {self.cles} | Dés: {self.des}"
