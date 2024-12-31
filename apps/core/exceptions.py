from rest_framework.exceptions import APIException
from rest_framework import status

class InsufficientPermission(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'You do not have permission to perform this action.'

class SubscriptionExpired(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'Your company subscription has expired.'

class LoanLimitExceeded(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Loan amount exceeds company limit.' 