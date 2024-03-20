from django.urls import path
from events import views
from django.contrib.auth import views as auth_views

app_name = 'events'

urlpatterns = [
    path('', views.events, name='events'),
    path('about/', views.about, name='about'),
    path('map/', views.map, name='map'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('add_event/', views.add_event, name='add_event'),
    path('my_events/', views.user_events_list, name='user_events_list'),
    path('event/<slug:event_slug>/choosen_event', views.choosenEvent, name='choosen_event'),
    path('event/<slug:event_slug>/review_and_discuss/', views.make_a_review_discuss_event, name='make_a_review_discuss_event'),
]
