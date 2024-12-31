from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import LoanApplication, LoanRepayment, Subscription, Invoice
import datetime

@receiver(post_save, sender=LoanApplication)
def create_loan_repayments(sender, instance, created, **kwargs):
    """
    create_loan_repayments function for the LoanApplication model.
    """
    if created and instance.status == 'APPROVED':
        # Create repayment schedule
        monthly_amount = instance.amount / instance.term_months
        for month in range(instance.term_months):
            due_date = instance.created_at.date() + datetime.timedelta(days=30 * (month + 1))
            LoanRepayment.objects.create(
                loan=instance,
                amount=monthly_amount,
                due_date=due_date
            )

@receiver(post_save, sender=Subscription)
def create_invoice(sender, instance, created, **kwargs):
    """
    create_invoice function for the Subscription model.
    """
    if created:
        Invoice.objects.create(
            company=instance.company,
            subscription=instance,
            amount=instance.price_per_month,
            issue_date=timezone.now().date(),
            due_date=timezone.now().date() + datetime.timedelta(days=30)
        )
