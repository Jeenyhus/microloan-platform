from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):
    """
    User model for the microloan platform.

    Attributes:
        phone_number (str): The phone number of the user.
        is_company_admin (bool): Whether the user is a company admin.
        company (Company): The company the user belongs to.
    """
    phone_number = models.CharField(max_length=20, blank=True)
    is_company_admin = models.BooleanField(default=False)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True, blank=True)

class Company(models.Model):
    """
    Company model for the microloan platform.

    Attributes:
        name (str): The name of the company.
        registration_number (str): The registration number of the company.
        address (str): The address of the company.
        created_at (datetime): The date and time the company was created.
        is_active (bool): Whether the company is active.
    """
    name = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=100, unique=True)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Subscription(models.Model):
    """
    Subscription model for the microloan platform.

    Attributes:
        company (Company): The company the subscription belongs to.
        plan (str): The plan the company has subscribed to.
        start_date (datetime): The date and time the subscription started.
        end_date (datetime): The date and time the subscription ends.
        is_active (bool): Whether the subscription is active.
        max_users (int): The maximum number of users the company can have.
        price_per_month (decimal): The price per month for the subscription.
    """
    PLAN_CHOICES = [
        ('BASIC', 'Basic'),
        ('PRO', 'Professional'),
        ('ENTERPRISE', 'Enterprise'),
    ]
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    max_users = models.IntegerField()
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2)

class LoanApplication(models.Model):
    """
    LoanApplication model for the microloan platform.

    Attributes:
        company (Company): The company the loan application belongs to.
        loan_officer (User): The loan officer who is handling the loan application.
        applicant_name (str): The name of the applicant.
        amount (decimal): The amount of the loan.
        interest_rate (decimal): The interest rate for the loan.
        term_months (int): The term of the loan in months.
        status (str): The status of the loan application.
        created_at (datetime): The date and time the loan application was created.
        updated_at (datetime): The date and time the loan application was last updated.
    """
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('DISBURSED', 'Disbursed'),
    ]
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    loan_officer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    applicant_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    term_months = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class LoanRepayment(models.Model):
    """
    LoanRepayment model for the microloan platform.

    Attributes:
        loan (LoanApplication): The loan the repayment belongs to.
        amount (decimal): The amount of the repayment.
        due_date (date): The date the repayment is due.
        paid_date (date): The date the repayment was paid.
        is_paid (bool): Whether the repayment has been paid.
    """
    loan = models.ForeignKey(LoanApplication, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)

class AuditLog(models.Model):
    """
    AuditLog model for the microloan platform.

    Attributes:
        user (User): The user the audit log belongs to.
        company (Company): The company the audit log belongs to.
        action (str): The action that was performed.
        timestamp (datetime): The date and time the action was performed.
        details (JSON): The details of the action.
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.JSONField()

class Invoice(models.Model):
    """
    Invoice model for the microloan platform.

    Attributes:
        company (Company): The company the invoice belongs to.
        subscription (Subscription): The subscription the invoice belongs to.
        amount (decimal): The amount of the invoice.
        issue_date (date): The date the invoice was issued.
        due_date (date): The date the invoice is due.
        paid_date (date): The date the invoice was paid.
        is_paid (bool): Whether the invoice has been paid.
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    issue_date = models.DateField()
    due_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)