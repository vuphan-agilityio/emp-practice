from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Employee
from backend.department.models import Department


class AccountModelsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'test@gmail.com', 'testpassword')
        self.department = Department.objects.create(name='department')

    def test_create_new_employee(self):
        employee = Employee.objects.create(
            user=self.user,
            department=self.department,
            age=23)
        self.assertTrue(employee)

    def test_get_employees_with_age_great_more_than_25(self):
        employee = Employee.objects.with_age_great_more_than_25()
        employee_result = Employee.objects.filter(age__gt=25)
        self.assertFalse(employee, employee_result)

    def test_can_get_avg_age_of_employees(self):
        employee = Employee.objects.with_aggregate_avg_age_of_employees()
        self.assertTrue(employee)

    def test_with_raw_sql_get_employees_has_status_code_is_true(self):
        employee = Employee.objects.with_raw_sql_get_employees_has_status_code_is_true()
        self.assertFalse(employee)

    def test_with_raw_sql_get_employees_get_age_great_more_than_25(self):
        employee = Employee.objects.with_raw_sql_get_employees_get_age_great_more_than_25()
        self.assertFalse(employee)

    def test_with_raw_sql_get_avg_of_employees(self):
        employee = Employee.objects.with_raw_sql_get_avg_of_employees()
        self.assertTrue(employee)

    def test_can_get_full_name(self):
        self.test_create_new_employee()
        employee = Employee.objects.get(user=self.user)
        full_name = employee.full_name()
        self.assertTrue(' ', full_name)

    def test_default_string_of_employee(self):
        self.test_create_new_employee()
        employee = Employee.objects.get(user=self.user)
        self.assertTrue('test@gmail.com', employee.__str__())
