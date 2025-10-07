import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from twilio.rest import Client

# --- 1. CONFIGURAÇÕES E CHAVES ---

GOOGLE_API_KEY = 'COLE SUAS CHAVES AQUI'
TWILIO_ACCOUNT_SID = 'COLE SUAS CHAVES AQUI'
TWILIO_AUTH_TOKEN = 'COLE SUAS CHAVES AQUI'


# Configure as APIs
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash-lite-preview-09-2025') # O modelo de ia para gerar o resumo
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def get_article_text(url):
    """Função para visitar uma URL de artigo e extrair seu texto limpo."""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        main_content_div = soup.find('div', id='main-content')
        if main_content_div:
            paragraphs = main_content_div.find_all('p')
            full_text = " ".join([p.get_text(strip=True) for p in paragraphs])
            return full_text
        return None
    except Exception as e:
        print(f"--> Erro ao processar a URL {url}: {e}")
        return None

# --- 2. BUSCAR NOTÍCIAS ---
homepage_url = 'https://www.tecmundo.com.br/voxel/'
response = requests.get(homepage_url)
soup = BeautifulSoup(response.content, 'html.parser')
articles = soup.find_all('article', class_='relative py-4')
all_texts = []

print("Lendo os 10 artigos mais recentes...")
for article in articles[:10]:
    link_tag = article.find('a')
    if link_tag:
        href = link_tag.get('href')
        full_link = f"https://www.tecmundo.com.br{href}"
        text = get_article_text(full_link)
        if text:
            all_texts.append(text)

# --- 3. GERAR O RESUMO COM A IA GEMINI---
summary = None
if all_texts:
    long_text = "\n\n---\n\n".join(all_texts)
    prompt = "Você é um especialista em notícias de games. Resuma os textos a seguir, destacando as 5 notícias mais importantes. Em até 1200 caracteres. O resumo deve ser direto e informativo. Textos: " + long_text
    
    print("Enviando textos para a IA para resumir...")
    try:
        response_ia = model.generate_content(prompt)
        summary = response_ia.text
        print("Resumo gerado com sucesso!")
    except Exception as e:
        summary = f"Erro ao gerar resumo: {e}"
        print(summary)

# --- 4. ENVIAR O RESUMO PELO WHATSAPP ---
if summary:
    de_onde = 'whatsapp:+Número do Twilio' # Número do Twilio

     # Crie uma lista com todos os números autorizados
    lista_de_contatos = [
        'whatsapp:+Seu número aqui', # Seu número aqui
        'whatsapp:+Outro número aqui'  # Outro número aqui
    ]
    
    print(f"Enviando resumo para {len(lista_de_contatos)} contato(s)...")
    
    # Loop que envia a mensagem para cada número na lista
    for contato in lista_de_contatos:
        try:
            message = twilio_client.messages.create(
                                          from_=de_onde,
                                          body=summary,
                                          to=contato
                                      )
            print(f"Mensagem enviada com sucesso para {contato}!")
        except Exception as e:
            print(f"Erro ao enviar para {contato}: {e}")