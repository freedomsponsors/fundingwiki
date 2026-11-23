from django.conf import settings
from django.db import models


class MWIdentity(models.Model):
    """MediaWiki identity linked to the existing Django auth user."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name="mw_identity")
    mw_id = models.BigIntegerField(unique=True)
    is_temp = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    active_before_block = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_temp_account(self):
        return self.is_temp

    @property
    def mw_temp_name(self):
        return self.user.username

    def can_create_issue(self): return True
    def can_vote(self): return True
    def can_comment(self): return True
    def can_sponsor(self): return not self.is_temp
    def can_receive_payment(self): return not self.is_temp

    def __str__(self):
        return f"MediaWiki user {self.mw_id} → {self.user.username}"


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
