from email.errors import MessageError


class PoKorisniku:
    def __init__(self, ime : str, prezime : str, adresa : str, grad : str, lista : list):
     self.ime = ime
     self.prezime = prezime
     self.adresa = adresa
     self.grad = grad 
 
     for item in lista :
         if type(item) != tuple(str, int):
             print()          
     self.lista = lista















