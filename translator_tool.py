# -*- coding: utf-8 -*-
# translator_tool.py

def translate_to_german(phrase):
    """Translates a common English phrase to German."""
    translations = {
        "good morning": "Guten Morgen",
        "have a nice day": "Einen schönen Tag",
        "sunshine": "Sonnenschein"
    }
    
    phrase_lower = phrase.strip().lower()
    
    if phrase_lower in translations:
        return translations[phrase_lower]
    else:
        return f"Sorry, I don't know the translation for '{phrase}'."
