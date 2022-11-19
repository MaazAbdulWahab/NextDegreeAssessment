from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class CustomTokenAuth(TokenAuthentication):

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        
        if token.created + timedelta(minutes=settings.TOKEN_EXPIRATION) < timezone.now():
            
            token.delete()
            raise exceptions.AuthenticationFailed(_('Token Expired'))
 

        return (token.user, token)
