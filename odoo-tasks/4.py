def glavna_funkcija():
    lista_brojeva = []

    while True:
        print("\nIzaberite opciju:")
        print("a) Unos/dodavanje novog broja u listu")
        print("b) Ispitati poziciju nekog broja u listi")
        print("c) Izaći iz programa")
        o = input("Vaš odabir: ").lower()
        if o == 'a':
            while True:
                try:
                    broj = input("Unesite broj (ili 'X' za povratak): ")
                    if broj == 'X':
                        break
                    broj = float(broj)
                    if 1 <= broj <= 100:
                        lista_brojeva.append(broj)
                        print(f"Broj {broj} dodan u listu.")
                    else:
                        print("Greška: Unesite broj između 1 i 100.")
                except ValueError:
                    unos = input("Greška: Unesite ispravan broj ili 'X' za povratak: ")
                    if unos.upper() == 'X':
                        break
        elif o == 'b':
            while True:
                try:
                    broj_za_ispitivanje = input("Unesite broj za ispitivanje pozicije (ili 'X' za povratak): ")
                    if broj_za_ispitivanje == 'X':
                        break
                    else:
                        broj_za_ispitivanje = int(broj_za_ispitivanje)
                        if broj_za_ispitivanje in lista_brojeva:
                            pozicija = lista_brojeva.index(broj_za_ispitivanje)
                            print(f"Broj {broj_za_ispitivanje} se nalazi na poziciji {pozicija}.")
                        else:
                            print(f"Broj {broj_za_ispitivanje} ne postoji u listi.")

                except ValueError:
                    print("Greška: Unesite ispravan broj ili 'X' za povratak.")

        elif o == 'c':
            print("Izlaz iz programata.")
            break
        else:
            print("Greška: Pogrešan vnes. Molim pokušajte ponovno.")

glavna_funkcija()
