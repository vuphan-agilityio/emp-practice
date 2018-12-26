from datetime import datetime, timedelta

from django.test import TestCase
from django.contrib.auth.models import User
from tastypie.test import ResourceTestCaseMixin

import jwt

from ..models import Contact
from backend.account.models import Employee
from backend.commons.constants import JWT_AUTH


class ContactResourceTestCase(ResourceTestCaseMixin, TestCase):
    """Test suite for the api Contact."""

    def setUp(self):
        """Define the test client and other test variables."""

        super(ContactResourceTestCase, self).setUp()

        # Create a user.
        self.password = 'password'
        self.email = 'unittest@unittest.com'
        self.user = User.objects.create_user(
            self.email,
            self.email,
            self.password)

        # Create new employee by user created
        self.employee = Employee.objects.create(
            user=self.user,
            first_name='Unit',
            last_name='Test',
            age=23)

        # Create new access token with user created
        self.payload = {
            'user_id': self.user.id,
            'exp': datetime.utcnow() + timedelta(
                seconds=JWT_AUTH.get('JWT_EXP_DELTA_SECONDS'))
        }
        self.access_token = jwt.encode(
            self.payload,
            JWT_AUTH.get('JWT_SECRET'),
            JWT_AUTH.get('JWT_ALGORITHM'))

        self.post_data = {
            'address': '604 Nui Thanh, Da Nang',
            'user_target_id': self.user.id
        }

    def get_credentials(self):
        return self.access_token

    def test_api_can_search_contact_by_name(self):
        """Test the api search contact by name."""

        self.assertHttpOK(self.api_client.get(
            '/api/v1/contact/search?q=vu',
            format='json',
            authentication=self.get_credentials()
        ))

    def test_api_create_new_contact(self):
        """Test the api create new contact."""

        # Check how many are there first.
        self.assertEqual(Contact.objects.count(), 0)
        self.assertHttpCreated(self.api_client.post(
            '/api/v1/contact/',
            format='json',
            data=self.post_data,
            authentication=self.get_credentials()
        ))
        # Verify a new one has been added.
        self.assertEqual(Contact.objects.count(), 1)

    def test_api_get_detail_unauthenticated(self):
        """Test the api get detail with unauthenticated."""

        self.assertHttpBadRequest(self.api_client.get(
            '/api/v1/contact/1/',
            format='json'
        ))

    def test_api_get_detail_with_access_token_is_invalid(self):
        """Test the api get detail with the access token is invalid."""

        self.assertHttpBadRequest(self.api_client.get(
            '/api/v1/contact/1/',
            format='json',
            authentication='invalidtoken'
        ))
