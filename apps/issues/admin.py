from apps.issues.models import *
from django.contrib import admin


class IssueAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'trackerURL')
    search_fields = ['title', 'description']


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'creationDate')
    search_fields = ['id', 'name', 'description']


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'creationDate', 'status', 'total', 'currency', 'offer_currency', 'usd2payment_rate')

admin.site.register(UserInfo)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(IssueComment)
admin.site.register(Offer)
admin.site.register(OfferComment)
admin.site.register(Solution)
admin.site.register(Payment, PaymentAdmin)
# Djangology admins
admin.site.register(Media)
admin.site.register(TechSolution)
admin.site.register(TechSolutionComment)
