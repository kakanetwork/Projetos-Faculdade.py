import os



lista = list()
lista = ["%userprofile%\AppData\Local\Temp", "%LOCALAPPDATA%\Microsoft\Windows\INetCache", "%windir%\temp", 
"C:\Windows\Prefetch", "C:\\Users\\USUARIO\Recent"]

lista_teste = ["C:\\Users\\USUARIO\OneDrive\Documents\s", "C:\\Users\\USUARIO\OneDrive\Documents\\a"]

for x in lista_teste:
    nomes = tuple(os.listdir(x))
    for a in nomes:
        os.remove('x\\a')
    print(f"apagando:... {os.listdir(x)}\n")