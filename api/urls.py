from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.get_hi, name='test'),
    path('analysis/', views.post_analysis, name='analysis'),
    path('data/', views.get_analysis, name='data'),
    path('summary/', views.get_summary, name='summary')
]
