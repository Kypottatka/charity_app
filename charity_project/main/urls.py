from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from main import views


app_name = 'main'


urlpatterns = [
    path('', views.index, name='index'),
    path('user/<int:user_id>/', views.user_profile, name='user_profile'),
    path(
        'user/<int:user_id>/volunteer_vacancy/<int:pk>',
        views.volunteer_vacancy_view,
        name='volunteer_vacancy'
    ),
    path(
        'user/<int:user_id>/nonprofit_event/<int:pk>',
        views.nonprofit_event_view,
        name='nonprofit_event'
    ),
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
        'fund/<int:fund_id>/campaign/<int:campaign_id>/',
        views.fundraising_campaign_view,
        name='fundraising_campaign',
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )