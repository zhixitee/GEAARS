from django.urls import path
from events import views

app_name = 'events'

urlpatterns = [
    path('', views.events, name='events'),
    path('about/', views.about, name='about'),
    path('map/', views.map, name='map'),
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
    path('add_category/', views.add_category, name='add_category'),
    path('category/<slug:category_name_slug>/add_page/', views.add_page, name='add_page'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),path('restricted/', views.restricted, name='restricted'),
    path('logout/', views.user_logout, name='logout'),
    path('add_event/', views.add_event, name='add_event'),
    path('my_events/', views.user_events_list, name='user_events_list'),
    path('david_guetta_event', views.choosenEvent, name='david_guetta_event'),
    path('kevin_heart_event', views.choosenEvent, name='kevin_heart_event'),
    path('maya_deliah_event', views.choosenEvent, name='maya_deliah_event'),
    path('peach_pit_event', views.choosenEvent, name= 'peach_pit_event'),
]
