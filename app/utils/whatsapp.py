import os, requests
from rest_framework.exceptions import ParseError


class WhatsAppIntegration():
    def __init__(self):
        self.wati_auth_token = os.getenv('WATI_ACCESS_TOKEN', None)
        self.wati_url = os.getenv('WATI_URL', None)


    def send_whatsapp_message(self, buyer_number=None, country_code=None, content=None, template_name=None):
        """ Send WhatsApp Message """
        try:
            if self.wati_auth_token and self.wati_url:
                url = f'{self.wati_url}api/v1/sendTemplateMessage?whatsappNumber={country_code}{buyer_number}'
                payload = (
                    "{\"parameters\":[{\"name\":\"content\",\"value\":\""
                    + content
                    + "\"}],\"template_name\":\""+template_name+"\",\"broadcast_name\":\""
                    + buyer_number
                    + "\"}"
                )
                headers = {"Content-Type": "application/json-patch+json", "Authorization": f"Bearer {self.wati_auth_token}"}
                response = requests.request("POST", url, data=payload, headers=headers)
                json_res = response.json()
                if response.status_code == 200 and json_res['validWhatsAppNumber']:
                    return True, 'WhatsApp message sent'
                else:
                    return False, 'WhatsApp message sending failed - ' + str(json_res['info'])
            else:
                raise Exception(' Whats App Auth Token & URL is not provided in the application')
        except Exception as e:
            raise ParseError({"details": str(e)})

