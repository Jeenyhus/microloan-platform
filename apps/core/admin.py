from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.db.models import Sum, Count
from .models import User, Company, Subscription, LoanApplication, LoanRepayment, AuditLog, Invoice
from django.utils import timezone
import json

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    CustomUserAdmin class for the User model.
    """
    list_display = ('username', 'email', 'company', 'is_company_admin', 'is_active', 'last_login')
    list_filter = ('is_company_admin', 'company', 'is_active', 'last_login')
    fieldsets = UserAdmin.fieldsets + (
        ('Company Information', {'fields': ('phone_number', 'company', 'is_company_admin')}),
    )
    actions = ['activate_users', 'deactivate_users']

    def activate_users(self, request, queryset):
        queryset.update(is_active=True)
    activate_users.short_description = "Activate selected users"

    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_users.short_description = "Deactivate selected users"

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """
    CompanyAdmin class for the Company model.
    """
    list_display = ('name', 'registration_number', 'is_active', 'created_at', 'total_users', 'active_loans')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'registration_number')
    readonly_fields = ('created_at',)
    actions = ['activate_companies', 'deactivate_companies']

    def total_users(self, obj):
        return obj.user_set.count()
    total_users.short_description = 'Total Users'

    def active_loans(self, obj):
        return obj.loanapplication_set.filter(status='APPROVED').count()
    active_loans.short_description = 'Active Loans'

    def activate_companies(self, request, queryset):
        queryset.update(is_active=True)
    activate_companies.short_description = "Activate selected companies"

    def deactivate_companies(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_companies.short_description = "Deactivate selected companies"

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """
    SubscriptionAdmin class for the Subscription model.
    """
    list_display = ('company', 'plan', 'start_date', 'end_date', 'is_active', 'max_users', 'subscription_status')
    list_filter = ('plan', 'is_active', 'start_date')
    search_fields = ('company__name',)
    readonly_fields = ('subscription_status',)

    def subscription_status(self, obj):
        if not obj.is_active:
            return format_html('<span style="color: red;">Inactive</span>')
        if obj.end_date < timezone.now():
            return format_html('<span style="color: orange;">Expired</span>')
        return format_html('<span style="color: green;">Active</span>')
    subscription_status.short_description = 'Status'

@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    """
    LoanApplicationAdmin class for the LoanApplication model.
    """
    list_display = ('company', 'loan_officer', 'applicant_name', 'amount', 'status', 'created_at', 'loan_progress')
    list_filter = ('status', 'company', 'created_at')
    search_fields = ('applicant_name', 'loan_officer__username')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')

    def loan_progress(self, obj):
        if obj.status == 'DISBURSED':
            total_paid = obj.loanrepayment_set.filter(is_paid=True).aggregate(Sum('amount'))['amount__sum'] or 0
            progress = (total_paid / obj.amount) * 100
            return format_html(
                '<div style="width:100px;background-color:#f8f9fa;border:1px solid #ddd">'
                '<div style="width:{}px;height:20px;background-color:#007bff"></div>'
                '</div> {:.1f}%', min(100, progress), progress
            )
        return '-'
    loan_progress.short_description = 'Repayment Progress'

@admin.register(LoanRepayment)
class LoanRepaymentAdmin(admin.ModelAdmin):
    """
    LoanRepaymentAdmin class for the LoanRepayment model.
    """
    list_display = ('loan', 'amount', 'due_date', 'paid_date', 'is_paid', 'payment_status')
    list_filter = ('is_paid', 'due_date')
    search_fields = ('loan__applicant_name',)
    date_hierarchy = 'due_date'
    actions = ['mark_as_paid']

    def payment_status(self, obj):
        if obj.is_paid:
            return format_html('<span style="color: green;">✓ Paid</span>')
        if obj.due_date < timezone.now().date():
            return format_html('<span style="color: red;">Overdue</span>')
        return format_html('<span style="color: orange;">Pending</span>')
    payment_status.short_description = 'Status'

    def mark_as_paid(self, request, queryset):
        queryset.update(is_paid=True, paid_date=timezone.now())
    mark_as_paid.short_description = "Mark selected repayments as paid"

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """
    AuditLogAdmin class for the AuditLog model.
    """
    list_display = ('user', 'company', 'action', 'timestamp', 'get_details')
    list_filter = ('company', 'action', 'timestamp')
    search_fields = ('user__username', 'action', 'details')
    date_hierarchy = 'timestamp'
    readonly_fields = ('user', 'company', 'action', 'timestamp', 'details')

    def get_details(self, obj):
        return format_html('<pre>{}</pre>', json.dumps(obj.details, indent=2))
    get_details.short_description = 'Details'

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    """
    InvoiceAdmin class for the Invoice model.
    """
    list_display = ('company', 'amount', 'issue_date', 'due_date', 'is_paid', 'payment_status')
    list_filter = ('is_paid', 'issue_date', 'due_date')
    search_fields = ('company__name',)
    date_hierarchy = 'issue_date'
    actions = ['mark_as_paid']

    def payment_status(self, obj):
        if obj.is_paid:
            return format_html('<span style="color: green;">✓ Paid</span>')
        if obj.due_date < timezone.now().date():
            return format_html('<span style="color: red;">Overdue</span>')
        return format_html('<span style="color: orange;">Pending</span>')
    payment_status.short_description = 'Status'

    def mark_as_paid(self, request, queryset):
        queryset.update(is_paid=True, paid_date=timezone.now())
    mark_as_paid.short_description = "Mark selected invoices as paid"
