from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from apps.issues.models import *
from django.contrib.auth.models import User
from apps.issues.services import language_services
from django.conf import settings


class Command(BaseCommand):

    help = "fill the language list table in the database"

    # def add_arguments(self, parser):
    #     # Define command-line arguments here
    #     parser.add_argument('name', type=str, help='Name to greet')
    #     parser.add_argument('--age', type=int, help='Optional age parameter')

    def handle(self, *args, **kwargs):
        self.stdout.write('start to fetch language list from server...')

        language_list = language_services.get_language_list_from_server()
        if len(language_list) == 0:
            raise CommandError('failed to fetch language list from server...')

        language_data = []
        for item in language_list:
            obj = Languages.newLanguage(item['label'], item['code'])
            language_data.append(obj)

        self.stdout.write('got '+str(len(language_data))+' languages from server...')

        Languages.objects.all().delete()
        Languages.objects.bulk_create(language_data)

        self.stdout.write('Successfully created languages data in database...')
