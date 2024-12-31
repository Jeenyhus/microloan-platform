import factory
from django.utils import timezone
from core.models import User, Company, Subscription, LoanApplication

class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company

    name = factory.Sequence(lambda n: f'Company {n}')
    registration_number = factory.Sequence(lambda n: f'REG{n:05d}')
    address = factory.Faker('address')
    is_active = True

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    company = factory.SubFactory(CompanyFactory)
    is_company_admin = False

class LoanApplicationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = LoanApplication

    company = factory.SubFactory(CompanyFactory)
    loan_officer = factory.SubFactory(UserFactory)
    applicant_name = factory.Faker('name')
    amount = factory.Faker('pydecimal', left_digits=5, right_digits=2, positive=True)
    interest_rate = factory.Faker('pydecimal', left_digits=2, right_digits=2, positive=True)
    term_months = factory.Faker('random_int', min=6, max=60)
    status = 'PENDING' 