from django.shortcuts import render,redirect,get_object_or_404
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate,login,logout
from .models import *
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse
import random
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url='login')
def index(request):
    return render(request,'login.html')

# logout 
@login_required(login_url='login')
def signout(request):
    logout(request)
    return redirect('login')

# delete exam
@login_required(login_url='login')
def deleteExam(request, id):
    # Access the logged-in user
    logged_in_user = request.user
    if logged_in_user.accesslevel != 1:
        messages.error(request, 'Forbidden')
        return redirect(request.META.get('HTTP_REFERER'))
    
    exam = get_object_or_404(Exam, id=id)

    exam.delete()
    messages.success(request, 'Exam deleted successfully!')
    return redirect('viewresults')
#edit exam
@login_required(login_url='login')
def editExam(request, id):
    # Access the logged-in user
    logged_in_user = request.user
    if logged_in_user.accesslevel == 3:
        return redirect(request.META.get('HTTP_REFERER'))
    if request.method == "POST":
        exam = get_object_or_404(Exam, id=id)
        mid_sem = request.POST.get("midsem")
        quiz = request.POST.get("quiz")
        lab = request.POST.get("lab")
        end_sem = request.POST.get("endsem")
        unit_id = request.POST.get("unit")
        student_id = request.POST.get("student")
        score = request.POST.get("total_score")
        if not unit_id or not student_id or not score:
            messages.error(request, "Please fill all the fields")
        else:
            exam.unit_id_id = unit_id
            exam.lab = lab
            exam.quiz = quiz
            exam.midsem = mid_sem
            exam.endsem = end_sem
            exam.student_id = student_id
            exam.score = score
            exam.status = 2

            messages.success(request, "Exam saved successfully")
            exam.save()
            
                
    exam = get_object_or_404(Exam, id=id)
    return render(request, 'resultsedit.html', {'exam':exam})
# delete course
@login_required(login_url='login')
def deleteCourse(request, id):
 
    course = get_object_or_404(Course, id=id)

    course.delete()
    messages.success(request, 'course deleted successfully!')
    return redirect('viewcourse')

# delete course
@login_required(login_url='login')
def deleteUnit(request, id):
 
    unit = get_object_or_404(Unit, id=id)

    unit.delete()
    messages.success(request, 'unit deleted successfully!')
    return redirect('viewcourse')

# edit course
@login_required(login_url='login')
def editCourse(request, id):
    
    if request.method == 'POST':
        
        course = get_object_or_404(Course,id=id)
        course_code = request.POST.get("course_code")
        course_name = request.POST.get("coursename")
        course.course_code  = course_code
        course.course_name = course_name
        course.save()
    course = get_object_or_404(Course,id=id)
    return render(request, 'courseedit.html', {'course':course})

# edit unit
@login_required(login_url='login')
def editUnit(request, id):
    if request.method == 'POST':
        unit = get_object_or_404(Unit, id=id)
        course_id = request.POST.get("course_id")
        unit_name = request.POST.get("unit")
        if Unit.objects.filter(unit_name =unit_name).exists():
            messages.error(request, "Unit with the same unit name exists.")
        else:
            unit.unit_name = unit_name
            unit.course_id_id = course_id
            messages.success(request, 'Unit Updated successfully!')
            unit.save()

         
    unit = get_object_or_404(Unit, id=id)
    courses = Course.objects.all()
    return render(request, 'unitedit.html', {'unit': unit,'courses':courses})

# delete user
@login_required(login_url='login')
def deleteUser(request, id):
    logged_in_user = request.user
    if logged_in_user.accesslevel != 1:
        messages.error(request, 'Forbidden')
        return redirect(request.META.get('HTTP_REFERER'))
 
    user = get_object_or_404(User, id=id)
    if user.id == request.user:
        messages.error(request, 'You cannot delete Your account')
        return redirect('viewuser')

    user.delete()
    messages.success(request, 'User deleted successfully!')
    return redirect('viewuser')
   
