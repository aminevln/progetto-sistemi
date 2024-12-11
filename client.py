import socket
import tkinter as tk
from tkinter import messagebox
import threading

class Forza4Client:
    def __init__(self, master, host, port):
        self.master = master
        self.master.title("Forza 4 - Giocatore")
        self.master.geometry("600x600")

        # Connessione al server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))

        # Ricevi il messaggio che identifica il giocatore
        self.received_message = self.client_socket.recv(1024).decode()
        print(self.received_message)  # Stampa il messaggio ricevuto dal server

        # Visualizza una finestra di messaggio con il ruolo del giocatore
        messagebox.showinfo("Connessione", self.received_message)

        # Crea il tabellone di gioco
        self.tabellone_frame = tk.Frame(self.master)
        self.tabellone_frame.place(relx=0.5, rely=0.3, anchor="center")
        self.crea_tabellone()

        # Aggiungi i pulsanti per giocare
        self.pulsanti_frame = tk.Frame(self.master)
        self.pulsanti_frame.place(relx=0.5, rely=0.8, anchor="center")
        self.crea_pulsanti()

        # Avvia il thread che ascolta i messaggi dal server
        self.listen_thread = threading.Thread(target=self.ascolta_messaggi)
        self.listen_thread.daemon = True
        self.listen_thread.start()

        # Variabile per controllare se il gioco è finito
        self.gioco_finito = False

    def crea_tabellone(self):
        """Crea la visualizzazione del tabellone vuoto."""
        self.bordi = []
        for i in range(6):  # 6 righe
            riga = []
            for j in range(7):  # 7 colonne
                label = tk.Label(self.tabellone_frame, text=" ", width=4, height=2, relief="solid", font=("Arial", 20))
                label.grid(row=i, column=j, padx=5, pady=5)
                riga.append(label)
            self.bordi.append(riga)

    def crea_pulsanti(self):
        """Crea i pulsanti per scegliere la colonna da giocare."""
        for col in range(7):
            button = tk.Button(self.pulsanti_frame, text=f"Colonna {col + 1}", width=10, command=lambda col=col: self.mossa(col))
            button.grid(row=0, column=col, padx=5, pady=5)

    def mossa(self, colonna):
        """Invia la mossa al server e aggiorna il tabellone."""
        if self.gioco_finito:
            messagebox.showinfo("Gioco finito", "Il gioco è già finito!")
            return

        # Invia la colonna al server
        self.client_socket.sendall(str(colonna).encode())

    def ascolta_messaggi(self):
        """Ascolta i messaggi dal server e aggiorna il tabellone."""
        while True:
            try:
                risposta = self.client_socket.recv(1024).decode()
                if risposta == "Colonna piena!":
                    messagebox.showwarning("Errore", risposta)
                elif risposta == "Hai vinto!":
                    messagebox.showinfo("Vittoria", "Hai vinto!")
                    self.gioco_finito = True
                    self.master.quit()  # Chiudi la finestra dopo la vittoria
                elif "Vittoria per il Giocatore" in risposta:
                    messagebox.showinfo("Vittoria", risposta)
                    self.gioco_finito = True
                    self.master.quit()  # Chiudi la finestra dopo la vittoria
                else:
                    self.aggiorna_tabellone(risposta)
            except Exception as e:
                print(f"Errore nell'ascolto: {e}")
                break

    def aggiorna_tabellone(self, tabellone_str):
        """Aggiorna il tabellone con l'aggiornamento ricevuto dal server."""
        tabellone = eval(tabellone_str)  # Converte la stringa del tabellone in una lista
        for i in range(6):
            for j in range(7):
                self.bordi[i][j].config(text=tabellone[i][j])

    def chiudi(self):
        """Chiude la connessione e l'app."""
        self.client_socket.close()
        self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = Forza4Client(root, '127.0.0.1', 12345)  # Usa l'IP e la porta del server
    root.protocol("WM_DELETE_WINDOW", app.chiudi)
    root.mainloop()
