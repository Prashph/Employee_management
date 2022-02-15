from django.shortcuts import render, redirect
from .models import Employee
from .forms import EmployeeForm
from django.db.models import Q
from django.contrib.auth import logout,authenticate,login
from django.contrib.auth.decorators import login_required


def loginuser(request):
    if request.method=='POST':
        username= request.POST.get('username')
        password= request.POST.get('password')

        user = authenticate(username=username, password=password)
        print(username,password)
        if user is not None:
            login(request,user)
            return redirect("/")
        else:
            return render(request, 'employee/login.html')
            
        
    return render(request, 'employee/login.html')

def logoutuser(request):
    logout(request)
    return redirect("/login")

def employees_list(request):
    if request.user.is_authenticated:
        search_query = ""

        if request.GET.get('search_query'):
            search_query = request.GET.get('search_query')

        employees = Employee.objects.filter(
            Q(emp_name__icontains=search_query) | 
            Q(emp_role__icontains=search_query) |
            Q(emp_salary__icontains=search_query)
        )

        context = {
            'employees': employees,
            'search_query': search_query,
        }
        return render(request, 'employee/list.html', context)
    else:
         return render(request, 'employee/login.html')

@login_required
def create_employee(request):
    form = EmployeeForm()

    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('employees-list')

    context = {
        'form': form,
    }
    return render(request, 'employee/create.html', context)

@login_required
def edit_employee(request, pk):
    employee = Employee.objects.get(id=pk)
    form = EmployeeForm(instance=employee)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employees-list')

    context = {
        'employee': employee,
        'form': form,
    }
    return render(request, 'employee/edit.html', context)

@login_required
def delete_employee(request, pk):
    employee = Employee.objects.get(id=pk)

    if request.method == 'POST':
        employee.delete()
        return redirect('employees-list')

    context = {
        'employee': employee,
    }
    return render(request, 'employee/delete.html', context)

