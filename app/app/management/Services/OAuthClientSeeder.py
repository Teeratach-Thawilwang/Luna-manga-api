
from app.Domain.Authentication.Models.OAuthClient import OAuthClient
from app.Domain.Authentication.Models.OAuthClientFactory import OAuthClientFactory


class OAuthClientSeeder:
    def create(self):
        oAuthClients = OAuthClient.objects.values_list('name', flat=True)
        
        if 'Backoffice' not in oAuthClients:
            params = {
                'name': 'Backoffice',
                'redirect_url': None
            }
            OAuthClientFactory.create(**params)
        
        if 'Front-end web' not in oAuthClients:
            params = {
                'name': 'Front-end web',
                'redirect_url': None
            }
            OAuthClientFactory.create(**params)
            
        if 'Mobile app' not in oAuthClients:
            params = {
                'name': 'Mobile app',
                'redirect_url': None
            }
            OAuthClientFactory.create(**params)