from deep_translator import GoogleTranslator
from langdetect import detect

def translate(text):
    try:
        lang = detect(text)
        if lang.startswith("zh"):
            translated = GoogleTranslator(source='zh-CN', target='en').translate(text)
            return translated
        else:
            translated = GoogleTranslator(source='en', target='zh-CN').translate(text)
            return translated
    except Exception as e:
        return f"[翻译错误: {str(e)}]"
