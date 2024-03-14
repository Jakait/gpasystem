from django.shortcuts import render,redirect
from .forms import UserRegistrationForm
from .models import *
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request,'login.html')

# register user
def registerUser(request):

    form = UserRegistrationForm()
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
       
       
      
        if form.is_valid():
            access_level = form.cleaned_data['accesslevel']
          
            if access_level in [2, 3]:
                course_id = request.POST.get('usercourse')  
                # If the access level is one or two, check if the course name is provided
                if access_level in [2, 3] and not course_id:
                    messages.error(request, "Please select a course.")
                else:
                    user = form.save()
                   
                    course = Course.objects.get(id=course_id) 
                    
                    if access_level == 3:
                        admno = getAdmno("ST")
                        student = Student.objects.create(course_id = course, adm_no = admno,user_id =user)
                    
                    else:
                        admno = getAdmno("LEC")
                        lectureer = Lecturer.objects.create(course_id = course, Lec_no = admno,user_id =user)

                        
              
                    messages.success(request, "User saved successfully.")
                    return redirect('viewuser')
            else:
                form.save()
                messages.success(request, "User saved successfully.")
                return redirect('viewuser')

        else:
            # Print form errors to console
            print(form.errors)
            
            
    return render(request,'userreg.html',{"form": form})


# view users
def  viewUser(request):
    users = User.objects.all().order_by('-id')
    user_data = []
    for user in users:
        user_type = None
        course_name = None

        if user.accesslevel == 1:
            user_type = 'Admin'
        elif user.accesslevel == 2:
            lecturer = Lecturer.objects.filter(user_id=user.id).first()
            if lecturer:
                user_type = 'Lecturer'
                course_name = lecturer.course_id.course_name if lecturer.course_id else None
        elif user.accesslevel == 3:
            student = Student.objects.filter(user_id=user.id).first()
            if student:
                user_type = 'Student'
                course_name = student.course_id.course_name if student.course_id else None

        user_data.append({
            'email': user.email,
            'firstname': user.firstname,
            'lastname': user.last_name,
            'middlename': user.middle_name,
            'user_type': user_type,
            'course_name': course_name
        })
    return render(request,'userview.html',{'users':user_data})


# add course
def registerCourse(request):
    if request.method == "POST":
        unitcourse = request.POST.get("unitcourse")
        if not unitcourse:
            messages.error(request, "Please select unit or course")
        else:
            if unitcourse == "101":
                coursename = request.POST.get("coursename")
                course_code = request.POST.get("course_code")
                if not course_code or not coursename:
                    messages.error(request, "Please fill all the fields")
                else:
                    # Check if either course name or course code already exists
                    if Course.objects.filter(course_name=coursename).exists() or Course.objects.filter(course_code=course_code).exists():
                        messages.error(request, "Course with the same name or code already exists.")
                    else:
                        # Create the course if it doesn't already exist
                        course = Course.objects.create(course_name=coursename, course_code=course_code)
                        messages.success(request, "Course saved successfully")
                  


            else:
                course_id = request.POST.get("course_id")
                unit = request.POST.get("unit")
                if not course_id or not unit:
                    messages.error(request, "Please fill all the fields")
                else:

                    course = Course.objects.get(id=course_id) 
                    
                    if Unit.objects.filter(unit_name =unit).exists():
                        messages.error(request, "Unit with the same unit name exists.")
                        
                    else:
                        Unit.objects.create(course_id =course, unit_name =unit)
                        messages.success(request, "Unit saved succesfully")






    return render(request, 'courseadd.html')

# dashboard
def dashboard(request):
    pass

# add results
def registerResults(request):
    return render(request, 'resultadd.html')

# fist get view course endpoint 
def viewCourse(request):
    return render(request, 'viewcourse.html')
# view course after fetch
def fetchCourseView(request):
    id = request.GET.get('course')
    
    courses = Course.objects.all()
    units = Unit.objects.all()
    if id == '101': 
        return render(request, 'components/courseview.html',{'courses':courses})
    elif id == '102':
        return render(request, 'components/unitview.html',{'units':units})
    else:
        return render(request, 'components/empty.html')

# fetch course or unit
# add course
def fetchCourse(request):
    id = request.GET.get('course')
    
    courses = Course.objects.all()
    if id == '101': 
        return render(request, 'components/course.html')
    elif id == '102':
        return render(request, 'components/unit.html',{'courses':courses})
    else:
        return render(request, 'components/empty.html')
    

# get user courses
def userCourse(request):
    access = request.GET.get('access')

    courses = Course.objects.all()
    if access == '2' or access == '3':
        return render(request, 'components/usercourse.html',{'courses':courses})
    else:
        return render(request, 'components/empty.html')
    

# get admission number
def getAdmno(admn):
    if (admn == "ST"):
            
        latest_user = Student.objects.order_by('-id').first()  # Get the latest student
        if latest_user is not None:
            latest_adm_no = latest_user.adm_no

    else:
        latest_user = Lecturer.objects.order_by('-id').first()  # Get the latest lecturer
        if latest_user is not None:
            latest_adm_no = latest_user.Lec_no
    if latest_user:
        # Get the latest adm_no
        if latest_adm_no.startswith(admn):
            number_part = latest_adm_no[len(admn):]  # Get the numeric part
            print(number_part)
            try:
                number = int(number_part)  # Convert numeric part to integer
            except ValueError:
                number = 0  # If conversion fails, set number to 0
            new_number = number + 1  # Increment number by 1
            
            
            user_adm_no = admn + str(new_number ) # Format number with leading zeros
        else:
            
            user_adm_no = admn +"1" 
    else:
        user_adm_no = admn +"1"   # If there are no existing user, set adm_no to adm1
    return user_adm_no
        



  