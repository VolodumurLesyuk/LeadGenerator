from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from customer.models import Customer
from .models import WorkerLead, EmployeeLead
from .forms import WorkerLeadForm, EmployeeLeadForm


# Worker
@login_required
def create_worker_lead(request):
    if request.method == 'POST':
        form = WorkerLeadForm(request.POST)
        if form.is_valid():
            customer = Customer.objects.get(user=request.user)
            form.instance.customer = customer
            form.save()
            return redirect('worker_lead_list')
    else:
        form = WorkerLeadForm()
    return render(request, 'lead/worker_lead_create.html', {'form': form})


@login_required
def update_worker_lead(request, uuid):
    worker_lead = get_object_or_404(WorkerLead, uuid=uuid)
    if request.method == 'POST':
        form = WorkerLeadForm(request.POST, instance=worker_lead)
        if form.is_valid():
            form.save()
            return redirect('worker_lead_list')
    else:
        form = WorkerLeadForm(instance=worker_lead)
    return render(request, 'lead/worker_lead_update.html', {'form': form})


@login_required
def delete_worker_lead(request, uuid):
    worker_lead = get_object_or_404(WorkerLead, uuid=uuid)
    if request.method == 'POST':
        worker_lead.delete()
        return redirect('worker_lead_list')
    return render(request, 'lead/worker_lead_delete_confirm.html', {'worker_lead': worker_lead})


@login_required
def list_worker_leads(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    leads = WorkerLead.objects.filter(customer=customer)
    return render(request, 'lead/worker_lead_list.html', {'leads': leads})


# Employee
@login_required
def create_employee_lead(request):
    if request.method == 'POST':
        form = EmployeeLeadForm(request.POST)
        if form.is_valid():
            customer = Customer.objects.get(user=request.user)
            form.instance.customer = customer
            form.save()
            return redirect('employee_lead_list')
    else:
        form = EmployeeLeadForm()
    return render(request, 'lead/employee_lead_create.html', {'form': form})


@login_required
def update_employee_lead(request, uuid):
    employee_lead = get_object_or_404(EmployeeLead, uuid=uuid)
    if request.method == 'POST':
        form = EmployeeLeadForm(request.POST, instance=employee_lead)
        if form.is_valid():
            form.save()
            return redirect('employee_lead_list')
    else:
        form = EmployeeLeadForm(instance=employee_lead)
    return render(request, 'lead/employee_lead_update.html', {'form': form})


@login_required
def delete_employee_lead(request, uuid):
    employee_lead = get_object_or_404(EmployeeLead, uuid=uuid)
    if request.method == 'POST':
        employee_lead.delete()
        return redirect('employee_lead_list')
    return render(request, 'lead/employee_lead_delete_confirm.html', {'employee_lead': employee_lead})


@login_required
def list_employee_leads(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    leads = EmployeeLead.objects.filter(customer=customer)
    return render(request, 'lead/employee_lead_list.html', {'leads': leads})
