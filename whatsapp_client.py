import requests

class WhatsAppClient():
    def __init__(self, gmb_whatsapp_api_key, gmb_whatsapp_group_id):
        self._whatsapp_message_endpoint="https://api.wassenger.com/v1/messages"
        self._gmb_whatsapp_api_key=gmb_whatsapp_api_key
        self._gmb_whatsapp_group_id=gmb_whatsapp_group_id

    def send_message(self, message):
        payload = {
            "group": self._gmb_whatsapp_group_id,
            "message": message
        }
        headers = {
            "Content-Type": "application/json",
            "Token": self._gmb_whatsapp_api_key 
        }

        response = requests.post(self._whatsapp_message_endpoint, json=payload, headers=headers)
        response.raise_for_status()

    def format_strength_index(self, strength_index):
        formatted_si = "Strength Index Rankings:\n"
        for team in strength_index:
            formatted_si += f"{team[0]}: {team[1]} Wins, {team[2]} Losses\n"
        return formatted_si
    
    def format_llamas(self, llamas):
        formatted_llamas = "The llamas are:\n"

        if len(llamas) < 10:
            raise Exception("invalid llamas format")

        for i, llama in enumerate(llamas):
            if i in [0, 1]:
                position_keyword="over"
            if i > 1 and i < 8:
                continue
            if i in [8, 9]:
                position_keyword="under"
                
            formatted_llamas += f"{llama[0]} is {position_keyword}performing by {llama[1]*-1} spots\n"
        
        return formatted_llamas
