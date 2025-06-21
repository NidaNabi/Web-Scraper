
import requests

def translate_to_english(text):
    url = "https://api.mymemory.translated.net/get"
    params = {
        "q": text,
        "langpair": "es|en"  # Spanish to English
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data["responseData"]["translatedText"]
        else:
            print("Translation API error:", response.text)
            return text
    except Exception as e:
        print("Translation failed:", str(e))
        return text

print(translate_to_english("Hola, ¿cómo estás?"))