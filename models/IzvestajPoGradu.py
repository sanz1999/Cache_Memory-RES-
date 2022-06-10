class IzvestajGrad():
    def __init__(self, items:dict()):
        self.items = items

class IzvestajGradItem():
    def __init__(self, brojilo : int, korisnik : str, adresa : str, potrosnja : float):
        self.brojilo = brojilo
        self.korisnik = korisnik
        self.adresa = adresa
        self.potrosnja = potrosnja