from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from main import views


app_name = 'main'


urlpatterns = [
    path('', views.index, name='index'),
    path('users/me/', views.user_profile_me, name='user_profile_me'),
    path('users/<int:user_id>/', views.user_profile, name='user_profile'),
    path(
        'users/<int:user_id>/volunteer_vacancy/<int:pk>',
        views.volunteer_vacancy_view,
        name='volunteer_vacancy'
    ),
    path(
        'users/<int:user_id>/nonprofit_event/<int:pk>',
        views.nonprofit_event_view,
        name='nonprofit_event'
    ),
    path(
        'funds/',
        views.list_funds,
        name='list_funds'
    ),
    path(
        'funds/<int:fund_id>/',
        views.fund_profile,
        name='fund_profile'
    ),
    path(
        'funds/<int:fund_id>/campaign/<int:pk>/',
        views.fundraising_campaign_view,
        name='fundraising_campaign',
    ),
    path(
        'fundraising_campaigns/',
        views.fundraising_campaign_list_view,
        name='fundraising_campaign_list'
    ),
    path(
        'nonprofit_events/',
        views.nonprofit_event_list_view,
        name='nonprofit_event_list'
    ),
    path(
        'volunteer_vacancies/',
        views.volunteer_vacancy_list_view,
        name='volunteer_vacancy_list'
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
