from django.contrib import admin
from .models import (
    CustomUser,
    UserProfile,
    FundProfile,
    Donation,
    Comment,
    FundraisingCampaign,
    VolunteerVacancy,
    NonprofitEvent,
)


admin.site.register(CustomUser)
admin.site.register(UserProfile)
admin.site.register(Donation)
admin.site.register(Comment)
admin.site.register(FundProfile)
admin.site.register(FundraisingCampaign)
admin.site.register(VolunteerVacancy)
admin.site.register(NonprofitEvent)
