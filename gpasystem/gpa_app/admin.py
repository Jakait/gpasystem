from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Lecturer)
admin.site.register(Semister)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Unit)
admin.site.register(Exam)

