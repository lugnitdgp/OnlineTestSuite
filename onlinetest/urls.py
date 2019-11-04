from django.urls import include, path
from onlinetest import views


# AppName
app_name = 'onlinetest'

urlpatterns = [
    path('', views.index, name="index"),
    path('update_time/', views.UpdateTime, name="update_time"),
    path('rules/', views.rules, name="rules"),
    path('questions/', views.questions, name="questions"),
    path('answers/<int:qid>', views.answers, name="answers"),
    path('finish/', views.finish, name="finish"),
    path('logout/', views.logout_user, name="logout"),
    path('results/', views.results, name="results")
]
