import json

LANGUAGES = ['ar', 'fr', 'en']

def get_translation(lang):
    try:
        with open(f'translations/{lang}.json', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}
