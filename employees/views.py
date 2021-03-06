from django.shortcuts import render, HttpResponse, get_object_or_404
from django.views import View
from .forms import EmployeeForm
from .models import Salary, GroupSalaries
from django.http import JsonResponse
from rest_framework import viewsets
from .serializers import SalarySerializer, GroupSerializer
from django.contrib.auth.decorators import login_required


# Create your views here.
class SalaryView(viewsets.ModelViewSet):
	queryset = Salary.objects.order_by('-id')
	serializer_class = SalarySerializer

class GroupView(viewsets.ModelViewSet):
	queryset = GroupSalaries.objects.order_by('-id')
	serializer_class = GroupSerializer

@login_required(login_url='/admin/login/')
def manage(request):
	groups = GroupSalaries.objects.order_by('-id')
	return render(request, 'employees/manage.html', {'groups': groups})

@login_required(login_url='/admin/login/')
def get_salary_id(request, id_salary_finger):
	salary = Salary.objects.filter(id_salary_finger=id_salary_finger).first()
	return HttpResponse(salary.id)

@login_required(login_url='/admin/login/')
def get_group_id(request, id):
	group = GroupSalaries.objects.filter(id=id).first()
	return HttpResponse(group.id)

@login_required(login_url='/admin/login/')
def get_name_fk(request,id):
	groupe = GroupSalaries.objects.filter(id = id).first()
	return HttpResponse(groupe.name)