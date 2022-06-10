class IzvestajMesecItem():
    def __init__(self, brojilo : int, korisnik : str, adresa : str, grad : str, potrosnja : float):
        self.brojilo = brojilo
        self.korisnik = korisnik
        self.grad = grad
        self.adresa = adresa
        self.potrosnja = potrosnja
class IzvestajMesec():
    def __init__(self,mesec : str, items : list):
        self.mesec = mesec
        self.items = items