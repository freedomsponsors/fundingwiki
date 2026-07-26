from django.db import models


class MWUser(models.Model):
    mw_session_cookie = models.CharField(max_length=255, unique=True)
    mw_temp_name = models.CharField(max_length=255)  # "~2026-4521983" o "Pepito"
    is_temp_account = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mw_users'

    def __str__(self):
        return self.mw_temp_name

    def can_create_issue(self):   return True
    def can_vote(self):           return True
    def can_comment(self):        return True
    def can_sponsor(self):        return not self.is_temp_account  # requiere cuenta registrada
    def can_receive_payment(self):return not self.is_temp_account  # requiere cuenta registrada
