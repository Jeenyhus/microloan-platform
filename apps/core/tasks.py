from celery import shared_task
from django.utils import timezone
from .models import LoanRepayment, Subscription
from .utils import send_email_notification, send_sms_notification

@shared_task
def check_overdue_repayments():
    """
    check_overdue_repayments function for checking overdue repayments.
    """
    overdue_repayments = LoanRepayment.objects.filter(
        is_paid=False,
        due_date__lt=timezone.now().date()
    )
    
    for repayment in overdue_repayments:
        send_email_notification(
            subject='Overdue Loan Repayment',
            message=f'Loan repayment of {repayment.amount} is overdue',
            recipient_list=[repayment.loan.loan_officer.email]
        )

@shared_task
def check_subscription_expiry():
    """
    check_subscription_expiry function for checking subscription expiry.
    """
    expiring_soon = Subscription.objects.filter(
        end_date__lte=timezone.now() + timezone.timedelta(days=7),
        is_active=True
    )
    
    for subscription in expiring_soon:
        send_email_notification(
            subject='Subscription Expiring Soon',
            message=f'Your subscription will expire on {subscription.end_date}',
            recipient_list=[admin.email for admin in subscription.company.user_set.filter(is_company_admin=True)]
        )
