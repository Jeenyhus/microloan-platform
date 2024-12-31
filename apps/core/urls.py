from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'companies', views.CompanyViewSet, basename='company')
router.register(r'subscriptions', views.SubscriptionViewSet, basename='subscription')
router.register(r'loan-applications', views.LoanApplicationViewSet, basename='loan-application')
router.register(r'loan-repayments', views.LoanRepaymentViewSet, basename='loan-repayment')
router.register(r'invoices', views.InvoiceViewSet, basename='invoice')

urlpatterns = [
    path('api/', include(router.urls)),
]
