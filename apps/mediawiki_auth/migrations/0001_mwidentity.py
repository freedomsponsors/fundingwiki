from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [migrations.CreateModel(
        name="MWIdentity",
        fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("mw_id", models.BigIntegerField(unique=True)),
            ("is_temp", models.BooleanField(default=False)),
            ("is_blocked", models.BooleanField(default=False)),
            ("active_before_block", models.BooleanField(blank=True, null=True)),
            ("created_at", models.DateTimeField(auto_now_add=True)),
            ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE,
                 related_name="mw_identity", to=settings.AUTH_USER_MODEL)),
        ],
    )]
