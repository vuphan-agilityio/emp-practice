from django.conf.urls import url

from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.utils import trailing_slash

from haystack.query import SearchQuerySet

from ..commons.authentication import AccessTokenAuthentication
from .models import Department


class DepartmentResource(ModelResource):
    """Department model resources"""

    class Meta(object):
        """Department model resource meta data."""

        queryset = Department.objects.all()
        fields = ['name']
        allowed_methods = ['get', 'post', 'put', 'delete']
        resource_name = 'department'
        authentication = AccessTokenAuthentication()
        authorization = Authorization()
        always_return_data = True
        include_resource_uri = False

    def prepend_urls(self):
        """Api urls."""

        return [
            url(r"^(?P<resource_name>%s)/search%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('search'), name="api_search_department")
        ]

    def search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self._meta.authentication.is_authenticated(request)
        self.throttle_check(request)

        q = str(request.GET.get('q', ''))
        sqs = SearchQuerySet().filter(name__contains=q).models(Department).load_all()

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
            self.build_bundle(obj=obj.object, request=request),
            for_list=True)
            for obj in to_be_serialized[self._meta.collection_name]]

        to_be_serialized[self._meta.collection_name] = [
            self.full_dehydrate(bundle) for bundle in bundles]
        to_be_serialized = self.alter_list_data_to_serialize(request, to_be_serialized)
        return self.create_response(request, to_be_serialized)
