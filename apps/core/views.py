from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from django.db.models import Count, Sum, Q, F
from django.utils import timezone
from .models import User, Company, Subscription, LoanApplication, LoanRepayment, Invoice
from .serializers import (UserSerializer, CompanySerializer, SubscriptionSerializer,
                         LoanApplicationSerializer, LoanRepaymentSerializer, InvoiceSerializer)

@api_view(['GET'])
def test_view(request):
    """
    Test view for the microloan platform.
    """
    return Response({"message": "Hello from Django!"})

class UserViewSet(viewsets.ModelViewSet):
    """
    UserViewSet class for the User model.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(company=self.request.user.company)

class CompanyViewSet(viewsets.ModelViewSet):
    """
    CompanyViewSet class for the Company model.
    """
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Company.objects.annotate(
            total_users=Count('user'),
            active_loans=Count('loanapplication', filter=Q(loanapplication__status='APPROVED'))
        )
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(id=self.request.user.company.id)

class SubscriptionViewSet(viewsets.ModelViewSet):
    """
    SubscriptionViewSet class for the Subscription model.
    """
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Subscription.objects.all()
        return Subscription.objects.filter(company=self.request.user.company)

class LoanApplicationViewSet(viewsets.ModelViewSet):
    """
    LoanApplicationViewSet class for the LoanApplication model.
    """
    serializer_class = LoanApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = LoanApplication.objects.annotate(
            repayment_progress=Sum('loanrepayment__amount', filter=Q(loanrepayment__is_paid=True)) / F('amount') * 100
        )
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(company=self.request.user.company)

    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        loan = self.get_object()
        new_status = request.data.get('status')
        if new_status not in dict(LoanApplication.STATUS_CHOICES):
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        loan.status = new_status
        loan.save()
        return Response(self.get_serializer(loan).data)

class LoanRepaymentViewSet(viewsets.ModelViewSet):
    """
    LoanRepaymentViewSet class for the LoanRepayment model.
    """
    serializer_class = LoanRepaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return LoanRepayment.objects.all()
        return LoanRepayment.objects.filter(loan__company=self.request.user.company)

    @action(detail=True, methods=['post'])
    def mark_as_paid(self, request, pk=None):
        repayment = self.get_object()
        repayment.is_paid = True
        repayment.paid_date = timezone.now()
        repayment.save()
        return Response(self.get_serializer(repayment).data)

class InvoiceViewSet(viewsets.ModelViewSet):
    """
    InvoiceViewSet class for the Invoice model.
    """
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Invoice.objects.all()
        return Invoice.objects.filter(company=self.request.user.company)