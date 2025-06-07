from django.urls import path
from .views import signupview, loginview, visual_view,lesson_view,student_dashboard,instructor_dashboard,course_detail

urlpatterns = [
    path('', home_page, name='vflox-home-page'),
    path('signup/', signupview, name='vflox-signup-page'),
    path('login/', loginview, name='login'),
    path('visual_view/', visual_view, name='visual_view'),
    path('lesson_view/', lesson_view, name='lesson_view'),
    path('student_dashboard/', student_dashboard, name='student_dashboard'),
    path('instructor_dashboard/', instructor_dashboard, name='instructor_dashboard'),
    path('course_detail/', course_detail, name='course_detail')
]