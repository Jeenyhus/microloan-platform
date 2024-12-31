from rest_framework import permissions

class IsCompanyAdmin(permissions.BasePermission):
    """
    IsCompanyAdmin class for the CompanyAdmin model.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_company_admin

class IsCompanyMember(permissions.BasePermission):
    """
    IsCompanyMember class for the CompanyMember model.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.company is not None

class IsLoanOfficer(permissions.BasePermission):
    """
    IsLoanOfficer class for the LoanOfficer model.
    """
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user == obj.loan_officer
