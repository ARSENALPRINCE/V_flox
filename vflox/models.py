from django.db import models
from django.contrib.auth.models import User


LEVEL_CHOICES=(
    ('beginner', 'Beginner'),
    ('intermediate','Intermediate'),
    ('professional', 'Professional')
)

LEVEL_CONTENT_TYPE =(
    ('text','TEXT'),
    ('video','VIDEO'),
    ('online','ONLINE')
)

class Category(models.Model):
    name = models.CharField(max_length=100)
    description =models.TextField(blank=True)
    slug =models.SlugField(unique=True)

class  Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    thumbnail = models.ImageField(upload_to='course_thumbnails/')
    level = models.CharField(max_length=15, choices=LEVEL_CHOICES, default='beginner')
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    is_free = models.BooleanField(default=True)

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content_type = models.CharField(max_length=15, choices=LEVEL_CONTENT_TYPE)
    content = models.TextField(blank=True)  # For text-based lessons
    video_url = models.URLField(blank=True)  # For video lessons
    order = models.IntegerField(default=0)
    is_preview = models.BooleanField(default=False)  # Free preview lesson

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)