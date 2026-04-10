"""
Factories factory-boy pour les tests.
"""
import factory
from django.contrib.auth import get_user_model
from django.utils import timezone

from contacts.models import ContactRequest
from portfolio.models import PortfolioProject, Testimonial
from quotes.models import Quote

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True

    email = factory.Sequence(lambda n: f'user{n}@example.com')
    username = factory.Sequence(lambda n: f'user{n}')
    first_name = 'Jean'
    last_name = 'Dupont'
    is_active = True

    @factory.post_generation
    def password(obj, create, extracted, **kwargs):
        pwd = extracted or 'TestPassword123!'
        obj.set_password(pwd)
        if create:
            obj.save()


class PortfolioProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PortfolioProject

    title = factory.Sequence(lambda n: f'Projet {n}')
    tagline = 'Un projet exemplaire'
    description = 'Description détaillée du projet.'
    tech_stack = ['Vue.js', 'Django']
    is_published = True
    is_featured = False
    order = factory.Sequence(lambda n: n)


class TestimonialFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Testimonial

    client_name = 'Marie Martin'
    client_company = 'PME Example'
    content = 'Excellent travail, je recommande vivement.'
    rating = 5
    is_active = True
    is_featured = False


class ContactRequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ContactRequest

    name = 'Jean Dupont'
    email = factory.Sequence(lambda n: f'contact{n}@example.com')
    subject = 'project'
    message = 'Bonjour, je souhaite en savoir plus sur vos services.'


class QuoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Quote

    client_name = factory.Sequence(lambda n: f'Client {n}')
    client_email = factory.Sequence(lambda n: f'client{n}@example.com')
    client_phone = '0612345678'
    status = Quote.STATUS_DRAFT
    base_price = factory.LazyAttribute(lambda _: 1500)
    subtotal_ht = factory.LazyAttribute(lambda o: o.base_price)
    vat_rate = 20
    vat_amount = factory.LazyAttribute(lambda o: o.subtotal_ht * 20 / 100)
    total_ttc = factory.LazyAttribute(lambda o: o.subtotal_ht + o.vat_amount)
    valid_until = factory.LazyFunction(
        lambda: (timezone.now() + timezone.timedelta(days=30)).date()
    )
