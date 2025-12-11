import os
import google.generativeai as genai
from dotenv import load_dotenv

# Assumiamo che il secondo file si chiami 'game_logic.py'
from GameLogic import GameLogic

# 1. Carica le variabili dal file .env
load_dotenv()

# 2. Recupera la chiave
api_key = os.getenv("GOOGLE_API_KEY")

# 3. Verifica che la chiave esista
if not api_key:
    raise ValueError("Errore: Chiave API non trovata. Assicurati di aver creato il file .env con GOOGLE_API_KEY.")

# 4. Configura GenAI
genai.configure(api_key=api_key)

try:
    model = genai.GenerativeModel('models/gemini-2.5-flash')
except:
    print("Modello 2.5 non trovato, passo a 2.0-flash")
    model = genai.GenerativeModel('gemini-2.0-flash')

# --- ESECUZIONE ---
if __name__ == "__main__":
    # Inizializziamo la classe passando il modello creato qui sopra
    game = GameLogic(model)

    game.set_nickname()
    game.select_genre()
    game.select_archetype()
    game.generate_introduction()

    # Per verifica, stampiamo lo stato
    print(f"\nStato aggiornato: {game.state}")