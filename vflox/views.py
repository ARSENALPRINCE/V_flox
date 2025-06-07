from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse,HttpRequest
from  django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from A_Learning.vflox.models import Category, Course, Enrollment, Lesson

# Create your views here.
def homepage(request):
    return HttpResponse("<h2 align='center style='color:grey;>'HELLO E_LEARNERS  </h2>")
def aboutpage(request):
    return HttpResponse("<h2 align='center' style='color:green;>' ABOUT<h2/>")
def contactpage(request):
    return HttpResponse("<h2 align='center' style='color:green;>' CONTACT VFLOX </h2>")

def signupview(request:HttpRequest):
    
    if request.method == "POST":
        email=request.POST.get("email")
        username=request.POST.get("username")
        password1=request.POST.get("password")
        password2=request.POST.get("password1")
        if password1 != password2 or len (password1)<8:
            return render(request,"auth/signup.html",{"error":"password do not match or len of password is < 8"})
        if not username :
            return render(request,"auth/signup.html",{"error":"username required"})
        user_found = User.objects.filter(username = username)
        if user_found :
            return render(request,"auth/signup.html",{"error":"User with the given username already exist"})
        # user = User(username=username , email=email, password = password1)
        # user.save()
        User.objects.create_user(username=username,email=email, password=password1)
        print('User Saved')
        return redirect("vflox-login-page")
    
    print("Get request for signup called upon")   
    return render(request,"auth/signup.html",{"error":None})
        
def loginview(request: HttpRequest):
    if  request.method=="POST":
        username=request.POST.get("username")
        pass1=request.POST.get("pass1")
        try:
            user = authenticate(request,username=username,password=pass1)
            if user == None:
                return render(request,"auth/login.html",{'error':"not a valid user"})
            login(request, user)
            return redirect("/vflox/homepage")
        except:
            return render(request,"auth/login.html",{'error':"server Error","success":None})
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
