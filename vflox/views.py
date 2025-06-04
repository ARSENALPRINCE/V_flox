from django.shortcuts import render
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, Lesson, Enrollment, Category
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
# create your views here.

def signupview(request:HttpRequest):
    # user1 = User.objects.create_user(username="divine1",email="swissb506@gmail.com",password="di1vi2ne3")
    # user1.save()
    if request.method == "POST":
        username= request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password1 = request.POST.get("password1")
        if password != password1 or len(password) < 8:
            return render(request,"auth/signup.html",{"error":"password do not match or minimum length of password not met"})
        if not username or not email :
           return render(request,"auth/signup.html",{"error":"username and email is required"}) 
        try:
            user_exist = User.objects.filter(username = username).first()
            if user_exist :
                return render(request,"auth/signup.html",{'error':"user already exist","success":None})
            # getting to this stage means we are good to signup the user
            user = User.objects.create_user(username=username,email=email,password=password)
            user.save()
            vflox = vflox.objects.create(trader=user)
            vflox.save()
            return render(request,"auth/signup.html",{'error':None,"success":"signup successful"})
        except Exception as e :
            print(e)
    return render(request,"auth/signup.html",{'error':"Server Error","success":None})


def loginview(request:HttpRequest):
    # user1 = User.objects.create_user(username="divine1",email="swissb506@gmail.com",password="di1vi2ne3")
    # user1.save()
    if request.method == "POST":
        username= request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request,username=username,password=password)
        print(user)
        if user is not None:
            login(request,user)
            return redirect('/tradex/wallet/')
        else :
            return render(request,"auth/login.html",{'error':"Server Error","success":None})
        
    return render(request,"auth/login.html",{})


def visual_view(request):
    # Filtering logic can be added here
    courses = Course.objects.all()
    categories = Category.objects.all()
    levels = Course._meta.get_field('level').choices
    return render(request, 'user/visual_view.html', {
        'courses': courses,
        'categories': categories,
        'levels': levels,
    })#It prepares the data needed to show all courses 
      #and filtering options on the course listing page

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = course.lessons.order_by('order')
    instructor = course.instructor
    # reviews = ... # Add review logic if you have a Review model
    return render(request, 'user/course_detail.html', {
        'course': course,
        'lessons': lessons,
        'instructor': instructor,
        # 'reviews': reviews,
    })

@login_required
def lesson_view(request, course_id, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id, course_id=course_id)
    course = lesson.course
    lessons = course.lessons.order_by('order')
    # progress = ... # Calculate user progress if needed
    return render(request, 'user/lesson_view.html', {
        'lesson': lesson,
        'course': course,
        'lessons': lessons,
        # 'progress': progress,
    })

@login_required
def student_dashboard(request):
    enrollments = Enrollment.objects.filter(user=request.user)
    # certificates = ... # Add certificate logic if you have a Certificate model
    # quiz_scores = ... # Add quiz logic if you have quizzes
    return render(request, 'user/student_dashboard.html', {
        'enrollments': enrollments,
        # 'certificates': certificates,
        # 'quiz_scores': quiz_scores,
    })

@login_required
def instructor_dashboard(request):
    courses = Course.objects.filter(instructor=request.user)
    # stats, reports, ratings, etc. can be added here
    return render(request, 'user/instructor_dashboard.html', {
        'courses': courses,
        # 'stats': stats,
        # 'reports': reports,
    })
