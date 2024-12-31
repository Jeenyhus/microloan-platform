from django.core.mail import send_mail
from django.conf import settings
import requests

def send_sms_notification(phone_number, message):
    """
    send_sms_notification function for sending SMS notifications.
    """
    # Implement your SMS gateway integration here
    pass

def send_email_notification(subject, message, recipient_list):
    """
    send_email_notification function for sending email notifications.
    """
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
    )

def calculate_loan_metrics(loan):
    """
    calculate_loan_metrics function for calculating loan metrics.
    """
    total_paid = loan.loanrepayment_set.filter(is_paid=True).aggregate(Sum('amount'))['amount__sum'] or 0
    total_due = loan.amount
    progress = (total_paid / total_due) * 100 if total_due > 0 else 0
    return {
        'total_paid': total_paid,
        'total_due': total_due,
        'progress': progress,
        'remaining': total_due - total_paid
    }
