from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from core.models import User, Company, LoanApplication
from decimal import Decimal

class LoanApplicationTests(APITestCase):
    def setUp(self):
        self.company = Company.objects.create(
            name="Test Company",
            registration_number="12345"
        )
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            company=self.company,
            is_company_admin=True
        )
        self.client.force_authenticate(user=self.user)

    def test_create_loan_application(self):
        url = reverse('loan-application-list')
        data = {
            'company': self.company.id,
            'applicant_name': "John Doe",
            'amount': "5000.00",
            'interest_rate': "5.00",
            'term_months': 12
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LoanApplication.objects.count(), 1) 