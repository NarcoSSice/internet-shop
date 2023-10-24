import uuid

from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from django.utils.translation import gettext_lazy as _
from main import settings
from shop.models import Customer


def confirm_email_customer(request, form):
    """
    This function take required data and get or create user in database.
    Then send message for confirmation.
    """

    data = {
        'email': form.cleaned_data['email'],
        'first_name': form.cleaned_data['first_name'],
        'last_name': form.cleaned_data['last_name'],
        'password': form.cleaned_data['password2'],
        'phone': form.cleaned_data['phone'],
    }
    try:
        customer = Customer.objects.get(email=data['email'])
    except Customer.DoesNotExist:
        customer = Customer.objects.create_user(**data)

    if customer.is_active:
        pass
    else:
        send_email_confirmation(request, customer)


def send_email_confirmation(request, customer):
    """
    This function create token for user and caches it.
    Then create message with confirmation link and send it on email.
    """

    token = uuid.uuid4().hex
    redis_key = settings.AUTH_USER_CONFIRMATION_KEY.format(token=token)
    cache.set(redis_key, {'customer_id': customer.id}, timeout=settings.AUTH_USER_CONFIRMATION_TIMEOUT)

    confirm_link = request.build_absolute_uri(
        reverse_lazy(
            'register_confirm', kwargs={'token': token}
        )
    )

    message = _(f'follow this link to confirm.\n{confirm_link}\nThis link will expire in 5 minutes')

    send_mail(
        subject=_('Confirm your email.'),
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[customer.email, ]
    )


def confirm_customer(token):
    """
    This function working when user follow the confirmation link,
    it takes user id from cache and change parameter is_active on True.
    """

    redis_key = settings.AUTH_USER_CONFIRMATION_KEY.format(token=token)
    customer_info = cache.get(redis_key) or {}
    customer_id = customer_info.get('customer_id')

    if customer_id:
        customer = get_object_or_404(Customer, id=customer_id)
        customer.is_active = True
        customer.save(update_fields=['is_active'])
        return True
    return False


def get_customer_activated(request, email):
    """
    It's function uses in login form for validate input data
    """

    try:
        customer = Customer.objects.get(email=email)
    except Customer.DoesNotExist:
        raise ValidationError(
            _('User with this email does not exist')
        )
    else:
        if not customer.is_active:
            send_email_confirmation(request, customer)
            raise ValidationError(
                _(
                    'This account is not activated '
                    'Confirmation link send on your email'
                )
            )
