from django.conf.urls import url
from django.contrib.auth.models import User
from django.db import IntegrityError

from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.utils import trailing_slash

from haystack.query import SearchQuerySet

from ..commons.authentication import AccessTokenAuthentication
from ..commons.custom_exception import CustomBadRequest
from .models import Contact


class ContactResource(ModelResource):
    """Contact model resources"""

    class Meta(object):
        """Contact model resource meta data."""

        queryset = Contact.objects.all()
        fields = ['address']
        allowed_methods = ['get', 'post', 'put', 'delete']
        resource_name = 'contact'
        authentication = AccessTokenAuthentication()
        authorization = Authorization()
        always_return_data = True
        include_resource_uri = False

    def prepend_urls(self):
        """Api urls."""

        return [
            url(r"^(?P<resource_name>%s)/search%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('search'), name="api_search_contact")
        ]

    def search(self, request, **kwargs):
        """Search contact by username."""

        self.method_check(request, allowed=['get'])
        self._meta.authentication.is_authenticated(request)
        self.throttle_check(request)

        q = str(request.GET.get('q', ''))
        sqs = SearchQuerySet().filter(username__contains=q).models(Contact).load_all()

        self.log_throttled_access(request)
        return self.paginator(request, sqs)

    def obj_create(self, bundle, **kwargs):
        """Customize api create new."""

        self.method_check(bundle.request, allowed=['post', 'put'])
        self._meta.authentication.is_authenticated(bundle.request)
        data = self.deserialize(
            bundle.request,
            bundle.request.body,
            format=bundle.request.META.get('CONTENT_TYPE', 'application/join'))
        if data is not None:
            user_target_id = data.get('user_target_id', None)
            address = data.get('address', '')
        else:
            raise CustomBadRequest(
                error_type='Authorization',
                error_message='Can not get data from request')

        try:
            user_email = bundle.request.user
            user_assign = User.objects.get(email=user_email)
            user_target = User.objects.get(pk=user_target_id)
        except User.DoesNotExist:
            raise CustomBadRequest(
                error_type='Database',
                error_message='Can not get user from database')


        try:
            contact = Contact.objects.create(
                address=address,
                created_by=user_assign,
                user=user_target)
            bundle.obj = contact
        except IntegrityError:
            raise CustomBadRequest(
                error_type='Database',
                error_message='Can not create contact')
        return bundle

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
            self.build_bundle(obj=obj.object, request=request),
            for_list=True)
            for obj in to_be_serialized[self._meta.collection_name]]

        to_be_serialized[self._meta.collection_name] = [
            self.full_dehydrate(bundle) for bundle in bundles]
        to_be_serialized = self.alter_list_data_to_serialize(request, to_be_serialized)
        return self.create_response(request, to_be_serialized)
