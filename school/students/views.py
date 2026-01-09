from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.

def student_list(request):
    students = Student.objects.all()
    return render(request, 'students_list.html', {'students': students})


def student_signup(request):
    if request.method == "POST":

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

#       verification
        if password != password2:
            messages.error(request, 'Les mot de passe ne correspondent pas ')
            return redirect('signup')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur existe deja ")
            return redirect('signup')
    
        if User.objects.filter(email=email).exists():
            messages.error(request, "Cet email est deja utilise ")
            return redirect('signup')
        
#  end verification 

        user = User.objects.create_user(
            username=username,
            email = email,
            password=password2
        )

        user.save()
        messages.success(request, 'Compte cree avec succes')
        return redirect('student_list')


    return render(request, 'signup.html')





















def student_create(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Student has been added successfully !")
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'student_form.html',{'form':form})


def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student has been updated successfully !')
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'student_update.html', {'student': student})



def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        student.delete()
        messages.success(request, 'Student deleted successfully !')
        return redirect('student_list')
    return render(request, 'student_delete_confirm.html', {'student_information': student})
