import os
import requests

def get_metal_prices():
    # Use Yahoo Finance (Free & No Key required)
    # Gold: GC=F, Silver: SI=F
    url = "https://query1.finance.yahoo.com/v8/finance/chart/GC=F?interval=1d"
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers).json()
    gold = r['chart']['result'][0]['meta']['regularMarketPrice']
    
    url_silver = "https://query1.finance.yahoo.com/v8/finance/chart/SI=F?interval=1d"
    r_s = requests.get(url_silver, headers=headers).json()
    silver = r_s['chart']['result'][0]['meta']['regularMarketPrice']
    
    return gold, silver

def send_whatsapp_message(gold, silver):
    # Retrieve secrets from Environment Variables (GitHub Secrets)
    token = os.getenv("WHATSAPP_TOKEN")
    phone_id = os.getenv("PHONE_NUMBER_ID")
    recipient = os.getenv("RECIPIENT_PHONE")

    url = f"https://graph.facebook.com/v18.0/{phone_id}/messages"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Payload for a basic text message
    data = {
        "messaging_product": "whatsapp",
        "to": recipient,
        "type": "text",
        "text": {"body": f"💰 Daily Price Update:\nGold: ${gold}/oz\nSilver: ${silver}/oz"}
    }
    
    response = requests.post(url, headers=headers, json=data)
    print(response.json())

if __name__ == "__main__":
    g, s = get_metal_prices()
    send_whatsapp_message(g, s)
