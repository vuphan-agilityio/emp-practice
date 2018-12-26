"""Authentication common methods."""
from django.contrib.auth.models import User
from tastypie.authentication import Authentication

import jwt

from ..commons.custom_exception import CustomBadRequest
from ..commons.constants import JWT_AUTH


class AccessTokenAuthentication(Authentication):
    """Provide authentication for access token."""

    def extract_credentials(self, request):
        """Extract key."""

        try:
            if request.META.get('HTTP_AUTHORIZATION'):
                access_token = request.META.get('HTTP_AUTHORIZATION')
            else:
                raise CustomBadRequest(error_type='UNAUTHORIZED')
        except Exception:
            raise CustomBadRequest(
                error_type='INVALID_DATA',
                error_message='Incorrect authorization header.')

        return access_token

    def is_authenticated(self, request, **kwargs):
        """Verify authentication."""

        # Get access_token from exact_credentials method
        access_token = self.extract_credentials(request)

        # Decode jwt to get user_id
        if access_token:
            try:
                payload = jwt.decode(
                    access_token,
                    JWT_AUTH.get('JWT_SECRET'),
                    algorithms=[JWT_AUTH.get('JWT_ALGORITHM')])
            except jwt.DecodeError:
                raise CustomBadRequest(
                    error_type='UNAUTHORIZED',
                    error_message='The token is invalid')
            except jwt.ExpiredSignatureError:
                raise CustomBadRequest(
                    error_type='UNAUTHORIZED',
                    error_message='The token is expired')

        # Try get user by access token in request
        try:
            user = User.objects.get(id=payload['user_id'])
            print('exp: ', payload['exp'])
        except User.DoesNotExist:
            raise CustomBadRequest(
                error_type='INVALID_DATA',
                error_message='Can not get user with access token')

        request.user = user

        if user.is_authenticated:
            return True
        else:
            raise CustomBadRequest(
                error_type='UNAUTHORIZED',
                error_message='Authentication was problem')
