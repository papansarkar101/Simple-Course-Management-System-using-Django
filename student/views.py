from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages

from .forms import CustomUserCreationForm, CourseForm

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login

from django.contrib.auth.decorators import login_required


from .models import Course, Enrollment, CustomUser

from django.shortcuts import render
from .models import Course, Enrollment
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def enrolled_courses(request):
    student = CustomUser.objects.get(username=request.user)
    enrolled_courses = student.enrollment_set.all()

    return render(request, 'courses/enrolled_courses.html', {'enrolled_courses': enrolled_courses})


@login_required(login_url='login')
def enroll_course(request, course_id):
    course = Course.objects.get(id=course_id)
    enrolled = Enrollment.objects.filter(course=course, student=request.user).exists()

    if enrolled:
        messages.success(request, 'You have enrolled in this course already')
        return redirect('home')  # Redirect the user to the home page if already enrolled

    if request.method == 'POST':
        enrollment = Enrollment(course=course, student=request.user)
        enrollment.save()
        messages.success(request, 'You have successfully enrolled.')
        return redirect('home')  # Replace 'home' with the name of your home URL pattern

    return render(request, 'courses/enroll_course.html', {'course': course})


@login_required(login_url='login')
def courses_view(request):
    all_courses = Course.objects.all()
    if request.user.user_type == 'student':
        student = CustomUser.objects.get(username=request.user)
        enrolled_courses = student.enrollment_set.all()
        all_courses = Course.objects.exclude(id__in=enrolled_courses.values_list('course_id', flat=True))
        
    my_courses = Course.objects.filter(teacher=request.user)
    context = {
        'all_courses': all_courses, 
        'my_courses': my_courses
    }
    return render(request, 'courses/courses.html', context)


@login_required(login_url='login')
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user  # Assign the teacher to the logged-in user
            course.save()
            return redirect('home')  # Replace 'home' with the name of your home URL pattern
    else:
        form = CourseForm()
    
    return render(request, 'courses/create_course.html', {'form': form})


def home(request):
	return render(request, 'home.html')

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have successfully logged in.')
                return redirect('home')  # Replace 'home' with the name of your home URL pattern
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})