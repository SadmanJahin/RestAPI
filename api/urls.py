from django.contrib import admin
from django.urls import path
from django.urls import include
from . import views
urlpatterns = [
    path('', views.apiOverview,name="api-overview"),
    path('task-list/', views.taskList,name="task-list"),
    path('task-create/', views.taskCreate,name="task-list"),
    path('upload/', views.upload,name="upload"),
     path('analyseHeartbeat/', views.analyseHeartbeat,name="analyseHeartbeat"),

    
]
