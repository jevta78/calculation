def list_to_string(qs):
    lista = []
    for i in range(0, len(qs)):
        lista.append(str(qs[i][2]))
    st = ','.join(lista)
    return st