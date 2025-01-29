from audioop import reverse
from decimal import Decimal

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext as _
from core.utils import paypal_adapter
from core.models import  Payment
from core.services import paypal_services, mail_services
import logging
import traceback
from paypal.standard.forms import PayPalPaymentsForm


logger = logging.getLogger(__name__)

__author__ = 'tony'

def process_payment(request):
    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % 0.01,
        'item_name': 'Order {}'.format(3),
        'invoice': str(3),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                        'paypal-ipn'),
        'return_url': 'http://{}{}'.format(host,
                                       'payment_done'),
        'cancel_return': 'http://{}{}'.format(host,
                                        'payment_cancelled'),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'sandbox/process_payment.html', {'order': {}, 'form': form})
