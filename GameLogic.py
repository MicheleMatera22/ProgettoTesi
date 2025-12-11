import json

class GameLogic:

    def __init__(self, ai_model):
        self.model = ai_model  # Salviamo il modello passato da app.py
        self.reset()

    def reset(self):
        self.state = {
            "nickname": "",
            "genre": "",
            "archetype": "",
            "inventory": [],
            "story_log": [],
            "game_over": False,
            "hp": 100,
            "map_layout": {},
            "player_pos": (0, 0),
            "total_rooms": 5,
            "rooms_solved": 0,
            # NUOVO STATO: Indica se siamo nel prologo
            "awaiting_start": False
        }

    # --- UTILS ---
    def clean_json(self, text):
        text = text.replace("```json", "").replace("```", "").strip()
        start = text.find("{")
        end = text.rfind("}") + 1
        return text[start:end] if start != -1 else text

    def call_ai_json(self, prompt):
        try:
            # Uso self.model invece di model
            resp = self.model.generate_content(prompt)
            return json.loads(self.clean_json(resp.text))
        except:
            return None

    def call_ai_text(self, prompt):
        try:
            # Uso self.model invece di model
            return self.model.generate_content(prompt).text.strip()
        except:
            return "..."

    def set_nickname(self):
        while True:
            name = input("Inserisci il nome del tuo personaggio: ").strip()

            if len(name) > 0:
                self.state["nickname"] = name
                return name
            else:
                print("Il nome non può essere vuoto. Riprova.")

    def select_genre(self):
        genres = [
            "Fantasy Medievale (Draghi, Magia, Cavalieri)",
            "Cyberpunk (Futuro, Hacker, Neon)",
            "Horror (Mistero, Follia, Antichi)",
            "Giallo (Detective, Crimini, Intrighi)",
            "Post-Apocalittico (Sopravvivenza, Rovine, Scarsità)"
        ]

        print("\n--- SELEZIONE GENERE NARRATIVO ---")
        for index, genre in enumerate(genres, 1):
            print(f"{index}. {genre}")

        # Loop per validare l'input
        while True:
            choice = input("\nDigita il numero del genere che preferisci (1-5): ").strip()

            if choice.isdigit():
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(genres):
                    # Salvataggio nello stato pulendo la descrizione tra parentesi per l'AI
                    selected_full = genres[choice_idx]
                    # Prendo solo la parte prima della parentesi per semplicità nello stato
                    clean_genre = selected_full.split("(")[0].strip()

                    self.state["genre"] = clean_genre
                    print(f"Genere selezionato: {clean_genre}")
                    return clean_genre

            print("Scelta non valida. Inserisci un numero da 1 a 5.")

    def select_archetype(self):
        if not self.state["genre"]:
            print("Errore: Seleziona prima un genere!")
            return

        print(f"\n--- GENERAZIONE CLASSI ({self.state['genre']}) ---")
        print("L'Oracolo sta individuando le classi disponibili...")

        # 1. Prompt semplificato: Chiede SOLO una lista di nomi
        prompt = f"""
        Agisci come un Game Designer. Il genere è: "{self.state['genre']}".
        Elenca 4 nomi di archetipi/classi giocabili per questo genere.

        Rispondi ESCLUSIVAMENTE con un array JSON di stringhe.
        Niente descrizioni, niente testo extra.

        Esempio formato output:
        ["Guerriero", "Mago", "Ladro", "Chierico"]
        """

        # 2. Chiamata AI
        options = self.call_ai_json(prompt)

        # Controllo errori
        if not options or not isinstance(options, list):
            print("⚠️ Errore AI. Riprovo...")
            # Qui potresti mettere un return o una logica di retry limitata
            return None

        # 3. Mostra le opzioni (ora sono semplici stringhe)
        print("\nScegli la tua classe:")
        for index, name in enumerate(options, 1):
            print(f"{index}. {name}")

        # 4. Selezione Utente
        while True:
            choice = input("\nScegli il numero (1-4): ").strip()

            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(options):
                    selected_name = options[idx]

                    # Se per caso l'AI ha restituito un oggetto invece di una stringa, lo gestiamo
                    if isinstance(selected_name, dict):
                        selected_name = list(selected_name.values())[0]

                    self.state["archetype"] = str(selected_name)
                    print(f"Hai scelto: {selected_name}")
                    return selected_name

            print("Scelta non valida.")

