from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.FileView.as_view(), name='file-upload'),
    path('open/', views.open, name='open'),
    path('close/', views.close, name='close'),
    path('state/', views.state, name='state'),
]