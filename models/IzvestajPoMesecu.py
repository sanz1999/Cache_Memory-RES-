class IzvestajMesec():
    def __init__(self, items : list()):
        self.items = items

class IzvestajMesecItem():
    def __init__(self, brojilo : int, korisnik : str, adresa : str, grad : str, potrosnja : float):
        self.brojilo = brojilo
        self.korisnik = korisnik
        self.grad = grad
        self.adresa = adresa
        self.potrosnja = potrosnja