# edit user
@login_required(login_url='login')
def editUser(request,id):
    
    
    if request.method == 'POST':
        user = get_object_or_404(User, id=id)
        
        # Extract information from POST request
        first_name = request.POST.get('firstname')
        middle_name = request.POST.get('middlename')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone')
        password = request.POST.get('password')
        
        # Assuming 'course' field is for a related model or a property you wish to update
        course = request.POST.get('course')  

        # Update user model instance
        user.firstname = first_name
        user.middle_name = middle_name
        user.last_name = last_name
        user.email = email
        user.phone_number = phone_number
        # Check if password change was requested
        if password:  # If password field is not empty
            user.set_password(password)
        
        if course:
            if user.accesslevel == 3:
                student = Student.objects.get(user_id=id)
                student.course_id_id = course
                student.save()
            else:
                lecturer = Lecturer.objects.get(user_id=id)
                lecturer.course_id_id = course
                lecturer.save()
         
        # Handle course update logic here, depending on your model structure
        
        user.save()  # Don't forget to save the changes

        messages.success(request, 'User updated successfully!')

    course_id = ''   
    user = get_object_or_404(User, id=id)
    if user.accesslevel == 3:
        course_id = Student.objects.get(user_id=user.id).course_id_id
    elif user.accesslevel == 2:
        course_id = Lecturer.objects.get(user_id=user.id).course_id_id


    courses = Course.objects.all()

    return render(request, 'edituser.html', {'user': user,'courses':courses,'course_id':course_id})





# register user
@login_required(login_url='login')
def registerUser(request):
    # Access the logged-in user
    logged_in_user = request.user
    if logged_in_user.accesslevel != 1:
        messages.error(request, 'Forbidden')
        return redirect(request.META.get('HTTP_REFERER'))

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
                        # admno = getAdmno("ST")
                        student = Student.objects.create(course_id = course, user_id =user)
                    
                    else:
                        # admno = getAdmno("LEC")
                        lectureer = Lecturer.objects.create(course_id = course,user_id =user)

                        
              
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
@login_required(login_url='login')
def  viewUser(request):
    # Access the logged-in user
    logged_in_user = request.user
    if logged_in_user.accesslevel != 1:
        users = User.objects.filter(id=logged_in_user.id)
    else:   
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
            'id':user.id,
            'email': user.email,
            'firstname': user.firstname,
            'lastname': user.last_name,
            'middlename': user.middle_name,
            'user_type': user_type,
            'course_name': course_name
        })
    return render(request,'userview.html',{'users':user_data,'logged_in_user':logged_in_user })

# fetch students units
@login_required(login_url='login')
def fetchstudentsunit(request):
    user_id = request.GET.get('studentid')
    student = Student.objects.get(user_id=user_id)
    courseid = student.course_id
    units = Unit.objects.filter(course_id=courseid)


    return render(request,'components/studentunits.html',{'studentunits':units})



# add course
@login_required(login_url='login')
def registerCourse(request):
    # Access the logged-in user
    logged_in_user = request.user
    if logged_in_user.accesslevel != 1:
        messages.error(request, 'Forbidden')
        return redirect(request.META.get('HTTP_REFERER'))
        
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
@login_required(login_url='login')
def dashboard(request):
    students_count  = Student.objects.all().count()
    lecturers_count = Lecturer.objects.all().count()
    units_count = Unit.objects.all().count()
    course_count = Course.objects.all().count()
    results_count = Exam.objects.values('student').distinct().count()
    context = {'students_count':students_count,'lecturers_count':lecturers_count, 'units_count':units_count,'results_count':results_count,'courses_count':course_count}
    return render(request,'home.html',context)
    

# add results
@login_required(login_url='login')
def registerResults(request):
     # Access the logged-in user
    logged_in_user = request.user
    students = User.objects.filter(accesslevel=3)
    if logged_in_user.accesslevel == 3:
        messages.error(request, 'Forbidden')
        return redirect(request.META.get('HTTP_REFERER'))
    elif  logged_in_user.accesslevel == 2:
        lecturer = Lecturer.objects.get(user_id = logged_in_user.id)
        students = User.objects.filter( Q(accesslevel=3) & Q(student_profile__course_id=lecturer.course_id_id))


    
    
    if request.method == "POST":
        mid_sem = request.POST.get("midsem")
        quiz = request.POST.get("quiz")
        lab = request.POST.get("lab")
        end_sem = request.POST.get("endsem")
        unit_id = request.POST.get("unitname")
        student_id = request.POST.get("student")
        score = request.POST.get("total_score")
        if not unit_id or not student_id or not score:
            messages.error(request, "Please fill all the fields")
        else:
            unit = Unit.objects.get(id=unit_id) 
            student = Student.objects.get(user_id=student_id)
            if Exam.objects.filter(unit_id = unit,student=student).exists():
                messages.error(request, f"Results for {student.user_id.firstname} {student.user_id.last_name} {unit.unit_name} already exist.")
            else:
                course = Exam.objects.create(unit_id = unit,lab=lab,quiz=quiz,midsem=mid_sem,endsem=end_sem,student=student,score=score,status=1)
                messages.success(request, "Exam saved successfully")
                
    return render(request, 'resultadd.html',{'students':students})

