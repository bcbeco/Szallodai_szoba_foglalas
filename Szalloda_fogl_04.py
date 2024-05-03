# Szállodai szoba foglalás
from datetime import datetime

class Szoba:
    def __init__(self, ar, szobaszam):
        self.ar = ar
        self.szobaszam = szobaszam
        self.foglalasok = []

    def foglal(self, foglalas):
        self.foglalasok.append(foglalas)

    def lemond(self, foglalas):
        if foglalas in self.foglalasok:
            self.foglalasok.remove(foglalas)
        else:
            print("Nincs ilyen foglalás ehhez a szobához.")

    def ellenoriz(self, datum):
        for foglalas in self.foglalasok:
            if foglalas.datum == datum:
                return False
        return True

    def foglalas_ar(self, datum):
        if not self.ellenoriz(datum):
            return 0
        else:
            return self.ar


class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(ar=10000, szobaszam=szobaszam)  # Egyágyas szoba ára: 10 000
        self.szemelyek_szama = 1

class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(ar=15000, szobaszam=szobaszam)  # Kétágyas szoba ára: 15 000
        self.szemelyek_szama = 2

class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.egyagyas_szobak = []
        self.ketagyas_szobak = []

    def add_egyagyas_szoba(self, egyagyas_szoba):
        self.egyagyas_szobak.append(egyagyas_szoba)

    def add_ketagyas_szoba(self, ketagyas_szoba):
        self.ketagyas_szobak.append(ketagyas_szoba)

    def foglalas(self, szobaszam, datum):
        for szoba in self.egyagyas_szobak + self.ketagyas_szobak:
            if szoba.szobaszam == szobaszam:
                if szoba.ellenoriz(datum):
                    ar = szoba.foglalas_ar(datum)
                    if ar > 0:
                        foglalas = Foglalas(szoba, datum)
                        szoba.foglal(foglalas)
                        return ar
                    else:
                        return "A szoba már foglalt ezen a napon."
                else:
                    return "A szoba már foglalt ezen a napon."
        return "Nincs ilyen szoba."

    def lemondas(self, szobaszam, datum):
        for szoba in self.egyagyas_szobak + self.ketagyas_szobak:
            if szoba.szobaszam == szobaszam:
                for foglalas in szoba.foglalasok:
                    if foglalas.datum == datum:
                        szoba.lemond(foglalas)
                        return "A foglalás sikeresen törölve."
                return "Nincs ilyen foglalás ehhez a szobához."
        return "Nincs ilyen szoba."

    def listaz_foglalasok(self):
        foglalasok = []
        for szoba in self.egyagyas_szobak + self.ketagyas_szobak:
            for foglalas in szoba.foglalasok:
                foglalasok.append((szoba.szobaszam, foglalas.datum))
        return foglalasok

    def listaz_szobak(self):
        szobak_allapota = []
        for szoba in self.egyagyas_szobak + self.ketagyas_szobak:
            foglalasok = [foglalas.datum for foglalas in szoba.foglalasok]
            if isinstance(szoba, EgyagyasSzoba):
                szoba_tipus = "egyágyas"
            elif isinstance(szoba, KetagyasSzoba):
                szoba_tipus = "kétágyas"
            foglalas_str = ", ".join(foglalasok)
            szobak_allapota.append((szoba.szobaszam, szoba_tipus, foglalas_str))
        return szobak_allapota

class Foglalas:
    def __init__(self, szoba, datum):
        self.szoba = szoba
        self.datum = datum

# Felhasználói interfész
def main():
    szalloda = Szalloda("Hotel BAB")
    szalloda.add_egyagyas_szoba(EgyagyasSzoba("101"))
    szalloda.add_egyagyas_szoba(EgyagyasSzoba("102"))
    szalloda.add_egyagyas_szoba(EgyagyasSzoba("103"))
    szalloda.add_ketagyas_szoba(KetagyasSzoba("201"))
    szalloda.add_ketagyas_szoba(KetagyasSzoba("202"))
    szalloda.add_ketagyas_szoba(KetagyasSzoba("203"))
    for i in range(1, 6):
        datum = f"2024-06-0{i}"
        szalloda.foglalas("101", datum)

    while True:
        print("\nVálasszon műveletet:")
        print("1. Szoba foglalása")
        print("2. Foglalás lemondása")
        print("3. Foglalások listázása")
        print("4. Szobák állapotának listázása")
        print("5. Kilépés")

        valasztas = input("Adja meg a választott művelet számát: ")

        if valasztas == "1":
            szobaszam = input("Adja meg a foglalandó szoba számát: ")
            datum = input("Adja meg a foglalás dátumát (éééé-hh-nn formátumban): ")
            try:
                datetime.strptime(datum, "%Y-%m-%d")
                ar = szalloda.foglalas(szobaszam, datum)
                if ar:
                    print("A foglalás sikeres. A szoba ára:", ar)
                else:
                    print(ar)
            except ValueError:
                print("Érvénytelen dátum formátum.")

        elif valasztas == "2":
            szobaszam = input("Adja meg a lemondani kívánt foglalás szobaszámát: ")
            datum = input("Adja meg a lemondani kívánt foglalás dátumát (éééé-hh-nn formátumban): ")
            try:
                datetime.strptime(datum, "%Y-%m-%d")
                eredmeny = szalloda.lemondas(szobaszam, datum)
                print(eredmeny)
            except ValueError:
                print("Érvénytelen dátum formátum.")

        elif valasztas == "3":
            foglalasok = szalloda.listaz_foglalasok()
            if foglalasok:
                print("Szobaszám , Foglalás dátuma")
                for foglalas in foglalasok:
                    print("Szoba:", foglalas[0], ", Dátum:", foglalas[1])
            else:
                print("Nincsenek foglalások.")

        elif valasztas == "4":
            szobak_allapota = szalloda.listaz_szobak()
            for szoba in szobak_allapota:
                if szoba[2]:
                    print(szoba[0], "számú", szoba[1], "szoba foglalásai:", szoba[2])
                else:
                    print(szoba[0], "számú", szoba[1], "szobához még nincs foglalás.")

        elif valasztas == "5":
            print("Kilépés...")
            break
        else:
            print("Érvénytelen választás.")

if __name__ == "__main__":
    main()
