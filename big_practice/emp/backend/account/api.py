from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.conf.urls import url
from django.db import transaction
from django.db import IntegrityError
from django.core.cache import cache
from django.conf import settings

from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.utils import trailing_slash
from tastypie.http import HttpUnauthorized
from tastypie.models import ApiKey
from tastypie.validation import Validation

from haystack.query import SearchQuerySet
import jwt

from ..commons.custom_exception import CustomBadRequest
from ..commons.authentication import AccessTokenAuthentication
from .models import Employee
from .signals import * # noqa
from ..commons.constants import JWT_AUTH


class UserResource(ModelResource):
    """User model resources."""

    class Meta(object):
        """User model resource meta data."""

        queryset = User.objects.all()
        fields = ['username', 'first_name', 'last_name', 'is_active']
        excludes = ['email', 'password', 'is_superuser']
        resource_name = 'auth/users'
        authentication = AccessTokenAuthentication()
        authorization = Authorization()
        always_return_data = True


class MultipartResource(object):
    """Docstring for MultipartResource."""

    def deserialize(self, request, data, format=None):
        """Tastypie dehydrate method."""

        if not format:
            format = request.META.get('CONTENT_TYPE', 'application/json')
        if format == 'application/x-www-form-urlencoded':
            return request.POST
        if format.startswith('multipart'):
            data = request.POST.copy()
            data.update(request.FILES)
            return data
        return super(MultipartResource, self).deserialize(request, data, format)


class FileSizeValidation(Validation):
    """Provide helper function to validation data when uploading image."""

    def is_valid(self, bundle, request=None):
        """Helper function to check bundle data valid or not valid."""

        errors = {}
        if bundle is not None:
            avatar_original = bundle.get('avatar_original')

        if avatar_original:
            if avatar_original.size > 3 * 1024 * 1024:
                errors["file_size"] = ['Image file too large ( > 3MB )']
        else:
            errors["unknown"] = ['Could not read uploaded image']
        return errors