# fist get view course endpoint 
@login_required(login_url='login')
def viewCourse(request):
    return render(request, 'viewcourse.html')
# view course after fetch
@login_required(login_url='login')
def fetchCourseView(request):
    id = request.GET.get('course')
     # Access the logged-in user
    logged_in_user = request.user
    if logged_in_user.accesslevel == 3:
        
        student = Student.objects.get(user_id=logged_in_user.id)
        
        courses = Course.objects.filter(id=student.course_id_id)
        course = Course.objects.get(id=student.course_id_id)
        units = Unit.objects.filter(id=course.id)
    elif logged_in_user.accesslevel == 2:
        lecturer = Lecturer.objects.get(user_id=logged_in_user.id)
        
        courses = Course.objects.filter(id=lecturer.course_id_id)
        course = Course.objects.get(id=student.course_id_id)
        units = Unit.objects.filter(id=course.id)
    else:
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
@login_required(login_url='login')
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
@login_required(login_url='login')
def userCourse(request):
    access = request.GET.get('access')

    courses = Course.objects.all()
    if access == '2' or access == '3':
        return render(request, 'components/usercourse.html',{'courses':courses})
    else:
        return render(request, 'components/empty.html')
    

# get admission number
@login_required(login_url='login')
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

# view reports
@login_required(login_url='login')
def report(request):
    logged_in_user =request.user
    exams = Exam.objects.all()
    students =Student.objects.all()
    if logged_in_user.accesslevel == 3:
        student = Student.objects.get(user_id = logged_in_user.id)
        students = Student.objects.filter(user_id = logged_in_user.id)
        exams = Exam.objects.filter(student_id = student.id )
   
    elif logged_in_user.accesslevel == 2:
        lecturer = Lecturer.objects.get(user_id = logged_in_user.id)
        students = Student.objects.filter(course_id = lecturer.course_id_id)
        student = Student.objects.get (course_id = lecturer.course_id_id)
        exams = Exam.objects.filter(student_id = student.id )

    
    # else:
    #     pass

    return render(request, "report.html",{"exams":exams,"students":students})
# view results
@login_required(login_url='login')
def viewResults(request):
    logged_in_user =request.user
    exams = Exam.objects.all()
    students =Student.objects.all()
    if logged_in_user.accesslevel == 3:
        student = Student.objects.get(user_id = logged_in_user.id)
        students = Student.objects.filter(user_id = logged_in_user.id)
        exams = Exam.objects.filter(student_id = student.id )
   
    elif logged_in_user.accesslevel == 2:
        lecturer = Lecturer.objects.get(user_id = logged_in_user.id)
        students = Student.objects.filter(course_id = lecturer.course_id_id)
        student = Student.objects.get (course_id = lecturer.course_id_id)
        exams = Exam.objects.filter(student_id = student.id )

    
    # else:
    #     pass

    return render(request, "viewresults.html",{"exams":exams,"students":students})
