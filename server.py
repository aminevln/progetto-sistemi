import socket
import threading
from gioco import crea_tabellone, verifica_vittoria

# Lista dei client connessi
clients = []

# Gestisce la connessione di ogni giocatore
def gestisci_client(client_socket, client_address, giocatore, tabellone, lock):
    try:
        # Aggiungi il client alla lista dei client
        clients.append(client_socket)
        
        # Invia il messaggio che identifica il giocatore
        client_socket.sendall(f"Sei il Giocatore {giocatore}!".encode())
        
        while True:
            # Riceve la mossa dal client
            colonna = int(client_socket.recv(1024).decode())
            if not (0 <= colonna < 7):
                client_socket.sendall("Mossa non valida!".encode())
                continue

            # Trova la riga vuota nella colonna
            for riga in range(5, -1, -1):
                if tabellone[riga][colonna] == ' ':
                    tabellone[riga][colonna] = giocatore
                    break
            else:
                client_socket.sendall("Colonna piena!".encode())
                continue

            # Controlla se c'è una vittoria
            if verifica_vittoria(tabellone, giocatore):
                # Manda la vittoria al client che ha vinto
                client_socket.sendall("Hai vinto!".encode())

                # Invia il messaggio di vittoria a tutti i client
                lock.acquire()
                for client in clients:
                    try:
                        client.sendall(f"Vittoria per il Giocatore {giocatore}!".encode())
                    except Exception as e:
                        print(f"Errore nell'invio al client: {e}")
                lock.release()
                return

            # Aggiorna il tabellone e invia a tutti i client
            lock.acquire()
            for client in clients:
                try:
                    client.sendall(str(tabellone).encode())
                except Exception as e:
                    print(f"Errore nell'invio al client: {e}")
            lock.release()
    except Exception as e:
        print(f"Errore con il client: {e}")
    finally:
        # Rimuovi il client dalla lista se si disconnette
        clients.remove(client_socket)
        client_socket.close()

# Avvia il server
def avvia_server():
    tabellone = crea_tabellone()
    lock = threading.Lock()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(2)
    print("Server in attesa di connessioni...")

    client_1, addr_1 = server_socket.accept()
    print(f"Giocatore 1 connesso da {addr_1}")
    client_2, addr_2 = server_socket.accept()
    print(f"Giocatore 2 connesso da {addr_2}")

    threading.Thread(target=gestisci_client, args=(client_1, addr_1, 'X', tabellone, lock)).start()
    threading.Thread(target=gestisci_client, args=(client_2, addr_2, 'O', tabellone, lock)).start()

if __name__ == "__main__":
    avvia_server()
