from django.urls import path
from .views import signupview, loginview, visual_view

urlpatterns = [
    path('signup/', signupview, name='vflox-signup-page'),
    path('login/', loginview, name='login'),
    path('visual_view/', visual_view, name='visual_view'),
]