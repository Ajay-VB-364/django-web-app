from linkedin_api import Linkedin


class LinkedInService:
    """ LinkedIN service functions"""

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_linkedin_api(self):
        """ Authenticate using any Linkedin account credentials """
        if self.username and self.password:
            api = Linkedin(self.username, self.password)
        return api
    
    def get_linkedin_company_details(self, api, company):
        """ Get Company Details """
        company = company.strip().lower()
        company = company.replace(' ','-')
        comp_data = {}
        if api:
            try:
                comp_data = api.get_company(company)
            except Exception as e:
                print("Error fetching comp_data ", str(e))
        return comp_data