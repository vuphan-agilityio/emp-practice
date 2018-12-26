from datetime import datetime, timedelta

from django.test import TestCase
from django.contrib.auth.models import User
from tastypie.test import ResourceTestCaseMixin

import jwt

from backend.account.models import Employee
from backend.commons.constants import JWT_AUTH


class DepartmentResourceTestCase(ResourceTestCaseMixin, TestCase):
    """Test suite for the api Department."""

    def setUp(self):
        """Define the test client and other test variables."""

        super(DepartmentResourceTestCase, self).setUp()

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
            'email': 'unit_test@unittest.com',
            'password': 'testpassword',
            'retype_password': 'testpassword',
            'first_name': 'Unit',
            'last_name': 'Test',
            'age': 23
        }

        self.request_body_sign_in = {
            'email': self.email,
            'password': self.password
        }

    def get_credentials(self):
        return self.access_token

    def test_api_can_search_department_by_name(self):
        """Test the api search department by name."""

        self.assertHttpOK(self.api_client.get(
            '/api/v1/department/search?q=vu',
            format='json',
            authentication=self.get_credentials()
        ))
