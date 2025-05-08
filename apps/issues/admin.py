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


class IssueCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'creationDate', 'language', 'author_id', 'issue_id')


class TechSolutionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'creationDate', 'createdByUser_id', 'issue_id')

admin.site.register(UserInfo)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(IssueComment, IssueCommentAdmin)
admin.site.register(Offer)
admin.site.register(OfferComment)
# admin.site.register(Solution)
admin.site.register(Payment, PaymentAdmin)
# Djangology admins
admin.site.register(Media)
admin.site.register(TechSolution, TechSolutionAdmin)
admin.site.register(TechSolutionComment)
