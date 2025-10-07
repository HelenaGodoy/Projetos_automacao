import google.generativeai as genai

# COLE SUA CHAVE DE API DO GOOGLE AI STUDIO AQUI
GOOGLE_API_KEY = 'GOOGLE_API_KEY'

genai.configure(api_key=GOOGLE_API_KEY)

print("--- Modelos de IA disponíveis ---")
for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)
