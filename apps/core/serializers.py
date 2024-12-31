from rest_framework import serializers
from .models import User, Company, Subscription, LoanApplication, LoanRepayment, Invoice

class UserSerializer(serializers.ModelSerializer):
    """
    UserSerializer class for the User model.
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone_number', 'is_company_admin', 'company')
        read_only_fields = ('id',)

class CompanySerializer(serializers.ModelSerializer):
    """
    CompanySerializer class for the Company model.
    """
    total_users = serializers.IntegerField(read_only=True)
    active_loans = serializers.IntegerField(read_only=True)

    class Meta:
        model = Company
        fields = ('id', 'name', 'registration_number', 'address', 'is_active', 
                 'created_at', 'total_users', 'active_loans')
        read_only_fields = ('id', 'created_at')

class SubscriptionSerializer(serializers.ModelSerializer):
    """
    SubscriptionSerializer class for the Subscription model.
    """
    class Meta:
        model = Subscription
        fields = '__all__'
        read_only_fields = ('id',)

class LoanApplicationSerializer(serializers.ModelSerializer):
    """
    LoanApplicationSerializer class for the LoanApplication model.
    """
    loan_officer_name = serializers.CharField(source='loan_officer.username', read_only=True)
    repayment_progress = serializers.FloatField(read_only=True)

    class Meta:
        model = LoanApplication
        fields = ('id', 'company', 'loan_officer', 'loan_officer_name', 'applicant_name',
                 'amount', 'interest_rate', 'term_months', 'status', 'created_at',
                 'updated_at', 'repayment_progress')
        read_only_fields = ('id', 'created_at', 'updated_at')

class LoanRepaymentSerializer(serializers.ModelSerializer):
    """
    LoanRepaymentSerializer class for the LoanRepayment model.
    """
    class Meta:
        model = LoanRepayment
        fields = '__all__'
        read_only_fields = ('id',)

class InvoiceSerializer(serializers.ModelSerializer):
    """
    InvoiceSerializer class for the Invoice model.
    """
    class Meta:
        model = Invoice
        fields = '__all__'
        read_only_fields = ('id',)
