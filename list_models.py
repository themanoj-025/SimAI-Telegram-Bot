import google.generativeai as genai

from config.config import Config


def list_models() -> None:
    config = Config()
    if not config.GEMINI_API_KEY:
        print("No API key.")
        return
    genai.configure(api_key=config.GEMINI_API_KEY)
    for m in genai.list_models():
        if "generateContent" in m.supported_generation_methods:
            print(m.name)


if __name__ == "__main__":
    list_models()
