from django.http import JsonResponse

from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets

from .models import AtdRecord, AtdRecord_clone, Break, Holidays, Summary, TimeEnter
from .pointages import show_pointages
from .serializers import (
    BreakSerializer,
    GroupSerializer,
    HolidaysSerializer,
    SalarySerializer,
    TimeSerializer,
)
from employees.models import GroupSalaries, Salary
from genericpath import exists
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='/admin/login/')
def profile(request, *args, **kwargs):
    clone_atd()
    try:
        salary = get_object_or_404(Salary, id_salary_finger=kwargs["id"])
        # salary 		=  Salary.objects.filter(id_salary_finger = kwargs['id']).first()
        new_list = []
        legal_time = get_object_or_404(TimeEnter, group=salary.group_salary)
        # legal_time 	= TimeEnter.objects.filter(group = salary.group_salary).first()
    except:
        context = {
            "salary": salary,
            "error": "Ce salaire n'est pas lié à un groupe ou son groupe n'est pas lié à un TimeEntry, nous ne pouvions pas montrer les enregistrements",
        }
        return render(request, "pointage/employees/profile.html", context)
    if request.method == "POST":
        new_list = show_pointages(
            request.POST.get("start"),
            request.POST.get("end"),
            salary,
            Summary,
            legal_time,
        )

    context = {"salary": salary, "dates": new_list, "legal_time": legal_time}
    return render(request, "pointage/employees/profile.html", context)

@login_required(login_url='/admin/login/')
def reports(request):
    clone_atd()
    try:
        salaries = Salary.objects.all()
        new_list = []

        if request.method == "POST":
            for salary in salaries:
                legal_time = get_object_or_404(TimeEnter, group=salary.group_salary)
                new_list += [["{} {}".format(salary.first_name, salary.last_name), "0"]]
                new_list += [
                    show_pointages(
                        request.POST.get("start"),
                        request.POST.get("end"),
                        salary,
                        Summary,
                        legal_time,
                    )
                ]
    except:
        return render(
            request,
            "pointage/employees/reports.html",
            {
                "error": "Certains salaires n'ont pas appartenu à un groupe ou un groupe n'est pas lié à un TimeEntry"
            },
        )

    context = {"dates": new_list}
    return render(request, "pointage/employees/reports.html", context)

@login_required(login_url='/admin/login/')
def manage(request):
    groups = GroupSalaries.objects.order_by("-id")
    return render(request, "pointage/times/manage.html", {"groups": groups})


class TimeEnterView(viewsets.ModelViewSet):
    queryset = TimeEnter.objects.order_by("-id")
    serializer_class = TimeSerializer


class BreakView(viewsets.ModelViewSet):
    queryset = Break.objects.order_by("-id")
    serializer_class = BreakSerializer


class GroupView(viewsets.ModelViewSet):
    queryset = GroupSalaries.objects.order_by("-id")
    serializer_class = GroupSerializer


class SalaryView(viewsets.ModelViewSet):
    queryset = Salary.objects.order_by("-id")
    serializer_class = SalarySerializer


class HolidaysView(viewsets.ModelViewSet):
    queryset = Holidays.objects.order_by("-id")
    serializer_class = HolidaysSerializer


def get_time_id(request, id):
    time = TimeEnter.objects.filter(id=id).first()
    return HttpResponse(time.id)


def clone_atd():
    atd_data = AtdRecord_clone.objects.all()
    for data in atd_data:
        if not AtdRecord.objects.filter(SerialId=data.SerialId).exists():
            new_atd = AtdRecord(
                SerialId=data.SerialId,
                CardNo=data.CardNo,
                RecDate=data.RecDate,
                RecTime=data.RecTime,
                dateb=data.dateb,)
            new_atd.save()
