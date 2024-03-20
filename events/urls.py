from django.urls import path
from events import views

app_name = 'events'

urlpatterns = [
    path('', views.events, name='events'),
    path('about/', views.about, name='about'),
    path('map/', views.map, name='map'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('add_event/', views.add_event, name='add_event'),
    path('my_events/', views.user_events_list, name='user_events_list'),
    path('event/<slug:event_slug>/', views.choosenEvent, name='choosen_event'),
]
