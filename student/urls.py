from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView

from .views import RegisterView, home, login_view, create_course, courses_view, enroll_course, enrolled_courses


urlpatterns = [
	path('', home, name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),

    path('create-course/', create_course, name='create_course'),
    path('courses/', courses_view, name='courses'),
    path('enroll-course/<int:course_id>/', enroll_course, name='enroll_course'),
    path('enrolled-courses/', enrolled_courses, name='enrolled_courses'),
]


