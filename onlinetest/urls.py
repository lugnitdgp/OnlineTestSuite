from django.urls import include, path
from onlinetest import views


# AppName
app_name = 'onlinetest'

urlpatterns = [
    path('', views.index, name="index"),
    path('rules/', views.Rules, name="rules"),
    path('questions/', views.Questions, name="questions"),
    path('createprofile/', views.CreateProfile, name="create_profile"),
]
