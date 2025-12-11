import os
import google.generativeai as genai
import json

from app import model


class GameLogic:

    def __init__(self):
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
            resp = model.generate_content(prompt)
            return json.loads(self.clean_json(resp.text))
        except:
            return None

    def call_ai_text(self, prompt):
        try:
            return model.generate_content(prompt).text.strip()
        except:
            return "..."