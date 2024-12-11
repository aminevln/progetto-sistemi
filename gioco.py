def crea_tabellone():
    # Crea una griglia 6x7 con celle vuote (' ')
    return [[' ' for _ in range(7)] for _ in range(6)]

def verifica_vittoria(tabellone, giocatore):
    # Controlla orizzontale
    for riga in range(6):
        for col in range(4):  # Ci sono 4 colonne da cui partire per una vittoria orizzontale
            if all(tabellone[riga][col + i] == giocatore for i in range(4)):
                return True

    # Controlla verticale
    for col in range(7):
        for riga in range(3):  # Ci sono 3 righe da cui partire per una vittoria verticale
            if all(tabellone[riga + i][col] == giocatore for i in range(4)):
                return True

    # Controlla diagonale (da sinistra a destra)
    for riga in range(3):  # 3 righe da cui partire per una diagonale che va giù e a destra
        for col in range(4):  # 4 colonne da cui partire
            if all(tabellone[riga + i][col + i] == giocatore for i in range(4)):
                return True

    # Controlla diagonale (da destra a sinistra)
    for riga in range(3):  # 3 righe da cui partire per una diagonale che va giù e a sinistra
        for col in range(3, 7):  # 3 colonne da cui partire
            if all(tabellone[riga + i][col - i] == giocatore for i in range(4)):
                return True

    return False
