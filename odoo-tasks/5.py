def razdvoji_podatke(p):
    pod = p.split(', ')
    ime = pod[0]
    adr = pod[1]
    p_b_m = pod[2]
    u_k_b = adr.split(' ')
    ul = ' '.join(u_k_b[:-1])
    k_b_d = u_k_b[-1]
    if k_b_d[-1].isalpha():
        k_b = k_b_d[:-1]
        dod_k_b = k_b_d[-1]
    else:
        k_b = k_b_d
        dod_k_b = None
    p_b, m = p_b_m.split(' ')
    print("Ime i prezime:", ime)
    print("Ulica:", ul)
    print("Kućni broj:", k_b)
    if dod_k_b is not None:
        print("Dodatak kućnom broju:", dod_k_b)
    print("Poštanski broj:", p_b)
    print("Mesto:", m)
  
ulazni = input("Unesite podatke (ime, adresa, poštanski broj i mesto): ")
razdvoji_podatke(ulazni)
