from django.urls import path
from .views import *

urlpatterns = [
    path('worker_leads/', list_worker_leads, name='worker_lead_list'),
    path('worker_leads/create/', create_worker_lead, name='create_worker_lead'),
    path('worker_leads/<uuid:uuid>/update/', update_worker_lead, name='update_worker_lead'),
    path('worker_leads/<uuid:uuid>/delete/', delete_worker_lead, name='delete_worker_lead'),

    path('employee_leads/', list_employee_leads, name='employee_lead_list'),
    path('employee_leads/create/', create_employee_lead, name='create_employee_lead'),
    path('employee_leads/<uuid:uuid>/update/', update_employee_lead, name='update_employee_lead'),
    path('employee_leads/<uuid:uuid>/delete/', delete_employee_lead, name='delete_employee_lead'),

    path('send_employee/', send_employee_leads_to_crm, name='send_employee_leads_to_crm'),
    path('send_worker/', send_worker_leads_to_crm, name='send_worker_leads_to_crm'),
]
