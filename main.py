import os
from dotenv import load_dotenv
from espn_fantasy_football_client import EspnStrengthIndexClient
from whatsapp_client import WhatsAppClient

def main():
    load_dotenv()
    league_id=os.getenv('LEAGUE_ID')
    year=2025
    swid=os.getenv('SWID')
    espn_s2=os.getenv('ESPN_S2')
    gmb_whatsapp_api_key=os.getenv('GMB_WHATSAPP_API_KEY')
    gmb_whatsapp_group_id=os.getenv('GMB_WHATSAPP_GROUP_ID')
    
    try:
        si_client=EspnStrengthIndexClient(league_id, year, swid, espn_s2)
    except Exception as e:
        print(f"Error: {e}")

    whatsapp_client=WhatsAppClient(gmb_whatsapp_api_key, gmb_whatsapp_group_id)
    
    formatted_si=whatsapp_client.format_strength_index(si_client.strength_index_sorted)
    formatted_llamas=whatsapp_client.format_llamas(si_client.llamas)
    
    try:
        whatsapp_client.send_message(formatted_si)
        whatsapp_client.send_message(formatted_llamas)
    except Exception as e:
        print(f"Error: {e}")
        
if __name__ == "__main__":
    main()
