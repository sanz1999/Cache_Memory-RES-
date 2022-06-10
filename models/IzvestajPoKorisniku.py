class IzvestajKorisnikItem():
    def __init__(self, adresa : str, grad : str, potrosnje : list):
        self.adresa = adresa
        self.grad = grad
        self.potrosnje = potrosnje

class IzvestajKorisnik():
    def __init__(self, korisnik : str, items : dict):
        self.korisnik = korisnik
        self.items = items