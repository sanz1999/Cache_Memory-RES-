class IzvestajGradItem():
    def __init__(self, brojilo : int, korisnik : str, adresa : str, potrosnja : float):
        self.brojilo = brojilo
        self.korisnik = korisnik
        self.adresa = adresa
        self.potrosnja = potrosnja
class IzvestajGrad():
    def __init__(self,grad : str, items : dict):
        self.grad = grad
        self.items = items