# show reports
@login_required(login_url='login')
def displayReport(request):
    grade_remarks = {
    'A': [
        "Outstanding performance! Keep up the excellent work.",
        "Exceptional effort! Your dedication is truly commendable.",
        "Superior understanding of the subject matter. Well done!",
        "Remarkable achievement! Your hard work has paid off.",
        "Exemplary performance! You are setting a high standard.",
        "Consistently excellent work. Congratulations on your success.",
        "Admirable work ethic. Your results speak volumes.",
        "Stellar performance! Your determination is inspiring.",
        "Top-notch performance. You are a standout student.",
        "Exceptionally high quality of work. Congratulations on your achievement!"
    ],
    'B': [
        "Very good effort! You've demonstrated solid understanding.",
        "Good job! Your performance shows promise and improvement.",
        "Strong performance overall. Keep up the good work!",
        "Well done! Your results reflect your dedication.",
        "Competent work. Your effort is commendable.",
        "Satisfactory performance. You are on the right track.",
        "Respectable achievement. Your progress is evident.",
        "Capable performance. Continue striving for excellence.",
        "Above-average work. Your efforts are paying off.",
        "Decent performance. Keep working hard to reach your potential."
    ],
    'C': [
        "Fair effort. There's room for improvement, but you're making progress.",
        "Adequate performance. Keep working on your weaknesses.",
        "Acceptable work. Focus on strengthening your skills.",
        "Average performance. Aim to raise your standards.",
        "Sufficient effort. Keep pushing yourself to improve.",
        "Mediocre performance. Strive for better results next time.",
        "Basic understanding demonstrated. Work on mastering the concepts.",
        "Needs improvement. Identify areas for growth and development.",
        "Competent effort. Keep practicing to refine your skills.",
        "Average achievement. Aim higher for better outcomes."
    ],
    'D': [
        "Below-average performance. Identify areas for improvement.",
        "Limited understanding shown. Seek help to clarify concepts.",
        "Inconsistent effort. Work on maintaining focus and consistency.",
        "Needs considerable improvement. Put in extra effort to catch up.",
        "Partial understanding demonstrated. Review and practice more.",
        "Unsatisfactory performance. Take steps to address weaknesses.",
        "Below-par effort. Identify strategies to improve your results.",
        "Disappointing performance. Reflect on areas needing attention.",
        "Substandard work. Seek guidance to enhance your performance.",
        "Insufficient effort. Commit to putting in more work and dedication."
    ],
    'E': [
        "Poor performance. Immediate action is needed to address deficiencies.",
        "Inadequate effort. Reevaluate your approach and commitment.",
        "Serious concerns regarding performance. Seek assistance promptly.",
        "Below-standard work. Identify challenges and work to overcome them.",
        "Significant improvement required. Take proactive steps to enhance performance.",
        "Unacceptable performance. Address issues to prevent further decline.",
        "Falling short of expectations. Focus on improving your results.",
        "Urgent need for improvement. Take responsibility for your learning.",
        "Critical performance issues. Seek support to get back on track.",
        "Failing grade. Review your study habits and seek assistance as needed."
    ]
}



    student_id = request.GET.get("studentid")
   
    # Filter exams for the given student_id and order by course_id
    student = get_object_or_404(Student, id=student_id)
    course = student.course_id_id
    # Get all units associated with the course of the student
    all_units = Unit.objects.filter(course_id=course).values_list('id', flat=True)

    student_units = Exam.objects.filter(student=student).values_list('unit_id', flat=True).distinct()
    # Find missing unit_ids
    missing_units = set(all_units) - set(student_units)
    if missing_units:
        return render(request, 'components/missingunits.html')
    try:
        exams = Exam.objects.filter(student=student).order_by('unit_id')
        
        scores = 0
        number = 0
        for exam in exams:
            scores +=exam.score
            number += 1
        if number == 0:
            average = 0
        else:
            average = scores / number
        average =  round(average, 1)
        if average > 90:
            grade = 'A'
        elif average > 80:
            grade = 'B'
        elif average > 65:
            grade = 'c'
        elif average > 55:
            grade = 'D'
        else:
            grade = 'E'
        
        def get_random_remark(grade):
            remarks = grade_remarks.get(grade)
            if remarks:
                return random.choice(remarks)
            else:
                return "No remarks available for this grade."

    
        remarks = get_random_remark(grade)
        


        

        # Pass the ordered exam queryset to the template for rendering
        return render(request, 'components/viewreports.html', {'exams': exams,'average':average,'scores':scores,'remarks':remarks})

    except Exam.DoesNotExist:
        # Handle the case where no exam records are found for the given student_id
        return render(request, 'components/empty.html')



# display results per student
@login_required(login_url='login')
def displayResults(request):
    student = request.GET.get("studentid")
    try:
        # Filter exams for the given student_id and order by course_id
        exams = Exam.objects.filter(student_id=student).order_by('unit_id')
        scores = 0
        number = 0
        for exam in exams:
            scores +=exam.score
            number += 1
        if number == 0:
            average = 0
        else:
            average = scores / number
        average =  round(average, 1)

        

        # Pass the ordered exam queryset to the template for rendering
        return render(request, 'components/viewexams.html', {'exams': exams,'average':average,'scores':scores})

    except Exam.DoesNotExist:
        # Handle the case where no exam records are found for the given student_id
        return render(request, 'components/empty.html')

# login

def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        print(username)
        user = authenticate(request,username=username, password= password)
        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.error(request,"Username or Password is incorrect")

    return render(request, "login.html")



  