class EmployeeResource(ModelResource):
    """Employee model resources"""

    class Meta(object):
        """Employee model resource meta data."""

        queryset = Employee.objects.all()
        fields = ['first_name', 'last_name', 'age']
        allowed_methods = ['get', 'post', 'put', 'delete']
        resource_name = 'employee'
        authentication = AccessTokenAuthentication()
        authorization = Authorization()
        always_return_data = True
        include_resource_uri = False

    def hydrate(self, bundle):
        """Tastypie hydrate method."""

        employee = User.objects.filter(id=bundle.request.user.id).first()
        bundle.data['user'] = {
            'id': bundle.request.user.id,
            'first_name': employee.first_name,
            'last_name': employee.last_name,
            'email': employee.email
        }

        return super(EmployeeResource, self).hydrate(bundle)

    def dehydrate(self, bundle):
        """Tastypie dehydrate method."""

        bundle.data['user'] = {
            'id': bundle.obj.user.id,
            'name': str(bundle.obj.user.first_name) + " " + str(bundle.obj.user.last_name)
        }

        return bundle

    def prepend_urls(self):
        """Api urls."""

        return [
            url(r"^(?P<resource_name>%s)/young%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('young'), name="api_young_employee"),
            url(r"^(?P<resource_name>%s)/search%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('search'), name="api_search"),
        ]

    def young(self, request, **kwargs):
        """Get all young employees with age from 18-25"""

        self.method_check(request, allowed=['get'])
        self._meta.authentication.is_authenticated(request)

        if 'young_employees' in cache:
            # Get result from cache
            sqs_result = cache.get('young_employees')
        else:
            sqs_result = SearchQuerySet().filter(
                age__range=[18, 25]).models(Employee).load_all()
            cache.set('young_employees', sqs_result, timeout=settings.CACHE_TTL)
        return self.paginator(request, sqs_result)

    def search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self._meta.authentication.is_authenticated(request)
        self.throttle_check(request)

        q = str(request.GET.get('q', ''))
        sqs = SearchQuerySet().filter(email__contains=q).models(Employee).load_all()

        self.log_throttled_access(request)
        return self.paginator(request, sqs)

    def paginator(self, request, objects, **kwargs):
        """Helper function to paginator result list."""

        paginator = self._meta.paginator_class(
            request.GET,
            objects,
            resource_uri=self.get_resource_uri(),
            limit=self._meta.limit,
            max_limit=self._meta.max_limit,
            collection_name=self._meta.collection_name)
        to_be_serialized = paginator.page()

        # Dehydrate the bundles in preparation for serialization.
        bundles = [self.full_dehydrate(
            self.build_bundle(obj=obj.object, request=request))
            for obj in to_be_serialized[self._meta.collection_name]]

        to_be_serialized[self._meta.collection_name] = [
            self.full_dehydrate(bundle) for bundle in bundles]
        to_be_serialized = self.alter_list_data_to_serialize(request, to_be_serialized)
        return self.create_response(request, to_be_serialized)


class AuthenticationResource(MultipartResource, ModelResource):
    """Authentication resource."""

    class Meta(object):
        """Meta data."""

        allowed_methods = ['get', 'post']
        always_return_data = True
        authentication = AccessTokenAuthentication()
        authorization = Authorization()
        queryset = User.objects.all()
        resource_name = 'authentication'
        fields = ['username', 'email', 'password']
        validation = FileSizeValidation()

    def prepend_urls(self):
        """Api urls."""

        return [
            url(r"^(?P<resource_name>%s)/sign_in%s$" % (
                self._meta.resource_name,
                trailing_slash()),
                self.wrap_view('sign_in'), name="api_sign_in"),
            url(r"^(?P<resource_name>%s)/sign_up%s$" % (
                self._meta.resource_name,
                trailing_slash()),
                self.wrap_view('sign_up_by_email'), name="api_sign_up_by_email"),
            url(r"^(?P<resource_name>%s)/sign_out%s$" % (
                self._meta.resource_name,
                trailing_slash()),
                self.wrap_view('sign_out'), name="api_sign_out"),
            url(r"^(?P<resource_name>%s)/getuserinfo%s$" % (
                self._meta.resource_name,
                trailing_slash()),
                self.wrap_view('get_user_info'), name="api_get_user_info"),
            url(r"^(?P<resource_name>%s)/update_avatar%s$" % (
                self._meta.resource_name,
                trailing_slash()),
                self.wrap_view('update_avatar'), name="api_update_avatar"),
        ]

    def sign_in(self, request, **kwargs):
        """Sign in api handler."""

        self.method_check(request, allowed=['post'])
        data = self.deserialize(
            request,
            request.body,
            format=request.META.get('CONTENT_TYPE', 'application/join'))
        retype_password = data.get('retype_password', None)
        if retype_password is not None:
            return self.sign_up_by_email(request, **kwargs)
        elif 'email' in data and 'password' in data:
            return self.sign_in_by_email(request, **kwargs)
        else:
            raise CustomBadRequest(error_type='UNAUTHORIZED')

    def sign_in_by_email(self, request, **kwargs):
        """Sign in by email api handler."""

        data = self.deserialize(
            request,
            request.body,
            format=request.META.get('CONTENT_TYPE', 'application/join'))
        email = data.get('email', '')
        password = data.get('password', '')
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                if user.is_active:
                    user = authenticate(username=email, password=password)
                    login(request, user)
                    access_token = None
                    # access_token, created = Token.objects.get_or_create(user=user)
                    payload = {
                        'user_id': user.id,
                        'exp': datetime.utcnow() + timedelta(
                            seconds=JWT_AUTH.get('JWT_EXP_DELTA_SECONDS'))
                    }
                    access_token = jwt.encode(
                        payload,
                        JWT_AUTH.get('JWT_SECRET'),
                        JWT_AUTH.get('JWT_ALGORITHM'))
                    apikey = ApiKey.objects.filter(user=user).first()
                    return self.create_auth_response(
                        request=request,
                        user=user,
                        api_key=apikey.key,
                        access_token=access_token)
                else:
                    raise CustomBadRequest(
                        error_type='UNAUTHORIZED',
                        error_message='Your email is not verified')
            else:
                raise CustomBadRequest(
                    error_type='UNAUTHORIZED',
                    error_message='Your password is not correct')
        except User.DoesNotExist:
            raise CustomBadRequest(
                error_type='UNAUTHORIZED',
                error_message='Your email address is not registered. Please register')

    def sign_up_by_email(self, request, **kwargs):
        """Sign up by email handler."""

        self.method_check(request, allowed=['post'])
        data = self.deserialize(
            request,
            request.body,
            format=request.META.get('CONTENT_TYPE', 'application/join'))
        return self.create_user(request, data)

    def create_user(self, request, data):
        """Provice helper funtion for create user."""

        email = data.get('email', '')
        password = data.get('password', '')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        age = data.get('age', '')

        # Remove space letters in last_name and first_name
        if last_name:
            last_name = last_name.strip()
        if first_name:
            first_name = first_name.strip()

        # Check email exist in system.
        if User.objects.filter(email__iexact=email).exists():
            raise CustomBadRequest(
                error_type='DUPLICATE_VALUE',
                field='email',
                obj='email')
        else:
            try:
                with transaction.atomic():

                    # Create user with paramaters
                    User.objects.create_user(
                        username=email,
                        email=email,
                        password=password,
                        first_name=first_name,
                        last_name=last_name)

                    user = authenticate(username=email, password=password)

                    login(request, user)

                    if user is not None:
                        # Create employee
                        self.create_employee(user.id, age=age)

                        apikey = ApiKey.objects.filter(user=user).first()
                        access_token = None

                        # Will create access_token when user has is_active = True
                        # Else is_active = False will send notifi to user
                        if not user.is_active:
                            self.create_response(
                                request,
                                {'success': False},
                                HttpUnauthorized)
                        else:
                            # access_token, created = Token.objects.get_or_create(user=user)
                            payload = {
                                'user_id': user.id,
                                'exp': datetime.utcnow() + timedelta(
                                    seconds=JWT_AUTH.get('JWT_EXP_DELTA_SECONDS'))
                            }
                            access_token = jwt.encode(
                                payload,
                                JWT_AUTH.get('JWT_SECRET'),
                                JWT_AUTH.get('JWT_ALGORITHM'))

                        Employee.objects.filter(user__id=user.id).update(
                            first_name=first_name,
                            last_name=last_name)

                        if access_token is not None:
                            return self.create_auth_response(
                                request=request,
                                user=user,
                                api_key=apikey.key,
                                access_token=access_token)
                        else:
                            return self.create_auth_response(
                                request=request,
                                user=user,
                                api_key=apikey.key,
                                access_token=access_token)
                    else:
                        raise CustomBadRequest(
                            error_type='UNKNOWN_ERROR',
                            error_message='Cant sign up by this email.')
            except ValueError as e:
                raise CustomBadRequest(error_type='UNKNOWN_ERROR', error_message=str(e))

    def sign_out(self, request, **kwargs):
        """Sign out handler."""

        self._meta.authentication.is_authenticated(request)
        self.method_check(request, allowed=['post', 'get'])
        access_token = self._meta.authentication.extract_credentials(request)
        user = self.logout(request, access_token)
        request.user = user
        if request.user and request.user.is_authenticated:
            logout(request)
            return self.create_response(request, {'success': True})
        else:
            return self.create_response(request, {'success': False}, HttpUnauthorized)

    def create_employee(self, user_id, **kwargs):
        """Create blank employee profile base on user_id."""

        # Add the user_id to kwargs
        kwargs['user_id'] = user_id

        # Create employee
        employee, _ = Employee.objects.get_or_create(user__id=user_id, defaults=kwargs)

        if employee is None:
            raise CustomBadRequest(
                error_type='UNKNOWNERROR',
                error_message="Can't create employee")

    def logout(self, request, access_token, **kwargs):
        """Support api to get user."""

        if access_token is not None:
            # Try get payload from access_token
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
                return user
            except User.DoesNotExist:
                raise CustomBadRequest(
                    error_type='INVALID_DATA',
                    error_message='Can not get user with access token')
        else:
            raise CustomBadRequest(
                error_type='UNLOGIN',
                error_message='Please add access token to request paramater')

    def create_auth_response(self, request, user, api_key, access_token=None):
        """Genetate response data for authentication process."""

        employee = Employee.objects.get(id=user.employee.id)

        resource_instance = EmployeeResource()
        bundle = resource_instance.full_hydrate(
            resource_instance.build_bundle(obj=employee, request=request))
        bundle.data['user']['api_key'] = api_key

        if access_token:
            bundle.data['user']['access_token'] = access_token
        return self.create_response(request, bundle)

    def update_avatar(self, request, **kwargs):
        """The api update avatar for employee."""

        self.method_check(request, allowed=['post', 'put'])
        self._meta.authentication.is_authenticated(request)
        data = self.deserialize(
            request,
            request.body,
            format=request.META.get('CONTENT_TYPE', 'application/join'))

        # Check validation for image (size and missed content types)
        validation = FileSizeValidation()
        errors = validation.is_valid(data)
        if errors:
            raise CustomBadRequest(error_type='INVALID_DATA',
                                   error_message=errors)

        if data is not None:
            avatar_original = data.get('avatar_original')
        else:
            raise CustomBadRequest(
                error_type='Authorization',
                error_message='Can not get data from request')

        employee = Employee.objects.get(user__id=request.user.id)

        try:
            employee.avatar_original = avatar_original
            employee.save()
        except IntegrityError:
            raise CustomBadRequest(
                error_type='Database',
                error_message='Can not create file')
        return self.create_response(request, {'success': True})
