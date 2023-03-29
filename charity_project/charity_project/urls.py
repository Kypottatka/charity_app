from django.contrib import admin
from django.urls import path
from main import views
from main.views import FundraisingCampaignView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('user/<int:user_id>/', views.user_profile, name='user_profile'),
    path(
        'fund/',
        views.list_funds,
        name='list_funds'
    ),
    path(
        'fund/<int:fund_id>/',
        views.fund_profile,
        name='fund_profile'
    ),
    path(
        'fund/<int:fund_id>/campaign/',
        views.list_fundraising_campaigns,
        name='list_fundraising_campaigns',
    ),
    path(
        'fund/<int:fund_id>/campaign/<int:campaign_id>/',
        FundraisingCampaignView.as_view(),
        name='fundraising_campaign',
    ),
    path(
        'fund/<int:fund_id>/campaign/create/',
        views.create_fundraising_campaign,
        name='create_fundraising_campaign'
    ),
    path(
        'create_comment/<str:model_type>/<int:model_id>/',
        views.create_comment,
        name='create_comment'
    ),
]
