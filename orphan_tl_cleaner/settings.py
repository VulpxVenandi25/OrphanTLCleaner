import os
import sys
import json


class Settings:
    def __init__(self):
        self.path = self._get_path()

    def _get_path(self):
        if hasattr(sys, '_MEIPASS'):
            base = sys._MEIPASS
        else:
            base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base, 'settings.json')

    def load(self):
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"locale": "es_ES", "theme": "light", "comment_blocks": False}

    def save(self, key, value):
        settings = self.load()
        settings[key] = value
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)
