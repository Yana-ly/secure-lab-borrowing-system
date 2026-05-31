from django.urls import path

from . import views

app_name = "equipment"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("equipment/", views.equipment_list, name="equipment_list"),
    path("equipment/create/", views.equipment_create, name="equipment_create"),
    path("equipment/<int:pk>/edit/", views.equipment_update, name="equipment_update"),
    path("equipment/<int:pk>/delete/", views.equipment_delete, name="equipment_delete"),
    path("requests/", views.request_list, name="request_list"),
    path("requests/create/", views.request_create, name="request_create"),
    path("requests/<int:pk>/edit/", views.request_update, name="request_update"),
    path("requests/<int:pk>/delete/", views.request_delete, name="request_delete"),
    path("requests/<int:pk>/approve/", views.request_approve, name="request_approve"),
    path("requests/<int:pk>/reject/", views.request_reject, name="request_reject"),
    path("requests/<int:pk>/admin-delete/", views.admin_request_delete, name="admin_request_delete"),
]
