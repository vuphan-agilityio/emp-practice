"""emp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from tastypie.api import Api

from backend.account.api import EmployeeResource, AuthenticationResource
from backend.contact.api import ContactResource
from backend.department.api import DepartmentResource

v1_api = Api(api_name='v1')
v1_api.register(EmployeeResource())
v1_api.register(ContactResource())
v1_api.register(DepartmentResource())
v1_api.register(AuthenticationResource())

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^api/', include(v1_api.urls)),
]
