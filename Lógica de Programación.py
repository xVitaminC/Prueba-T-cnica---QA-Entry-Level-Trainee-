def eliminar_duplicados(lista):
    sin_dupl = []
    for i in range(len(lista)):
        encontrado = False
        for j in range(len(sin_dupl)):
            if sin_dupl[j] == lista[i]:
                encontrado = True
                break
        if not encontrado:
            sin_dupl.append(lista[i])
    return sin_dupl

def ordenar_burbuja(lista):
    arr = list(lista)
    n = len(arr)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

entrada = [4, 2, 7, 2, 4, 9, 1]
sin_duplicados = eliminar_duplicados(entrada)
salida = ordenar_burbuja(sin_duplicados)
print(salida)  # → [1, 2, 4, 7, 9]
