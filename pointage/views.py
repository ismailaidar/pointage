from django.shortcuts import render, get_object_or_404
from employees.models import Salary, GroupSalaries
from .models import Summary, TimeEnter
from .pointages import show_pointages

# Create your views here.
def profile(request, *args, **kwargs):
	try:
		salary 		= get_object_or_404(Salary, id_salary_finger = kwargs['id'])
		# salary 		=  Salary.objects.filter(id_salary_finger = kwargs['id']).first()
		new_list 	= []
		legal_time 	= get_object_or_404(TimeEnter, group=salary.group_salary)
		# legal_time 	= TimeEnter.objects.filter(group = salary.group_salary).first()
	except:
		context = {
			'salary' : salary,
			'error': "Ce salaire n'est pas lié à un groupe ou son groupe n'est pas lié à un TimeEntry, nous ne pouvions pas montrer les enregistrements"
		}
		return render(request, 'pointage/employees/profile.html', context)
	if request.method == 'POST':
		new_list 	= show_pointages(request.POST.get('start'), request.POST.get('end'),salary, Summary, legal_time)

	context = {
		'salary' : salary,
		'dates' : new_list,
		'legal_time': legal_time
	}
	return render(request, 'pointage/employees/profile.html', context)


def reports(request):
	try:
		salaries = Salary.objects.all()
		new_list = []

		if request.method == 'POST':
			for salary in salaries:
				legal_time 	= get_object_or_404(TimeEnter, group=salary.group_salary)
				new_list += [["{} {}".format(salary.first_name, salary.last_name), '0']]
				new_list += [show_pointages(request.POST.get('start'), request.POST.get('end'),salary, Summary, legal_time)]
	except:
		return render(request, 'pointage/employees/reports.html', {'error': "Certains salaires n'ont pas appartenu à un groupe ou un groupe n'est pas lié à un TimeEntry"})

	context = {
		'dates' : new_list,
	}
	return render(request, 'pointage/employees/reports.html', context)
