from django.core.exceptions import ValidationError
from django.utils import timezone

def validate_future_date(value):
    if value < timezone.now().date():
        raise ValidationError('Date cannot be in the past.')

def validate_phone_number(value):
    if not value.isdigit() or len(value) < 10:
        raise ValidationError('Invalid phone number format.')

def validate_loan_amount(value):
    if value <= 0:
        raise ValidationError('Loan amount must be greater than zero.') 