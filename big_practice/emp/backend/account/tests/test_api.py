from datetime import datetime, timedelta

from django.test import TestCase
from django.contrib.auth.models import User
from tastypie.test import ResourceTestCaseMixin

import jwt

from ..models import Employee
from backend.commons.constants import JWT_AUTH


class AuthenticationResourceTestCase(ResourceTestCaseMixin, TestCase):
    """Test suite for the api Authentication."""

    def setUp(self):
        """Define the test client and other test variables."""

        super(AuthenticationResourceTestCase, self).setUp()

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

        self.request_body_sign_in_with_incorrect_email = {
            'email': 'incorrect_email@gmail.com',
            'password': self.password
        }

        self.request_body_sign_in_with_incorrect_password = {
            'email': self.email,
            'password': 'incorrect_password'
        }

    def get_credentials(self):
        return self.access_token

    def test_api_can_sign_up_an_account(self):
        """Test the api sign up an account"""

        # Check how many are there first.
        self.assertEqual(Employee.objects.count(), 1)
        self.assertHttpOK(self.api_client.post(
            '/api/v1/authentication/sign_up/',
            format='json',
            data=self.post_data))
        # Verify a new one has been added.
        self.assertEqual(Employee.objects.count(), 2)

    def test_api_can_sign_in_with_email_and_password(self):
        """Test the api sign in with email and password in request body."""

        self.assertHttpOK(self.api_client.post(
            '/api/v1/authentication/sign_in/',
            format='json',
            data=self.request_body_sign_in
        ))

    def test_api_can_sign_out_with_access_token(self):
        """Test the api sign out with access token of user."""

        self.assertHttpOK(self.api_client.get(
            '/api/v1/authentication/sign_out/',
            format='json',
            authentication=self.get_credentials()
        ))

    def test_api_sign_in_with_incorrect_email(self):
        """Test the api sign in with incorrect email."""

        self.assertHttpBadRequest(self.api_client.post(
            '/api/v1/authentication/sign_in/',
            format='json',
            data=self.request_body_sign_in_with_incorrect_email
        ))

    def test_api_sign_in_with_incorrect_password(self):
        """Test the api sign in with incorrect password."""

        self.assertHttpBadRequest(self.api_client.post(
            '/api/v1/authentication/sign_in/',
            format='json',
            data=self.request_body_sign_in_with_incorrect_password
        ))

    def test_exception_api_sign_up_with_email_registered(self):
        """Test exception api sign up when sign up with email registered."""

        # Registering account
        self.test_api_can_sign_up_an_account()

        self.assertHttpBadRequest(self.api_client.post(
            '/api/v1/authentication/sign_up/',
            format='json',
            data=self.post_data))


class EmployeeResourceTestCase(ResourceTestCaseMixin, TestCase):
    """The test suite for the api Empoloyee."""

    def setUp(self):
        """Define the test client and other test variables."""

        super(EmployeeResourceTestCase, self).setUp()

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

    def test_api_can_get_young_employees(self):
        """Test the api young employees can get employees got age from 18-25."""

        self.assertHttpOK(self.api_client.get(
            '/api/v1/employee/young/',
            format='json',
            authentication=self.get_credentials()
        ))

    def test_api_can_search_employee_by_name(self):
        """Test the api search employee by name."""

        self.assertHttpOK(self.api_client.get(
            '/api/v1/employee/search?q=vu',
            format='json',
            authentication=self.get_credentials()
        ))
