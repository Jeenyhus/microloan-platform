from django_filters import rest_framework as filters
from .models import LoanApplication, LoanRepayment, Invoice

class LoanApplicationFilter(filters.FilterSet):
    min_amount = filters.NumberFilter(field_name="amount", lookup_expr='gte')
    max_amount = filters.NumberFilter(field_name="amount", lookup_expr='lte')
    created_after = filters.DateFilter(field_name="created_at", lookup_expr='gte')
    created_before = filters.DateFilter(field_name="created_at", lookup_expr='lte')

    class Meta:
        model = LoanApplication
        fields = ['status', 'loan_officer', 'company']

class LoanRepaymentFilter(filters.FilterSet):
    due_date_from = filters.DateFilter(field_name="due_date", lookup_expr='gte')
    due_date_to = filters.DateFilter(field_name="due_date", lookup_expr='lte')

    class Meta:
        model = LoanRepayment
        fields = ['is_paid', 'loan']

class InvoiceFilter(filters.FilterSet):
    min_amount = filters.NumberFilter(field_name="amount", lookup_expr='gte')
    max_amount = filters.NumberFilter(field_name="amount", lookup_expr='lte')
    
    class Meta:
        model = Invoice
        fields = ['is_paid', 'company'] 