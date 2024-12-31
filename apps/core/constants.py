# Subscription Plans
SUBSCRIPTION_PLANS = {
    'BASIC': {
        'max_users': 5,
        'price': 50,
        'features': ['loan_management', 'basic_reporting']
    },
    'PRO': {
        'max_users': 20,
        'price': 200,
        'features': ['loan_management', 'advanced_reporting', 'api_access']
    },
    'ENTERPRISE': {
        'max_users': None,  # Unlimited
        'price': None,  # Custom pricing
        'features': ['loan_management', 'advanced_reporting', 'api_access', 'custom_integration']
    }
}

# Loan Constants
MINIMUM_LOAN_AMOUNT = 100
MAXIMUM_LOAN_AMOUNT = 1000000
MAXIMUM_LOAN_TERM = 60  # months

# System Settings
MAX_LOGIN_ATTEMPTS = 5
PASSWORD_RESET_TIMEOUT = 24  # hours
TOKEN_EXPIRY = 30  # minutes 