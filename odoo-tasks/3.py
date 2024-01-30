def sortirajne_rijeci(input_, output_):
    with open(input_, 'r') as data:
        data = data.read()
        rijeci = data.split()
        rijeci.sort()
    with open(output_, 'w') as data:
        data.write(' '.join(rijeci))
    print(f"Riječi u datoteci su sortirane")


ulazna_datoteka = input("Input file ")
izlazna_datoteka = input("Output file")

sortirajne_rijeci(ulazna_datoteka, izlazna_datoteka)
