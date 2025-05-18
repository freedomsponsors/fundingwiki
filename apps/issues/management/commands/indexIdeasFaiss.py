from django.core.management.base import BaseCommand, CommandError

from apps.issues.models import Ideas
from apps.issues.services import faiss_services, idea_services


class Command(BaseCommand):

    help = "index the ideas in the database"

    def handle(self, *args, **kwargs):
        self.stdout.write('start to index the ideas...')

        idea = Ideas.objects.get(id=10)
        idea_services.get_suggest_by_idea(idea)
        return

        ideal = Ideas.objects.filter(faiss_id=-1).first()
        if ideal:
            ideal.faiss_id = faiss_services.add_to_faiss(ideal.content)
            ideal.save()

            self.stdout.write('Successfully indexed the ideas, idea id:'+str(ideal.id)+', faiss_id:'+str(ideal.faiss_id))
        else:
            self.stdout.write('no ideas to index...')

        # faiss_services.add_to_faiss('Design an app where users can log and track the care of their plants. Include reminders for watering, sunlight needs, and potential problems.')
        # faiss_services.add_to_faiss('Design an app on ios platform')
        # faiss_services.add_to_faiss('apple')
        # faiss_services.add_to_faiss('banana')
        # faiss_services.add_to_faiss('orange')
        # faiss_services.add_to_faiss('phone')



