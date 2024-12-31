from django.test import TestCase
from django.utils import timezone
from core.models import User, Company, Subscription, LoanApplication
from decimal import Decimal

class CompanyTests(TestCase):
    def setUp(self):
        self.company = Company.objects.create(
            name="Test Company",
            registration_number="12345",
            address="Test Address"
        )

    def test_company_creation(self):
        self.assertEqual(self.company.name, "Test Company")
        self.assertTrue(self.company.is_active)

class UserTests(TestCase):
    def setUp(self):
        self.company = Company.objects.create(
            name="Test Company",
            registration_number="12345"
        )
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            company=self.company,
            is_company_admin=True
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, "test@example.com")
        self.assertTrue(self.user.is_company_admin)
        self.assertEqual(self.user.company, self.company) 