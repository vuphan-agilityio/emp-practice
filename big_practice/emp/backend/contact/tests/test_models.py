from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Contact


class DepartmentModelsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'test@gmail.com', 'testpassword')

    def test_create_new_contact_user(self):
        contact = Contact.objects.create(user=self.user, address='604 Nui Thanh, Da Nang')
        self.assertTrue(contact)

    def test_default_string_contact(self):
        self.test_create_new_contact_user()
        contact = Contact.objects.get(user=self.user)
        self.assertTrue('604 Nui Thanh, Da Nang', contact.__str__())
