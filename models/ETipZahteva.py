from enum import Enum


class ETipZahteva(Enum):
     #Tipovi zahteva za Readera 
     KORISNIK = 1 
     MESEC = 2
     GRAD = 3

     #Tipovi zahteva za upravljanje bazom
     ADD_USER = 4
     REMOVE_USER = 5
     ADD_CON = 6         #Ovo korisnti Dumping Buffer
     REMOVE_CON = 7
     GET_ALL_USERS = 8
     EXISTS_USER = 9
     DB_INSERTS = 10
     GET_ALL_CON = 11