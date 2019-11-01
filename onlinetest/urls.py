from django.urls import include, path
from onlinetest import views


# AppName
app_name = 'onlinetest'

urlpatterns = [
    path('', views.index, name="index"),
    path('rules/', views.rules, name="rules"),
    path('questions/', views.questions, name="questions"),
]
