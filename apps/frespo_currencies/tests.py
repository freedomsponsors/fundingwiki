import unittest

from django.test import TestCase
from apps.frespo_currencies import currency_service

__author__ = 'tony'


@unittest.skip("Legacy live-network test; currency_service is effectively unused")
class CurrencyServiceTests(TestCase):
    def test_currency_service(self):
        r = currency_service.get_rate('USD', 'BRL')
        r = currency_service.get_rate('USD', 'BTC')
        r = currency_service.get_rate('BTC', 'USD')
        r = currency_service.get_rate('BTC', 'BRL')
        pass
