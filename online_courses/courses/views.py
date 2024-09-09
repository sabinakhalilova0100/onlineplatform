# courses/views.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import StudentRegistrationForm, LessonCreationForm, ModuleCreationForm, CourseCreationForm
from .models import User, Lesson, Module, Course, StudentProgress

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_admin:
                return redirect('admin_page')
            elif user.is_student:
                return redirect('student_page')
        else:
            return render(request, 'courses/login.html', {'error': 'Invalid credentials'})
    return render(request, 'courses/login.html')

@login_required
def admin_page(request):
    student_form = StudentRegistrationForm()
    lesson_form = LessonCreationForm()
    module_form = ModuleCreationForm()
    course_form = CourseCreationForm()

    if request.method == 'POST':
        if 'add_student' in request.POST:
            student_form = StudentRegistrationForm(request.POST)
            if student_form.is_valid():
                student_form.save()
                return redirect('admin_page')
        elif 'add_lesson' in request.POST:
            lesson_form = LessonCreationForm(request.POST, request.FILES)
            if lesson_form.is_valid():
                lesson_form.save()
                return redirect('admin_page')
        elif 'add_module' in request.POST:
            module_form = ModuleCreationForm(request.POST)
            if module_form.is_valid():
                module_form.save()
                return redirect('admin_page')
        elif 'add_course' in request.POST:
            course_form = CourseCreationForm(request.POST)
            if course_form.is_valid():
                course_form.save()
                return redirect('admin_page')
        elif 'delete_course' in request.POST:
            course_id = request.POST['course_id']
            Course.objects.filter(id=course_id).delete()
            return redirect('admin_page')

    students = User.objects.filter(is_student=True)
    lessons = Lesson.objects.all()
    modules = Module.objects.all()
    courses = Course.objects.all()

    context = {
        'student_form': student_form,
        'lesson_form': lesson_form,
        'module_form': module_form,
        'course_form': course_form,
        'students': students,
        'lessons': lessons,
        'modules': modules,
        'courses': courses,
    }
    return render(request, 'courses/admin_page.html', context)

@login_required
def student_page(request):
    if not request.user.is_student:
        return redirect('login')
    courses = Course.objects.all()
    return render(request, 'courses/student_page.html', {'courses': courses})

@login_required
def profile_page(request):
    progress = StudentProgress.objects.filter(student=request.user)
    return render(request, 'courses/profile.html', {'progress': progress})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'courses/course_detail.html', {'course': course})

def delete_student(request, student_id):
    student = get_object_or_404(User, id=student_id, is_student=True)
    if request.method == 'POST':
        student.delete()
        return redirect('admin_page')  # Предполагается, что у вас есть URL 'admin_page'
    return render(request, 'courses/delete_student.html', {'student': student})

@login_required
def delete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if request.method == 'POST':
        lesson.delete()
        return redirect('admin_page')  # Предполагается, что у вас есть URL 'admin_page'
    return render(request, 'courses/delete_lesson.html', {'lesson': lesson})

@login_required
def delete_module(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    if request.method == 'POST':
        module.delete()
        return redirect('admin_page')  # Предполагается, что у вас есть URL 'admin_page'
    return render(request, 'courses/delete_module.html', {'module': module})