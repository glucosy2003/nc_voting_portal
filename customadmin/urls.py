from django.urls import path
from . import views

app_name = 'customadmin'

urlpatterns = [
    path('', views.admin_login, name='admin_login'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('logout/', views.admin_logout, name='admin_logout'),

    path('candidates/', views.manage_candidates, name='manage_candidates'),
    path('candidates/approve/<int:candidate_id>/', views.approve_candidate, name='approve_candidate'),
    path('candidates/reject/<int:candidate_id>/', views.reject_candidate, name='reject_candidate'),
    path('candidates/delete/<int:candidate_id>/', views.delete_candidate, name='delete_candidate'),


    path('results/', views.view_results, name='view_results'),
    path('registered-voters/', views.registered_voters, name='registered_voters'),


    # Valid students
    path('valid-students/', views.list_valid_students, name='list_valid_students'),
    path('valid-students/add/', views.add_valid_student, name='add_valid_student'),
    path('valid-students/delete/<int:pk>/', views.delete_valid_student, name='delete_valid_student'),

    path('change-password/', views.change_admin_password, name='change_admin_password'),
    path('countdown/', views.countdown_timer_control, name='countdown_timer_control'),

    path('clear-votes/', views.clear_votes, name='clear_votes'),

]
