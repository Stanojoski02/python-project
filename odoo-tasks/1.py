def zaokruzi(decimal_num, number_of_dec):
    if number_of_dec == 0:
        return int(decimal_num)
    a = 10 ** number_of_dec
    z = int(decimal_num * a)
    zaokruzen_broj = z / a
    return zaokruzen_broj


decimalni_broj = 3.14159
broj_decimala = 2
zaokruzeni_broj = zaokruzi(decimalni_broj, broj_decimala)
print(zaokruzeni_broj)
