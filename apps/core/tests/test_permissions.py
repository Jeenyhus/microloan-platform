from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from core.models import User, Company
from core.permissions import IsCompanyAdmin, IsCompanyMember

class PermissionTests(APITestCase):
    def setUp(self):
        self.company = Company.objects.create(
            name="Test Company",
            registration_number="12345"
        )
        self.admin_user = User.objects.create_user(
            username="admin",
            password="admin123",
            company=self.company,
            is_company_admin=True
        )
        self.regular_user = User.objects.create_user(
            username="user",
            password="user123",
            company=self.company,
            is_company_admin=False
        )

    def test_company_admin_access(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('company-detail', args=[self.company.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_regular_user_restricted_access(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('company-detail', args=[self.company.id])
        response = self.client.patch(url, {'name': 'New Name'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) 